import datetime
import pandas as pd
import pandas.io.data
from pandas import Series, DataFrame
from dateutil.relativedelta import relativedelta
import time
import math
    
#Get the past stock return for each ticker
def get_historic_prices(ticker_list, indices):

    '''
    (list of str) -> NoneType
    
    Read a list of stock tickers, fetch their past historic
    adjusted close prices, and print the returns to
    returns.csv in the root folder


    Version 1.0, MPPA @ 10:00 29-Apr-2014
    '''

    filename = 'prices.csv'
    print_est1 = 50
    print_est2 = 250
    est = True
    
    # Prompt number of months to get prices
    hist_months = int(raw_input('\n' +"How many months of historic prices" \
                            " do you want to fetch?" + '\n' + \
                            "Please enter number of months as integer: "))

    # Prompt index choice
    names = indices.keys()
    names.sort()
    ind=[indices[i] for i in names]
    print '\n'+'Which index do you want as benchmark?'
    for i in range(1,len(ind)+1):
        print str(i)+': '+names[i-1]
    bench_q = int(raw_input('Choose your input: '))
    if ((bench_q > 0) & (bench_q < len(ind)+1)):
        print '-> Selected', names[bench_q-1]
    else:
        bench_q = len(ind)
        print '-> Invalid input, proceeding with', names[bench_q-1],\
              'as benchmark!' 
    benchmark=ind[bench_q-1]

    # Mirror raw_ticker_list in case of errors
    ticker_list.insert(0,benchmark)    
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
    print '\nFetching historical price data for ' + str(len(ticker_list)-1) + \
          ' companies and index.'
    
    #Get time series for securities
    for ticker in ticker_list:
        try:
            s = pd.io.data.get_data_yahoo(ticker, \
                      start=datetime.datetime(past.year, past.month, past.day), \
                      end=datetime.datetime(now.year, now.month, now.day)) \
                      ['Adj Close']          
            s.name = ticker # Rename series to match security name
            prices.append(s)
        
            
        except (IOError, Warning): # Resort to manual input of ticker
            #man_ticker = raw_input("-> There was a problem with the ticker " \
                                  #+ ticker + '.' + '\n' + \
                                  #"Please enter an alternative spelling: ")
            man_ticker = '0'  
            #Remove bad ticker from clean_stock_list and increase drop counter          
            if ticker != benchmark:
                ticker_list.remove(ticker)
            drop_count = drop_count + 1
            adj_list.append(str(ticker+' -> '+man_ticker))

            try:
                s = pd.io.data.get_data_yahoo(man_ticker,\
                      start=datetime.datetime(past.year, past.month, past.day),\
                      end=datetime.datetime(now.year, now.month, now.day))\
                      ['Adj Close']
                s.name = man_ticker
                prices.append(s)
                if ticker != benchmark:
                    ticker_list.append(man_ticker)

            except (IOError, Warning): #Prompt failure to fetch time series
                #print '-> There is still a problem with ' + man_ticker \
                #     + '. Proceeding without ticker.'
                drop_count = drop_count + 1
                drop_list.append(man_ticker)
                if ticker == benchmark:
                    print '-> No benchmark included with prices!'
            if est:
                checked = 0
                st_time = time.time()
            
        if est:
            if checked < print_est2:
                checked = checked + 1
            if checked == print_est1:
                el_time = time.time() - st_time
                iter_time = el_time/checked
                tot_time = iter_time*len(ticker_list)
                tot_h = math.floor(tot_time/3600)
                tot_m = math.floor((tot_time-tot_h*3600)/60)
                tot_s = tot_time-tot_h*3600-tot_m*60
                t=datetime.timedelta(hours=tot_h,minutes=tot_m,seconds=int(tot_s))
                fin_date = start_date + t
                print 'Estimated finish:   ' + \
                      fin_date.strftime("%H:%M:%S, %B %d, %Y") + ' (based on ' + \
                      str(print_est1) + ' iterations)'
                print 'Time per iteration: ' + \
                      "%2.4f" %(iter_time)+' sec' + ' (based on ' + \
                      str(print_est1) + ' iterations)'
            if checked == print_est2:
                el_time = time.time() - st_time
                iter_time = el_time/checked
                tot_time = iter_time*len(ticker_list)
                tot_h = math.floor(tot_time/3600)
                tot_m = math.floor((tot_time-tot_h*3600)/60)
                tot_s = tot_time-tot_h*3600-tot_m*60
                t=datetime.timedelta(hours=tot_h,minutes=tot_m,seconds=int(tot_s))
                fin_date = start_date + t
                print 'Updated estimated finish:   ' + \
                      fin_date.strftime("%H:%M:%S, %B %d, %Y") + ' (based on ' + \
                      str(print_est2) + ' iterations)'
                print 'Updated time per iteration: ' + \
                      "%2.4f" %(iter_time)+' sec' + ' (based on ' + \
                      str(print_est2) + ' iterations)'
                est = False
            

    ticker_list.pop(0)
    
    #Write the data to the file
    prices_df = pd.concat(prices, axis=1)
    prices_df = prices_df.ffill()
    prices_df = prices_df.T
    prices_df.to_csv(filename,tupleize_cols=False)
    #print ticker_list
    #print len(ticker_list)

    # Print summary
    print '\n'+ '---------------------------------------' \
          + '-------------------------------'
    print 'MODULE: ADJ. CLOSE PRICES LAST', str(hist_months), 'MONTHS.'
    print 'Output:', filename, '\n'
    print 'Total time series pinged:', len(prices)+drop_count
    print 'Drop count:', drop_count
    print 'Initial problems with (incl alt ticker):', adj_list
    print 'Still problems with:', drop_list
    print 'Total time series fetched successfully:', len(prices)
    print 'Run-time:', "%.2f" %(time.time() - start_time), 'sec'
    print '---------------------------------------' \
          + '-------------------------------' + '\n'
    
    return prices_df.convert_objects(convert_numeric=True)
