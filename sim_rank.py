import bb_calc as bb_c
import bb_load as bb_l
import time
import numpy as np
import math
import pandas as pd
import datetime

def simulate_rank(data, iterations):
    '''

    Version 2.0: MPPA @ 12:30 09.07.14
    
    Perform ranking simulations of the input data set <data>.
    Iterate the simulation with random variables <iterations> times.
    
    '''

    ###### SETTINGS ######
    # Print-out and output parameters
    first_time_est = 200
    print_freq = 2000 # Define how often to print out progress
    reorder_freq = 2000 # Define how often to cut the output
    cut_lim = 1000 # Define the number of simulations to keep in dataframe

    # Simulation parameters
    min_ticks = 25 # Define the min number of tickers to keep in dataframe
    rank_switch = [False, # MC
                   False, # PBR
                   False, # Abn25d
                   True, # Abn50d
                   False, # Abn100d
                   True, # Abn150d
                   False, # Abn250d
                   False, # SR
                   False, # Beta
                   False, # BB/MC
                   True, # AdjMC
                   True, # AdjPBR
                   True] # AbdjBB/MC

    # Return computation parameters
    delay_days = 14 # Define the number of days from BB and to buy
    hold_years = 3 # Define the number of yeas held after buy

    ############

    # Define dataframe for output
    sim_parameters = ['Abn. Ret.',\
                      'Return',\
                      'Bench Ret.',\
                      '#Ticks',\
                      'Cutoff',\
                      'Tot. Weight',\
                      'Max Rank',\
                      'Min Rank',\
                      'Mean Rank',\
                      'Median Rank',\
                      'Rank Std. Dev.',\
                      'Selected Tickers']  
    
    init_rank_names = ['MC Rank', \
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

    init_rank_dim = ['log10(MC)', \
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
    
    # Format: [Low, High, Step]
    init_rank_weight_lim = [[0,1,0.2], #  MC
                            [0,1,0.2], #  PBR
                            [0,1,0.2], #  Abn25d
                            [0,1,0.2], #  Abn50d
                            [0,1,0.2], #  Abn100d
                            [0,1,0.2], #  Abn150d
                            [0,1,0.2], #  Abn250d
                            [0,1,0.2], #  SR
                            [0,1,0.2], #  Beta
                            [0,1,0.2], #  BB/MC
                            [0,1,0.2], #  AdjMC
                            [0,1,0.2], #  AdjPBR
                            [0,1,0.2]] #  AdjBB/MC

    # Format: [[Bot_Low, Bot_High],[Top_Low, Top_High], Step]
    init_rank_bounds_lim = [[[10.4,11.7],[8,9.5],0.135], #        MC
                       [[0.85,1.55],[-0.35,0.35],0.072], #   PBR
                       [[0.03,0.18],[-0.24,-0.08],0.015], # Abn25d
                       [[0.05,0.25],[-0.24,-0.06],0.018], # Abn50d
                       [[0.1,0.4],[-0.4,-0.1],0.03], #     Abn100d
                       [[0.12,0.48],[-0.48,-0.12],0.036], # Abn150d
                       [[0.25,0.75],[-0.65,-0.15],0.054], # Abn250d
                       [[-0.15,0.45],[0.85,1.45],0.06], #  SR
                       [[1,1.6],[0,0.6],0.06], #           Beta
                       [[-3.6,-2.4],[-1.5,-0.3],0.126], #   BB/MC
                       [[10.45,12.55],[6.95,9.05],0.21], #  AdjMC
                       [[1.31,2.69],[-1,0.4],0.138], #      AdjPBR
                       [[-3.25,-1.75],[-0.75,0.75],0.15]] #AdjBB/MC

    # Define initial rank bounds weight and cutoff (as in main)
    init_rank_bounds = [[11,8.75], #     MC
                   [1.2,0], #       PBR
                   [0.1,-0.15], #   Abn25d
                   [0.15,-0.15], #  Abn50d
                   [0.25,-0.25], #  Abn100d
                   [0.3,-0.3], #    Abn150d
                   [0.5,-0.4], #    Abn250d
                   [0.15,1.15], #   SR
                   [1.3,0.3], #     Beta
                   [-3,-0.9], #     BB/MC
                   [11.5,8], #      AdjMC
                   [2,-0.3], #      AdjPBR
                   [-2.5,0]] #      AdhBB/MC
    
    init_rank_weight = [1, #   MC
                        1, #   PBR
                        0.5, # Abn25d
                        0.3, # Abn50d
                        0.3, # Abn100d
                        0.2, # Abn150d
                        0.2, # Abn250d
                        1, #   SR
                        1, #   Beta
                        1, #   BB/MC
                        0.2, # AdjMC
                        0.2, # AdjPBR
                        0.2] # AbdjBB/MC

    init_sim_parameters = ['MC',\
                           'PBR',\
                           'Ab25',\
                           'Ab50',\
                           'Ab100',\
                           'Ab150',\
                           'Ab250',\
                           'SR',\
                           'Beta',\
                           'BB\MC',\
                           'AdjMC',\
                           'AdjPBR',\
                           'AdjBB\MC']

    # Build the selected ranking dimensions
    rank_names = []
    rank_dim = []
    rank_weight_lim = []
    rank_bounds_lim = []
    rank_bounds = []
    rank_weight = []

    for i in range(len(rank_switch)):
        if rank_switch[i]:
            rank_names.append(init_rank_names[i])
            rank_dim.append(init_rank_dim[i])
            rank_weight_lim.append(init_rank_weight_lim[i])
            rank_bounds_lim.append(init_rank_bounds_lim[i])
            rank_bounds.append(init_rank_bounds[i])
            rank_weight.append(init_rank_weight[i])
            sim_parameters.append(init_sim_parameters[i]+' Wght')
            sim_parameters.append(init_sim_parameters[i]+' Bot')
            sim_parameters.append(init_sim_parameters[i]+' Top')
    
    # Format: [Low, High, Step]
    cutoff_lim = [0.65,0.95,0.02]
    # Initial value
    rank_cutoff = 0.75                 

    # Compute upper and lower limits as multiple of step
    u=[]
    l=[]
    for i in range(len(rank_dim)):
        u_t = []
        l_t = []
        l_t.append(int(rank_weight_lim[i][0]/rank_weight_lim[i][2]))
        u_t.append(int(rank_weight_lim[i][1]/rank_weight_lim[i][2]))
        l_t.append(int(rank_bounds_lim[i][0][0]/rank_bounds_lim[i][2]))
        u_t.append(int(rank_bounds_lim[i][0][1]/rank_bounds_lim[i][2]))
        l_t.append(int(rank_bounds_lim[i][1][0]/rank_bounds_lim[i][2]))
        u_t.append(int(rank_bounds_lim[i][1][1]/rank_bounds_lim[i][2]))
        u.append(u_t)
        l.append(l_t)
    lc = int(cutoff_lim[0]/cutoff_lim[2])
    uc = int(cutoff_lim[1]/cutoff_lim[2])

    # Get ticker_list and load prices. Read BB announcement dates
    ticker_list = data.index
    prices = bb_l.load_price_df(ticker_list)
    bench = bb_l.load_benchmark_df()
    bb_d = data['Buyback Date']

    # Declare simulation output dataframe
    sim_result = pd.DataFrame(columns=sim_parameters)
    
    # Start clock and initial output
    print '$$$$$ -----------------------------------------------'
    print '$$$$$ Simulating '+str(iterations)+ ' rankings...'
    start_date = datetime.datetime.now()
    start_time = time.time()
    print '$$$$$ Start time:         ' + \
                  start_date.strftime("%H:%M, %B %d, %Y")

    # Main iteration loop
    for k in range(iterations):
        # Print first time estimation
        if k == first_time_est:
            el_time = time.time() - start_time
            iter_time = el_time/float(k)
            rem_time = (iterations-k)*iter_time
            tot_time = el_time + rem_time
            tot_h = math.floor(tot_time/3600)
            tot_m = math.floor((tot_time-tot_h*3600)/60)
            tot_s = tot_time-tot_h*3600-tot_m*60
            t=datetime.timedelta(hours=tot_h,minutes=tot_m,seconds=int(tot_s))
            fin_date = start_date + t
            print '$$$$$ Estimated finish:     ' + \
                  fin_date.strftime("%H:%M, %B %d, %Y")
            print '$$$$$ Estimated total time: ' +\
                  "%2.0f" %(tot_h)+'h '+"%2.0f" %(tot_m)+'m '+\
                  "%2.2f" %(tot_s)+'s'
            print '$$$$$ Time per iteration:   ' + \
                  "%2.4f" %(iter_time)+' sec'
            print '$$$$$ '
        # Print progress
        if float(k)/print_freq -round(float(k)/print_freq)==0:
            if k>0:
                prog = float(k)*100/float(iterations)
                print '$$$$$ '+str(k)+' iterations completed'
                print '$$$$$ Simation progress:   '+"%.2f"%(prog)+'%'
                el_time = time.time() - start_time
                iter_time = el_time/float(k)
                elt_h = math.floor(el_time/3600)
                elt_m = math.floor((el_time-elt_h*3600)/60)
                elt_s = el_time-elt_h*3600-elt_m*60
                print '$$$$$ Elapsed time:        '+\
                      "%3.0f" %(elt_h)+'h '+"%2.0f" %(elt_m)+'m '\
                      +"%2.2f" %(elt_s)+'s'
                rem_time = (iterations-k)*iter_time
                rem_h = math.floor(rem_time/3600)
                rem_m = math.floor((rem_time-rem_h*3600)/60)
                rem_s = rem_time-rem_h*3600-rem_m*60
                tot_time = el_time + rem_time
                tot_h = math.floor(tot_time/3600)
                tot_m = math.floor((tot_time-tot_h*3600)/60)
                tot_s = tot_time-tot_h*3600-tot_m*60
                print '$$$$$ Est. total time:     '+\
                      "%3.0f" %(tot_h)+'h '+"%2.0f" %(tot_m)+'m '\
                      +"%2.2f" %(tot_s)+'s'
                print '$$$$$ Est. time remaining: '+\
                      "%3.0f" %(rem_h)+'h '+"%2.0f" %(rem_m)+'m '\
                      +"%2.2f" %(rem_s)+'s'
                t=datetime.timedelta(hours=tot_h,minutes=tot_m,\
                                     seconds=int(tot_s))
                fin_date = start_date + t
                print '$$$$$ Updated est. finish: ' + \
                      fin_date.strftime("%H:%M, %B %d, %Y")
                print '$$$$$ Time per iteration:  ' + \
                      "%2.4f" %(iter_time)+' sec'
                print '$$$$$ '
        
        # Compute rankings
        tot_rank = pd.Series(data=[0]*len(data), index=data.index)
        tot_weight = 0
        for i in range(len(rank_dim)):
            data[rank_names[i]] = bb_c.rank(data[rank_dim[i]], \
                                                 rank_bounds[i][0], \
                                                 rank_bounds[i][1])
            tot_rank = tot_rank + rank_weight[i]*data[rank_names[i]]
            tot_weight = tot_weight + rank_weight[i]

        tr = tot_rank/tot_weight

        # Take away all stocks with ranking below cutoff
        picked_ticker_list = tr[tr > rank_cutoff].\
                             index.values.tolist()
        num_tick = len(picked_ticker_list)
        
        
        # Compute returns if above ticker threshold
        if num_tick >= min_ticks:
            # Compute returns
            
            ret = bb_c.quick_ret_calc(prices.T[picked_ticker_list].T, bench, \
                                      bb_d[picked_ticker_list].tolist(), \
                                      delay_days, hold_years)
            # Compute rank properties
            mx = tr.max()
            mi = tr.min()
            me = tr.mean()
            md = tr.median()
            std = tr.std()

            # Include string of tickers
            ticks = ''
            for i in picked_ticker_list: ticks = ticks + i + ' '

            # Write result to dataframe
            wrt = [ret[0], ret[1], ret[2], num_tick, float(rank_cutoff), \
                   tot_weight, mx, mi, me, md, std, ticks]
            for i in range(len(rank_dim)):
                wrt.append(float(rank_weight[i]))
                wrt.append(float(rank_bounds[i][0]))
                wrt.append(float(rank_bounds[i][1]))
            sim_result.loc[k] = wrt

        # Generate random numbers for next iteration
        for i in range(len(rank_dim)):
            rank_weight[i] = float(np.random.randint(l[i][0],u[i][0]+1))\
                             *rank_weight_lim[i][2]
            rank_bounds[i][0] = float(np.random.randint(l[i][1],u[i][1]+1))\
                             *rank_bounds_lim[i][2]
            rank_bounds[i][1] = float(np.random.randint(l[i][2],u[i][2]+1))\
                             *rank_bounds_lim[i][2]
            # Remove chance of similar top and bottom bound
            if rank_bounds[i][0] == rank_bounds[i][1]:
                rank_bounds[i][1] = rank_bounds[i][0] + rank_bounds_lim[i][2]

        rank_cutoff = float(np.random.randint(lc,uc))*cutoff_lim[2]

        if float(k)/reorder_freq -round(float(k)/reorder_freq)==0:
            if k>0:
                sim_result = sim_result.\
                             sort('Abn. Ret.',ascending=False)
                if len(sim_result) > cut_lim:
                    sim_result = sim_result[1:cut_lim]

    # Sort according to return
    sim_result = sim_result.sort('Abn. Ret.',ascending=False)
    if len(sim_result) > cut_lim:
        sim_result = sim_result[1:cut_lim]

    tot_time = time.time() - start_time
    iter_time = tot_time/float(iterations)
    tot_h = math.floor(tot_time/3600)
    tot_m = math.floor((tot_time-tot_h*3600)/60)
    tot_s = tot_time-tot_h*3600-tot_m*60
    print '$$$$$ Total simulation time: '+\
          "%2.0f" %(tot_h)+'h '+"%2.0f" %(tot_m)+'m '\
          +"%2.2f" %(tot_s)+'s'
    print '$$$$$ Time per iteration:    ' + \
                      "%2.4f" %(iter_time)+' sec'
    print '$$$$$ -----------------------------------------------'

    filename = 'Simulations\sim_result_' + \
               start_date.strftime("%y-%m-%d_%H%M") + \
               '_n=' + str(iterations) + '.csv'
    sim_result.to_csv(filename)        
    return sim_result

def load_stats():

    '''

    Version 1.0: MPPA @ 17:45 08.07.14
    
    ( ) -> dataframe.
    
    '''

    df = pd.read_csv('full_info.csv')
    df.index = df['Unnamed: 0'].tolist()
    df = df.T[1:].T
    return df.convert_objects(convert_numeric=True)

def write_stats(data):

    '''

    Version 1.0: MPPA @ 17:45 08.07.14
    
    (dataframe) -> write to file.
    
    '''

    data.to_csv('full_info.csv')
