import bb_load as bb_l
import bb_group as bb_g
import time
from dateutil.relativedelta import relativedelta
import pandas

def filt_ticker_list(ticker_list, lim_vol, se):

    '''

    (ticker_list) -> list of str

    Sort ticker_list on different financial attributes from
    get_financial_data(ticker_list) and returns a sorted list of tickers
    
    '''

    # Import and transpose the dataframe of financial data
    df = bb_l.load_fin_dat_df(ticker_list) 
    
    legend = []
    legend.append('name') # Cell 00 Name
    legend.append('stex') # Cell 01 Stock exchange
    legend.append('pric') # Cell 02 Price
    legend.append('ldch') # Cell 03 Last day change
    legend.append('ldvo') # Cell 04 Last day volume
    legend.append('advo') # Cell 05 Avg day volume
    legend.append('mcap') # Cell 06 Market cap
    legend.append('bval') # Cell 07 Book value
    legend.append('edea') # Cell 08 EBITDA
    legend.append('divs') # Cell 09 Dividend per share
    legend.append('divy') # Cell 10 Dividend yield
    legend.append('epsh') # Cell 11 Earnings per share
    legend.append('52wh') # Cell 12 52 week high
    legend.append('52wl') # Cell 13 52 week low
    legend.append('50ma') # Cell 14 50 day moving average
    legend.append('200m') # Cell 15 200 day moving average
    legend.append('pera') # Cell 16 Price earnings ratio
    legend.append('pegr') # Cell 17 Price earnings growth ratio
    legend.append('psra') # Cell 18 Price sales ratio
    legend.append('pbra') # Cell 19 Price book ratio
    legend.append('shra') # Cell 20 Short ratio
    df.columns = legend

    df['voldollars'] = df.iloc[:,2]*df.iloc[:,5]
    # Sort dataframe
    filt_df = df[(df.voldollars > float(lim_vol))]
    
    # Filters away any stock traded on certain exchanges
    if bool(se):
        filt_df = filt_df[((filt_df.stex == 'NMS') | \
                               (filt_df.stex == 'NYQ'))]
    
    # Make sorted ticker list
    filt_ticker_list = filt_df.index.tolist()

    return filt_ticker_list

def filt_tickers_time_since_bb(ticker_list, time_range):

    '''

    (ticker_list, time_range) -> list of tickers

    Filter <ticker_list> by removing tickers for which buyback announcement
    was made within the last <time_range> weeks.

    Version 2.0: MPPA @ 20:20 05.05.2014
    
    '''
    time_end = time.strftime("%Y-%m-%d")
    time_beg = pandas.to_datetime(time_end) - relativedelta(weeks = time_range)
    time_beg = time_beg.strftime("%Y-%m-%d")

    # Load list of recent buybacks and remove tickers
    recent_bb = bb_g.group_bb_df(time_beg, time_end).T.index.tolist()
    for i in recent_bb:
        if i in ticker_list:
            ticker_list.remove(i)
            
    return ticker_list
