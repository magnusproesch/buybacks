import pandas as pd
from pandas import DataFrame, read_csv

def load_transactions():
    '''
    NoneType -> df

    Loads all transactions from database or writes and empty df
    if the file is missing or corrupt.

    Version 0.1 MSP @ 02-Jul-2014
    
    '''

    try:
        #Load
        df_cur = read_csv('all_transactions.csv', index_col = 0) 
        print '-> Successfully loaded ' + str(len(df_cur)) + \
              ' transactions from the database.' + '\n'

    except (IOError, Warning):
        #Create empty
        df_cur = []
        print('Warning: Could not find the transaction file.' '\n'
              '-> Will create new dataframes and new files.')

    return df_cur

def write_portfolio(df_cur):
    '''

    prompt(str,bool) -> df

    Writes buy and sell to the list of transactions file.
    
    Version 0.1 MSP @ 02-Jul-2014
    
    '''
        
    #Def some of the variables used
    b_legend = []
    b_legend.append('Ticker')
    b_legend.append('Position')
    b_legend.append('Price')
    b_legend.append('Currency')
    b_legend.append('Date bought')
    b_legend.append('Commission')
    b_legend.append('Total cost')

    df_buy = pd.DataFrame(index = b_legend)
        
    s_legend = []
    s_legend.append('Ticker')
    s_legend.append('Position')
    s_legend.append('Price')
    s_legend.append('Currency')
    s_legend.append('Date sold')
    s_legend.append('Commission')
    s_legend.append('Total cost')

    df_sel = pd.DataFrame(index = s_legend)
    
    #Prompt buy
    print('--------------------------------------------')  
    num_new = int(input('How many new stocks have you purchased? '))

    for new in range(num_new):
        print('--------------------')
        ticker = str(raw_input('Ticker: '))
        b_date = str(raw_input('Date (yyyy-mm-dd): '))
        b_fx = str(raw_input('Currency: '))
        b_position = int(raw_input('Number of shares: '))
        b_price = float(raw_input('Price (xx.xx): '))

        if (b_position * b_price * 0.0015) > 13: #minimum commission requirement
            b_com = b_position * b_price * 0.0015
        else:
            b_com = 13

        b_cost = (b_position * b_price + b_com) * (-1)
    
        df_buy[ticker] = pd.Series([ticker, b_position, b_price, \
                                 b_fx, b_date, b_com, b_cost], index = b_legend)
        
    #Prompt sell
    print('--------------------------------------------')
    num_sel = int(input('How many new stocks have you sold? '))

    for new in range(num_sel):
        print('--------------------')
        ticker = str(raw_input('Ticker: '))
        s_date = str(raw_input('Date (yyyy-mm-dd): '))
        s_fx = str(raw_input('Currency: '))
        s_position = - int(raw_input('Number of shares: '))
        s_price = float(raw_input('Price (xx.xx): '))

        if (s_position * s_price * 0.0015 * (-1) ) > 13: #minimum commission requirement
            s_com = s_position * s_price * 0.0015 * (-1)
        else:
            s_com = 13

        s_cost = (s_position * s_price - s_com)*(-1)
    
        df_sel[ticker] = pd.Series([ticker, s_position, s_price, \
                                 s_fx, s_date, s_com, s_cost], index = s_legend)
    
    #Add buy and sell to the current portfolio   
    if len(df_cur) == 0:
        df_cur = pd.concat([df_buy, df_sel],axis = 1).T
    else:
        df_cur = pd.concat([df_cur.T, df_buy, df_sel],axis = 1).T

    #Write to file
    df_cur.to_csv('all_transactions.csv')

def print_transaction_list():
    '''
    NoneType -> df
    
    Load, rearrange, and print transaction list
    '''
    
    df_cur = load_transactions()
    
    df_cur = df_cur[['Currency',\
                        'Date bought',\
                        'Date sold',\
                        'Position',\
                        'Price',\
                        'Commission',\
                        'Total cost']]
    
    print df_cur
    

def consolidate_df():
    '''

    Consolidate dataframe
    
    '''

    import port_func as pf

    # Get unique list of tickers from transaction database

    df = pf.load_transactions()
    tickers = list(set(df.index.values.tolist()))

    # Get net positions
    net = df.groupby(['Ticker']).sum()

    # Calculate relative share of cost and append to dataframe
    cost_col = net['Total cost']
    w = []
    for n in range(len(cost_col)):
        w.append(cost_col[n-1] / cost_col.sum())

    w = pd.DataFrame(w,index=tickers,columns=['Weight'])
    net.join(w) 
    net_df = net 

    return net_df


def get_current_prices():
    '''
    '''
    
    import urllib
    import port_func as pf

    # Get unique list of tickers from consolidated dataframe
    df = pf.consolidate_df()
    tickers = df.index.values.tolist()

    stat = 'b0'
    ask = []

    # Get updated market prices and append to dataframe
    for stock in tickers:
        url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (stock, stat)
        value = float(urllib.urlopen(url).read().strip().strip('"').split(',')[0])
        ask.append(value)

    bid = pd.DataFrame(ask,index=tickers,columns=['Bid'])

    df = df.join(bid)

    # Calculated updated P&L
    gain = []
    rel = []
    
    for n in range(len(tickers)):
        abs_diff = ((df['Bid'][n]-df['Price'][n]) * df['Position'][n]) - df['Commission'][n]
        rel_diff = (-abs_diff) / df['Total cost'][n]
        gain.append(abs_diff)
        rel.append(rel_diff)

    gain = pd.DataFrame(gain,index=tickers,columns=['Net gain'])
    rel = pd.DataFrame(rel,index=tickers,columns=['Net dev.'])

    df = df.join(gain)
    df = df.join(rel)

    df = df.drop('Commission',1)   
    df = df.drop('Date sold',1)

    # Make currency adjusted returns
    gain_fx = []

    url = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=USDNOK=X'
    fx = float(urllib.urlopen(url).read().strip().strip('"').split(',')[1])

    gain_fx = gain * fx
    gain_fx = gain_fx.rename(columns = {'Net gain': 'Net NOK gain'})

    df = df.join(gain_fx)

    # Sum the columns:
    sum_row = {col: df[col].sum() for col in df}
    # Turn the sums into a DataFrame with one row with an index of 'Total':
    sum_df = pd.DataFrame(sum_row, index=["Total"])
    # Now append the row:
    df = df.append(sum_df)
    
    # Rearrange the matrix
    df = df[['Bid',\
             'Price',\
             'Net gain',\
             'Net NOK gain',\
             'Net dev.',\
             'Position',\
             'Total cost']]
    
    net_df = df
    
    return net_df

def risk_reward():
    '''

    '''
    import urllib
    import port_func as pf
    import datetime
    import time
    import pandas.io.data
    from dateutil.relativedelta import relativedelta

    # Get tickers in portfolio

    df = pf.consolidate_df()
    tickers = df.index.values.tolist()
    
    ### Get historic prices
    
    # Prompt number of months to get prices
    hist_months = int(raw_input('\n' +"How many months of historic prices" \
                            " do you want to fetch?" + '\n' + \
                            "Please enter number of months as integer: "))

    # Mirror raw_ticker_list in case of errors
    '''tickers.insert(0,benchmark)'''    
    prices = []
    drop_count = int(0)
    drop_list = []
    adj_list = []

    now = datetime.datetime.now() 
    past = datetime.datetime(now.year, now.month, now.day)+ \
           relativedelta(months = - int(hist_months) )

    # Start clock
    start_time = time.time()
    st_time = start_time
    start_date = datetime.datetime.now()
    checked = 0
    print '\nFetching historical price data for ' + str(len(tickers)) + \
          ' companies.'

    #Get time series for securities
    for ticker in tickers:
        s = pd.io.data.get_data_yahoo(ticker, \
                      start=datetime.datetime(past.year, past.month, past.day), \
                      end=datetime.datetime(now.year, now.month, now.day)) \
                      ['Adj Close']
        s.name = ticker # Rename series to match security name
        prices.append(s)

    prices_df = pd.concat(prices, axis=1)
    prices_df = prices_df.ffill()
    
    #Write the data to the file
    filename = 'port_prices.csv'
    prices_df = prices_df.T
    prices_df.to_csv(filename,tupleize_cols=False)

    ## various calculations
    rets = prices_df.pct_change()
    rets_mu = (1+rets.mean())**250 - 1
    std_mu = rets.std()*(250**0.5)
    sharpe = (rets_mu - 0.04) / std_mu

    # get historic fx rates from file
    df = read_csv('fx_USDNOK_py.csv')
    df = df.set_index('End Date')
    
    
        
