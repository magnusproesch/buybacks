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

        df_cur = pd.concat([df_buy,df_sel],axis = 1)
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

        s_cost = (s_position * s_price - s_com)
    
        df_sel[ticker] = pd.Series([ticker, s_position, s_price, \
                                 s_fx, s_date, s_com, s_cost], index = s_legend)
    
    print df_buy
    print df_sel
    print df_cur
    
    #Add buy and sell to the current portfolio
    df_cur = pd.concat([df_cur, df_buy, df_sel],axis = 1)
    print df_cur

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
    
    
