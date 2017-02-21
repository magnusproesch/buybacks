import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame, read_csv
import time

# Read buybacks from database into a list for further processing
def load_ticker_list(time_beg, time_end):

    '''
    Version 1.1: MSP @ 14:00 15.05.14
    
    (time_beg, time_end) -> list of strings

    <time_beg> and <time_end> in format yyyy-mm-dd
    If <time_beg> <=0, set <time_beg> = 1970-01-01
    If <time_end> <=1, set <time_end> = Today's date

    Read a file (scrape_database.csv) and return a list of the tickers for
    which buybacks were announced between <time_beg> and <time_end>.
    
    '''
    
    source = open('scrape_database.csv','r')

    if time_beg <= 0: time_beg = 0
    if time_end <= 1: time_end = time.strftime("%Y-%m-%d")

    time_beg = pd.to_datetime(time_beg)
    time_end = pd.to_datetime(time_end)

    raw_ticker_list = []

    line = source.readline()
    
    while line !='':
        
        bb_date = pd.to_datetime(line[:line.find(",")])
        
        if (bb_date < time_end) & (bb_date > time_beg):
            ticker = line[line.find(",") + 1 : line.rfind(",")]

            if ticker not in raw_ticker_list:
                raw_ticker_list.append(str(ticker))

        line = source.readline()

    source.close()

    return raw_ticker_list
    print raw_ticker_list


# Make dataframe of buybacks for further processing
def load_buyback_df(time_beg, time_end):

    '''

    Version 1.1: MSP @ 14:00 15.05.14
    
    (time_beg, time_end) -> dataframe

    <time_beg> and <time_end> must be in format yyyy-mm-dd

    Read a file (scrape_database.csv) and return
    a dataframe of dates, tickers, and amounts of buybacks
    announced between <time_beg> and <time_end>.
    
    '''
   
    source = open('scrape_database.csv','r')
    line = source.readline()

    dates = []
    tickers = []
    amounts = []


    if time_beg <= 0: time_beg = 0
    if time_end <= 0: time_end = time.strftime("%Y-%m-%d")

    time_beg = pd.to_datetime(time_beg)
    time_end = pd.to_datetime(time_end)    
    
    while line !='':
       
        bb_date = pd.to_datetime(line[:line.find(",")])

        date = line[0:line.find(",")]
        ticker = line[line.find(",") + 1 : line.rfind(",")]
        amount = line[line.rfind(",")+1:len(line)+1]

        if (bb_date <= time_end) & (bb_date >= time_beg):
            dates.append(str(date))
            tickers.append(str(ticker))
            amounts.append(float(str(amount.strip('\n'))))
            
        line = source.readline()

    df = zip(dates,amounts) # Combine the two lists into one list
    
    source.close()

    #Convert list to dataframe
    if len(tickers)>0:
        ticker_df = DataFrame(data=df,index=tickers,columns=['Date','Amount'])
    else:
        ticker_df = DataFrame(index=tickers,columns=['Date','Amount'])
    return ticker_df.T

# Make dataframe of prices for ticker_list
def load_price_df(ticker_list):

    '''

    Version 2.0: MPPA @ 17:45 29.04.14
    
    (ticker_list) -> dataframe

    Read file prices.csv and return a dataframe containing historic prices of
    the stocks in <ticker_list>, obtained from the csv.
    
    '''

    df = read_csv('prices.csv')
    full_ticker_df = df['Unnamed: 0']
    ind = df.columns.tolist()
    ind.pop(0)
    full_ticker = full_ticker_df.tolist()
    df = df.T
    df = df[1:]
    df.columns = full_ticker

    # Selecting the shorter ticker_list. Needed when some tickers no longer are found in the price database
    try:
        r = df[ticker_list]
    except (KeyError):
        r = df[full_ticker]
        
    r = r.T

    return r.convert_objects(convert_numeric=True)

# Make dataframe of financial data for ticker_list
def load_fin_dat_df(ticker_list):

    '''

    Version 2.0: MPPA @ 17:45 29.04.14
    
    (ticker_list) -> dataframe

    Read file financial_data.csv and return a dataframe
    containing financial data for tickers in <ticker_list>.
    
    '''

    df = read_csv('financial_data.csv')
    full_ticker_df = df['Unnamed: 0']
    ind = df.columns.tolist()
    ind.pop(0)
    full_ticker = full_ticker_df.tolist()
    df = df.T
    df = df[1:]
    df.columns = full_ticker
    #r = df[ticker_list]
    r = df[full_ticker]
    r = r.T
    return r.convert_objects(convert_numeric=True)

# Make dataframe of historic prices of benchmark in database
def load_benchmark_df():

    '''

    Version 1.1: MSP @ 15:25 08.05.14
    
    ( ) -> dataframe

    Read file prices.csv and return a dataframe
    containing historic price of benchmark obtained from the csv.
    
    '''

    df = read_csv('prices.csv')
    full_index_df = df['Unnamed: 0']
    col = df.columns.tolist()
    col.pop(0)
    full_index = full_index_df.tolist()
    df = df.T
    df = df[1:]
    df.columns = full_index
    r = df[full_index[0]]

    return r.convert_objects(convert_numeric=True)

# Load name of benchmark in database as string
def load_benchmark_name():

    '''

    Version 1.0: MPPA @ 22:45 04.05.14
    
    ( ) -> string

    Read file prices.csv and return a string
    containing the name of benchmark in the csv.
    
    '''

    df = read_csv('prices.csv')
    full_ticker_list = df['Unnamed: 0'].tolist()
    return full_ticker_list.pop(0)
