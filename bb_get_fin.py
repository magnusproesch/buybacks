
import pandas as pd
import urllib
import time
import math
from dateutil.relativedelta import relativedelta
import datetime
    
#Get specific financial data for list of tickers
def get_financial_data(ticker_list):

    '''
    (list of str) -> list

    Get all available quote data for the given ticker symbols.

    Version 2.1, MSP @ 03.05.14 15:20
    
    '''

    print_est1 = 50
    print_est2 = 250
    est = True
    filename = 'financial_data.csv'

    # Start clock
    start_time = time.time()
    st_time = start_time
    start_date = datetime.datetime.now()
    checked = 0
    print '\nFetching financial data of ' + str(len(ticker_list)) + \
          ' companies.'
    
    stat = 'nxpp2va2j1b4j4dyekjm3m4rr5p5p6s7'
    not_added = 0
    
    legend = []
    legend.append('Name') #                         Cell 00
    legend.append('Stock Exchange') #               Cell 01
    legend.append('Price') #                        Cell 02
    legend.append('Last Day Change (%)') #          Cell 03
    legend.append('Last Day Volume') #              Cell 04
    legend.append('Average Daily Volume') #         Cell 05
    legend.append('Market Cap (M)') #               Cell 06
    legend.append('Book Value per Share') #         Cell 07
    legend.append('EBITDA (M)') #                   Cell 08
    legend.append('Dividend per Share') #           Cell 09
    legend.append('Dividend Yield (%)') #           Cell 10
    legend.append('Earnings per Share') #           Cell 11
    legend.append('52 Week High') #                 Cell 12
    legend.append('52 Week Low') #                  Cell 13
    legend.append('50 Day Moving Average') #        Cell 14
    legend.append('200 Day Moving Average') #       Cell 15
    legend.append('Price Earnings Ratio') #         Cell 16
    legend.append('Price Earnings Growth Ratio') #  Cell 17
    legend.append('Price Sales Ratio') #            Cell 18
    legend.append('Price Book Ratio') #             Cell 19
    legend.append('Short Ratio') #                  Cell 20

    # add row description as first column
    master = pd.DataFrame(data = legend, index = legend, columns = ['Legend']) 

    for stock in ticker_list:
        url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (stock, stat)
        values = urllib.urlopen(url).read().strip().strip('"').split(',')
        # Recombine additional Name cells (Cell 00)
        while len(values) > len(legend) :
            temp = values.pop(1)
            values[0] = values[0] + temp
        # Remove unvanted signs from Name (Cell 00)
        values[0] = values[0].strip('"').strip().strip('"').strip()
        # Remove "" from Stock Exchange (Cell 01)
        values[1] = values[1].strip('"')
        # Remove + from Last Day Change (Cell 03)

        try:
            values[3] = float(values[3])
        except (ValueError):
            values[3] = 0
            #print 'Exception: ', stock
        # Remove unit from Market Cap (Cell 06)
        temp = values[6]
        if temp[len(temp)-1] == 'B':
            temp = float(temp[0:len(temp)-2])*1000
        elif temp[len(temp)-1] == 'M':
            temp = float(temp[0:len(temp)-2])
        elif temp[len(temp)-1] == 'K':
            temp = float(temp[0:len(temp)-2])/1000
        elif temp.isdigit():
            temp = float(temp)/1000000
        values[6] = temp
        # Remove unit from EBITDA (Cell 08)
        temp = values[8]
        if temp[len(temp)-1] == 'B':
            temp = float(temp[0:len(temp)-2])*1000
        elif temp[len(temp)-1] == 'M':
            temp = float(temp[0:len(temp)-2])
        elif temp[len(temp)-1] == 'K':
            #Handle lacking decimal places
            if len(temp) == 2: 
                temp = float(temp[0:len(temp)-1])/1000
            else:
                temp = float(temp[0:len(temp)-2])/1000
        elif temp.isdigit():
            temp = float(temp)/1000000
        values[8] = temp
        #print master
        master[str(stock)] = values
        
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
    
    del master['Legend'] # remove first row of legends
    
    master = master.T
    master.to_csv(filename)
    
    print '\n'+'---------------------------------------' \
          + '-------------------------------'
    print 'MODULE: FINANCIAL DATA RETRIVAL FROM FINANCE.YAHOO.COM.'
    print 'Output: Added', str(len(ticker_list)), 'buybacks to', filename, '\n'
    print 'Retrival of financial data unsuccessful for', not_added, 'shares. \n'
    print 'Run-time:', "%.2f" %(time.time() - start_time), 'sec'
    print '---------------------------------------' \
          + '-------------------------------' + '\n'
    master = master.convert_objects(convert_numeric=True)

    return master.convert_objects(convert_numeric=True)
