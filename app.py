from flask import Flask, render_template, request, redirect
import requests # accessing data
import pandas as pd # data wrangling
import bokeh # plotting results
from bokeh.plotting import figure, output_file, show

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/graph.html',methods=['GET','POST'])
def stock_pars():

    # gives a dictionary of all the values
    # checkbox is given as "on" if checked, not included if not checked
    req = request.form

    # ticker symbol for the company
    var_tick = req['tick_symb']

    myapi = "596NHA9N0W7KPYL4"

    # extracting the daily and daily adjusted data
    # will only get compact data (last 100 days) because not passing an optional output size
    # extracting directly as csv
    vari_dict_adj = {'function': 'TIME_SERIES_DAILY_ADJUSTED', 'symbol': var_tick,'apikey':myapi,'datatype':'csv'}

    # requesting data from the website
    req_dat = requests.get('https://www.alphavantage.co/query?', params=vari_dict_adj)

    # reading in the file
    # column headings are:
    # timestamp, open, high, low, close, adjusted_close, volume, dividend_amount, split_coefficient
    readin = pd.read_csv(req_dat.url)

    # naming output file
    output_file("graph.html")

    # tools that can be displayed
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

    # colors to use
    # copied values from colorbrewer, 5-Class Dark 2
    cols_use = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e']

    # setting up figure with title and setting x axis to be a datetime
    p1 = figure(title="Stock Price", tools=TOOLS,x_axis_type='datetime')

    # adding lines
    # each line will be one of the variables
    # variables selected will be in the dictionary, but unselected ones will not
    if 'open' in req.keys():
        p1.line(pd.to_datetime(readin['timestamp']),readin['open'],line_color=cols_use[0], legend="Open")
    if 'close' in req.keys():
        p1.line(pd.to_datetime(readin['timestamp']),readin['close'],line_color=cols_use[1], legend="Close")
    if 'close_adj' in req.keys():
        p1.line(pd.to_datetime(readin['timestamp']),readin['adjusted_close'],line_color=cols_use[2], legend="Close Adj")
    if 'low' in req.keys():
        p1.line(pd.to_datetime(readin['timestamp']),readin['low'],line_color=cols_use[3], legend="Low")
    if 'high' in req.keys():
        p1.line(pd.to_datetime(readin['timestamp']),readin['high'],line_color=cols_use[4], legend="High")

    show(p1)
    '''
    # adding opening stock prices, if selected
    if 'open_id' in lister:
        df_stocks['Open'] = df_stocks['open']
    else:
        df_stocks.drop('Open',axis=1,inplace=True)

    # adding opening adjusted stock prices, if selected
    if 'open_adj_id' in lister:
        df_stocks['OpenAdj'] = df_stocks_adj['open']
    else:
        df_stocks.drop('OpenAdj',axis=1,inplace=True)

    # adding closing stock prices, if selected
    if 'close_id' in lister:
        df_stocks['Close'] = df_stocks['Close']
    else:
        df_stocks.drop('Open',axis=1,inplace=True)

    # adding closing adjusted stock prices, if selected
    if 'close_adj_id' in lister:
        df_stocks['CloseAdj'] = df_stocks_adj['close']
    else:
        df_stocks.drop('CloseAdj',axis=1,inplace=True)
    '''

    return render_template('graph.html')

if __name__ == '__main__':
  app.run(port=33507)
