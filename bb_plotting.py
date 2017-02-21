import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('figure', figsize=(12, 9))

def plot_outputs(norm_price, norm_bench, norm_bench_beta, anr, anr_beta, full_info,\
                 picked_ticker_list, rank_cutoff, rets):
    '''

    Version 1.0, MPPA @ 19:00 29.07.14

    Generate output plots
    
    '''
        
    print 'Creating plots...'
    start_time = time.time() # Start clock

    
    num_ticks = 8
    min_day = -250
    max_day = 700
    days = anr.columns.tolist()
    if days[0] > min_day: min_day = days[0]
    if days[len(days)-1] < max_day: max_day = days[len(days)-1]
    if len(picked_ticker_list) < num_ticks: num_ticks = len(picked_ticker_list)-1
    top_list = picked_ticker_list[0:num_ticks]
    n = len(full_info)

    ########################
    ### PLOT TIME SERIES ###
    ########################
    
    # Plot a selection of companies (abn. ret.)
    a = anr.T[top_list]
    a = a.ix[min_day:max_day]
    a['Days relative to buyback'] = a.index
    a.plot(x='Days relative to buyback')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4,\
               mode="expand", borderaxespad=0.)
    plt.ylabel(r'Abn. Return ($\beta=1$), BB date = 0')
    plt.savefig('Output_Plots/TS_ab_ret_plot')

    # Plot a selection of companies (share price)
    plt.figure()
    b = norm_price.T[top_list]
    b = b.ix[min_day:max_day]
    b['Days relative to buyback'] = b.index
    b.plot(x='Days relative to buyback')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4,\
               mode="expand", borderaxespad=0.)
    plt.ylabel('Normalized Share Price, BB date = 100')
    plt.savefig('Output_Plots/TS_share_price_plot')

    # Plot the cumulative
    c = pd.DataFrame(index=anr.T[top_list].ix[min_day:max_day].index)
    c[r'Tot. Abn. Ret. $\beta=1$'] = anr.T[picked_ticker_list].\
                                    T.mean().ix[min_day:max_day]
    c[r'Tot. Abn. Ret. Act. $\beta$'] = anr_beta.T[picked_ticker_list].\
                                    T.mean().ix[min_day:max_day]
    c['Mean Price'] = norm_price.T[picked_ticker_list].T.mean().\
                      ix[min_day:max_day]-100
    c['Mean Index'] = norm_bench.T[picked_ticker_list].T.mean().\
                      ix[min_day:max_day]-100
    c['Beta Adj. Index'] = norm_bench_beta.T[picked_ticker_list].T.mean().\
                      ix[min_day:max_day]-100
    c['Days relative to buyback'] = c.index
    c.plot(x='Days relative to buyback')
    plt.ylabel('% (Normalized to BB date = 0)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3,\
               mode="expand", borderaxespad=0.)
    plt.savefig('Output_Plots/TS_portfolio_plot')
    plt.close('all')

    #######################
    ### PLOT HISTOGRAMS ###
    #######################

    ### RANKING INPUTS ###
    
    # Plot MC distribution
    d = full_info['log10(MC)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(Market Cap)')
    plt.ylabel('Frequency')
    plt.title(r'Market Cap distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10MC')

    # Plot the Price to Book Ratio distribution
    d = full_info['log10(PBR)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(Price Book Ratio)')
    plt.ylabel('Frequency')
    plt.title(r'Price Book Ratio distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10PBR')

    # Plot the Previous Abn. Return distribution
    days = ['25','50','100','150','250']
    for i in days:
        d = full_info['Abn. return '+i+'d pre']*100
        plt.figure()
        d.hist(bins=80)
        plt.xlabel(r'Abnormal Return ($\beta=1$) prior to Buyback (%)')
        plt.ylabel('Frequency')
        plt.title(r'Abn. Return Distribution, '+i+\
                   ' days ($n =$ '+str(n)+')')
        plt.savefig('Output_Plots/HIST_Rank_In_abn_ret_'+i)

    # Plot the Short Ratio distribution
    d = full_info['log10(SR)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(Short Ratio)')
    plt.ylabel('Frequency')
    plt.title('Short Ratio Distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10SR')

    # Plot Beta distribution
    d=full_info['Beta']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel(r'$\beta$')
    plt.ylabel('Frequency')
    plt.title(r'$\beta$ Distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_beta')

    # Plot the Relative BB size distribution
    d = full_info['log10(BB/MC)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(BB/MC)')
    plt.ylabel('Frequency')
    plt.title(r'Relative BB Size to Market Cap distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10BB_MC')

    # Plot Adjusted MC distribution
    d = full_info['log10(AdjMC)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(Adjusted Market Cap)')
    plt.ylabel('Frequency')
    plt.title(r'Adjusted Market Cap distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10MC_adj')

    # Plot the Adjusted Price to Book Ratio distribution
    d = full_info['log10(AdjPBR)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(Adjusted Price Book Ratio)')
    plt.ylabel('Frequency')
    plt.title(r'Adjusted Price Book Ratio distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10PBR_adj')

    # Plot the Adjusted Relative BB size distribution
    d = full_info['log10(BB/AdjMC)']
    plt.figure()
    d.hist(bins=80)
    plt.xlabel('log10(BB/Adj.MC)')
    plt.ylabel('Frequency')
    plt.title(r'Relative BB Size to Adjusted Market Cap distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_In_log10BB_MC_adj')

    ### RANKING OUTPUTS ###
    
    # Plot the Ranking distribution
    d=full_info['Total Rank']
    plt.figure()
    d.hist(bins=80)
    plt.vlines(rank_cutoff,0,plt.ylim()[1], colors='r', \
               linestyles='dashed', label='Cutoff')
    plt.xlabel(r'Ranking')
    plt.ylabel('Frequency')
    plt.title(r'Ranking Distribtion Distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Rank_Out_total')

    ### OTHER INFO ###

    # Plot the Post Abn. Return distribution
    d=full_info['Abn. Return post']*100
    plt.figure()
    d.hist(bins=80)
    plt.xlabel(r'Abnormal Return ($\beta=1$), post Buyback (%)')
    plt.ylabel('Frequency')
    plt.title(r'Abn. Return Distribution post announcement ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Other_abn_ret_post')

    # Plot the Previous Abn. Return distribution
    d=full_info['Dividend Yield (%)']*100
    plt.figure()
    d.hist(bins=80)
    plt.xlabel(r'Dividend Yield (%)')
    plt.ylabel('Frequency')
    plt.title(r'Dividend Yield Distribution ($n =$ '+str(n)+')')
    plt.savefig('Output_Plots/HIST_Other_div_yield')

    plt.close('all')
    
    #####################
    ### PLOT SCATTERS ###
    #####################

    # Plot the Previous Abn. Return distribution
    a = rets[rets['B/S']<0]
    plt.figure()
    plt.scatter(a['Return'],a['Total Rank'])
    plt.grid(True)
    plt.ylabel(r'Ranking')
    plt.xlabel(r'Return (%)')
    plt.title(r'Return versus Total Ranking ($n =$ '+str(len(a))+')')
    plt.savefig('Output_Plots/SCATTER_return_vs_rank')
    
    ##########################
    ### FINALIZE AND CLOSE ###
    ##########################
    
    plt.close('all')
    print '-> Processing time:', "%.2f" %(time.time() - start_time), 'sec\n'
