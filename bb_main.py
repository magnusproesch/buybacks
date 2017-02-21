'''

Version 3.1, MPPA @ 10:50 02.06.14 

'''

############## Test Databases and update if necessary/wanted ##############
import time
fundamental_time = time.time() # Start clock

print '\n   ########################################################'
print '   #####                    BUYBACK                    ####'
print '   #####               Magnus S. Proesch               ####'
print '   #####              Matthias P.P. Amble              ####'
print '   #####                    (C)2016                    ####'
print '   ########################################################\n'

print 'Loading libraries...'

import bb_update_database as bb_u
import bb_load as bb_l
import bb_filt as bb_f
import bb_calc as bb_c
import bb_time_shift as bb_ts
import bb_plotting as bb_p

import sim_rank as s_r

import pandas as pd
from pandas_datareader import data
from pandas import DataFrame, read_csv
import datetime
import numpy as np

print '-> Processing time:', "%.2f" %(time.time() - fundamental_time), 'sec\n'

#Prompt time range for analysis
'''
time_beg = str(raw_input('From what date do you want to analyse buybacks?'\
                           + '\n' + 'Input date (yyyy-mm-dd): '))
time_end = str(raw_input('To what date do you want to analyse buybacks?'\
                           + '\n' + 'Input date (yyyy-mm-dd): '))
'''
################################################
# Hard coded to avoid prompting during testing #
################################################
time_beg = -1
time_end = time.strftime("%Y-%m-%d") # Today's date
################################################

# Set argument to False if no prompt is desired
bb_u.bb_update_database(True)

############## START PROCESSING ##############

# Initial ticker filtering
ticker_list = bb_l.load_ticker_list(time_beg, time_end)
print 'Perform initial ticker filtering...'
init_ticks = len(ticker_list)
ticker_list = bb_f.filt_ticker_list(ticker_list,100000,True)
print '-> Number of tickers reduced from '+str(init_ticks)+\
      ' to '+str(len(ticker_list))+'\n'


# Remove most recent BB announcements
'''
weeks_filt = int(raw_input('Input desired min. number of weeks '\
                           +'of return after buyback announcements: '))
'''
################################################
# Hard coded to avoid prompting during testing #
# Set to = 0 when you want to include all BBs  #
################################################

weeks_filt = 0

# Her bytter ticker_list fra scrape_database til financials csv

# First fetch ticker list from prices.csv
df_P = read_csv('prices.csv')
full_ticker_dfP = df_P['Unnamed: 0']
full_ticker_P = full_ticker_dfP.tolist()
full_ticker_P.pop(0)

# Then fetch from financials.csv
df_F = read_csv('prices.csv')
full_ticker_dfF = df_F['Unnamed: 0']
full_ticker_F = full_ticker_dfF.tolist()
full_ticker_F.pop(0)

# Then chose the shortest list
if len(full_ticker_P) > len(full_ticker_F):
    ticker_list = full_ticker_F  
else:
    ticker_list = full_ticker_P

# Then filter the ticker list
ticker_list = bb_f.filt_tickers_time_since_bb(ticker_list, weeks_filt)

'''
print '-> Number of tickers reduced further to '+str(len(ticker_list))+'\n'
'''

print 'Computing other statistics...'
start_time = time.time() # Start clock
#full_info = s_r.load_stats()
full_info = bb_c.stats_calc(ticker_list)
print '-> Calculation time:', "%.2f" %(time.time() - start_time), 'sec\n'

# Write historical financial data
### TO COME

# Compute rankings
start_time = time.time() # Start clock
print 'Computing rankings...'
'''
rank_names = ['MC Rank', \
              'PBR Rank', \
              'Abn. Ret Rank 25d', \
              'Abn. Ret Rank 50d', \
              'Abn. Ret Rank 100d', \
              'Abn. Ret Rank 150d', \
              'Abn. Ret Rank 250d', \
              'Short Ratio Rank', \
              'Beta Rank', \
              'BB Size Rank',\
              'Adj. MC Rank', \
              'Adj. PBR Rank', \
              'Adj. BB Size Rank']

rank_dim = ['log10(MC)', \
            'log10(PBR)', \
            'Abn. return 25d pre', \
            'Abn. return 50d pre', \
            'Abn. return 100d pre', \
            'Abn. return 150d pre', \
            'Abn. return 250d pre', \
            'log10(SR)', \
            'Beta',\
            'log10(BB/MC)',\
            'log10(AdjMC)', \
            'log10(AdjPBR)', \
            'log10(BB/AdjMC)']

rank_weight = [1, \
               1, \
               0, \
               0, \
               1, \
               0, \
               0, \
               0, \
               0, \
               0, \
               0, \
               0, \
               1]

rank_bounds = [[11,8.75],\
               [1.2,0],\
               [0.1,-0.15],\
               [0.15,-0.15],\
               [0.25,-0.25],\
               [0.3,-0.3],\
               [0.5,-0.4],\
               [0.15,1.15],\
               [1.3,0.3],\
               [-3,-0.9],\
               [11.5,8],\
               [2,-0.3],\
               [-2.5,-0]]
'''

rank_names = ['Abn. Ret Rank 100d',\
              'PBR Rank',\
              'Adj. MC Rank',\
              'Adj. BB Size Rank']

rank_dim = ['Abn. return 100d pre',\
            'log10(PBR)',\
            'log10(AdjMC)',\
            'log10(BB/AdjMC)']

rank_weight = [1.5, \
               1.0, \
               1.5,\
               1.0]

rank_bounds = [[0.25,-0.25],\
               [1.2,0],\
               [11.5,8],\
               [-2.5,-0]]

tot_rank = pd.Series(data=[0]*len(full_info), index=full_info.index)
tot_weight = 0
for k in range(len(rank_dim)):
    full_info[rank_names[k]] = bb_c.rank(full_info[rank_dim[k]], \
                                         rank_bounds[k][0], \
                                         rank_bounds[k][1])
    tot_rank = tot_rank + rank_weight[k]*full_info[rank_names[k]]
    tot_weight = tot_weight + rank_weight[k]
full_info['Total Rank'] = tot_rank/tot_weight

print '-> Calculation time:', "%.2f" %(time.time() - start_time), 'sec\n'

# Take away all stocks with ranking below cutoff
rank_cutoff = 0.75
picked_ticker_list = full_info[full_info['Total Rank'] > rank_cutoff].\
                     index.values.tolist()
print 'Remove tickers with ranking below '+str(rank_cutoff)+'...'
print '-> Number of tickers reduced to '+str(len(picked_ticker_list))+'\n'


############## EVALUATE RESULTS ##############

### Shift time ###
if len(picked_ticker_list) != 0:
    
    print 'Time shifting prices for the picked ticker list...'
    start_time = time.time() # Start clock
    print picked_ticker_list
    norm_price = bb_ts.time_shift_norm_prices(picked_ticker_list)
    print '-> Calculation time:', "%.2f" %(time.time() - start_time), 'sec\n'

    print 'Time shifting benchmark...'
    start_time = time.time() # Start clock
    print '-> Selected benchmark for abn. return calculation: ', \
          bb_l.load_benchmark_name()
    norm_bench = bb_ts.time_shift_norm_benchmark(picked_ticker_list)
    norm_bench_beta=(norm_bench-100).mul(full_info['Beta'][picked_ticker_list], axis=0)+100
    print '-> Calculation time:', "%.2f" %(time.time() - start_time), 'sec\n'

    ### Compute returns ###
    print 'Computing returns...'
    start_time = time.time() # Start clock
    anr = bb_ts.time_shifted_abn_ret(picked_ticker_list)
    anr_beta = bb_ts.time_shifted_abn_ret(picked_ticker_list, \
                                          full_info['Beta'][picked_ticker_list].\
                                          tolist())
    num_days = anr.T[picked_ticker_list].T.mean().tail(1).index.tolist().pop()
    print '-> Abn. return from buyback date ('+str(num_days)+\
          ' days, actual beta for all stocks): '+\
          "%.2f" %anr_beta.T[picked_ticker_list].T.mean().tail(1).tolist().pop()+'%'
    print '-> Abn. return from buyback date ('+str(num_days)+\
          ' days, Beta = 1 for all stocks):    '+\
          "%.2f" %anr.T[picked_ticker_list].T.mean().tail(1).tolist().pop()+'%'
    print '-> Calculation time:', "%.2f" %(time.time() - start_time), 'sec\n'

    ### Compute returns ###
    print 'Computing portfolio returns...'
    del_days = 14
    hold_years = 3
    start_time = time.time() # Start clock
    rets = bb_c.ret_calc(picked_ticker_list,\
                         full_info['Buyback Date'][picked_ticker_list].tolist(),\
                         del_days, hold_years)
    rets['Total Rank'] = full_info['Total Rank'][picked_ticker_list]
    rets.loc['Total','Total Rank'] = rets[rets['B/S']==-1]['Total Rank'].mean()
    print '-> Calculation time:', "%.2f" %(time.time() - start_time), 'sec\n'

    ### Create Plots ###
    #bb_p.plot_outputs(norm_price, norm_bench, norm_bench_beta, anr, anr_beta, \
                   # full_info, picked_ticker_list, rank_cutoff, rets)

    ### Write output dataframe ###
    s_r.write_stats(full_info)

    ### Print out important results in shell ###
    print_no = 30
    print 'Rankings of the '+str(print_no)+' most recent buybacks:'
    print full_info.sort_values(by = 'Buyback Date',ascending=False)\
          [['Buyback Date','Total Rank','Abn. Return post']].head(print_no)

    print '\n'+'Top '+str(print_no)+' Rankings:'
    print full_info[full_info['Total Rank'] > 0].\
          sort_values(by = 'Total Rank',ascending=False)\
          [['Buyback Date','Total Rank','Abn. Return post']].head(print_no)

    print '\n'+'Top '+str(print_no)+' performing tickers (ex post):'
    print full_info[full_info['Abn. Return post'] > 0].\
          sort_values( by = 'Abn. Return post',ascending=False)\
          [['Buyback Date','Total Rank','Abn. Return post']].head(print_no)

    print '\n'+'Selected stocks:'
    print rets[rets['B/S']<1].sort_values(by = ['Date'], ascending = False)

    #Pausing for input
    further = ()
    further = str(raw_input('\nDo you want additional information on the picked list? y/n: '))

    if further == 'y':
        
        print '\n'+'Further details on selected stocks:'
        selection = []
        selection = full_info.loc[picked_ticker_list].transpose().drop(['Stock Exchange',\
                                                        'Last Day Change (%)',\
                                                        'Last Day Volume',\
                                                        'Average Daily Volume',\
                                                        'Last available share price',\
                                                        'log10(SR)',\
                                                        'log10(MC)',\
                                                        'log10(PBR)',\
                                                        'log10(BB/MC)',\
                                                        'BB / MC',\
                                                        'log10(AdjMC)',\
                                                        'log10(AdjPBR)',\
                                                        'log10(BB/AdjMC)',\
    #                                                   'Abn. Ret Rank 50d',\
                                                        'Abn. Ret Rank 100d'])
    #                                                   'Abn. Ret Rank 250d'])\
                                                                        

        print selection

    print_recommendation = ()
    print_recommendation = str(raw_input('\nDo you want to print the data on '\
                                         'the selected stocks? y/n: '))
    #Pausing for input
    if print_recommendation == 'y':
        file_name_rec = str(datetime.datetime.now().isoformat())[:10]+'.csv'
        selection.to_csv(file_name_rec)

else:
    print '\n No ticker was selected \n'
    print_no = 30

    print '\n'+'Top '+str(print_no)+' Rankings:'
    print full_info[full_info['Total Rank'] > 0].\
          sort_values(by = 'Total Rank',ascending=False)\
          [['Buyback Date','Total Rank','Abn. Return post']].head(print_no)

    print '\n'+'Rankings of the '+str(print_no)+' most recent buybacks:'
    print full_info.sort_values(by = 'Buyback Date',ascending=False)\
          [['Buyback Date','Total Rank','Abn. Return post']].head(print_no)

print '\n--------------------------------------'
print '      Total Run Time:', "%.2f" %(time.time() - fundamental_time), 'sec'
print '--------------------------------------\n'
