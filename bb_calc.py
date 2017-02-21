import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np
import bb_time_shift as bb_ts
import bb_group as bb_g
import bb_load as bb_l
from dateutil.relativedelta import relativedelta

def stats_calc(ticker_list):
    '''

    Version 2.0, MPPA @ 19:00 29.07.14

    Compute various stats used for ranking
    
    '''
      
    # Load Data
    bb = bb_g.group_bb_df(-1,-1)
    p_port = bb_l.load_price_df(ticker_list)
    p_benc = bb_l.load_benchmark_df()
    bb_dates = bb[ticker_list].T['Date'].tolist()
    bb_am = bb[ticker_list].T['Amount']
    bb_oc = bb[ticker_list].T['No. of BB announ.'].tolist()

    
    bench_bb_date = bb_ts.time_shift_benchmark(ticker_list)[:][0]
    price_bb_date = bb_ts.time_shift_prices(ticker_list)[:][0]
    bench_last = float(p_benc.iloc[len(p_benc)-1])
    price_last = p_port.T.iloc[len(p_port.T)-1]

    
    fin = bb_l.load_fin_dat_df(ticker_list)
    sr = fin['Short Ratio']
    cur_pb = fin['Price Book Ratio']
    cur_mcap = fin['Market Cap (M)']
    cur_mc = cur_mcap*1000000
    
    # Compute returns
    ret_pre_25d = pre_ret_calc(ticker_list,25) 
    ret_pre_50d = pre_ret_calc(ticker_list,50)
    ret_pre_100d = pre_ret_calc(ticker_list,100)
    ret_pre_150d = pre_ret_calc(ticker_list,150)
    ret_pre_250d = pre_ret_calc(ticker_list,250)
    abn_ret_pre_25d = pre_abn_ret_calc(ticker_list,25)
    abn_ret_pre_50d = pre_abn_ret_calc(ticker_list,50)
    abn_ret_pre_100d = pre_abn_ret_calc(ticker_list,100)
    abn_ret_pre_150d = pre_abn_ret_calc(ticker_list,150)
    abn_ret_pre_250d = pre_abn_ret_calc(ticker_list,250)
    
    # Calculate standard deviations for beta calculations
    stdev_bench = p_benc.T.pct_change().std()
    stdev = p_port.T.pct_change().std()
    
    beta_list = []
    bb_price = []
    current_price = []
    abn_ret_post = []
    ret_post = []
    
    for ticker in ticker_list:
        cov = p_port.T[ticker].pct_change().cov(p_benc.pct_change())
        beta_list.append(cov/(stdev_bench*stdev_bench))
        bb_price.append(float(price_bb_date[ticker]))
        current_price.append(float(price_last[ticker]))
        ret = float(price_last[ticker])/float(price_bb_date[ticker]) - 1
        b_ret = bench_last/float(bench_bb_date[ticker]) - 1
        ret_post.append(ret)
        abn_ret_post.append(ret - b_ret)

    # Generate series of post return and post abn. return
    ret_series = pd.Series(ret_post,index=ticker_list)
    abn_ret_series = pd.Series(ret_post,index=ticker_list)
    
    # Compute adjusted MC and PBR
    adj_mcap = cur_mcap/(1-ret_series)
    adj_mc = adj_mcap*1000000
    adj_pb = cur_pb/(1-abn_ret_series)

    # Compute relative BB size with adjusted MC
    rel_bb_size_c = bb_am/cur_mcap
    rel_bb_size_a = bb_am/adj_mcap
    rel_bb_size_c = rel_bb_size_c.tolist()
    rel_bb_size_a = rel_bb_size_a.tolist()
    # Compute Log of MC
    mc_c_l = cur_mc.tolist()
    logmc_c_l = np.log10(mc_c_l)
    mc_a_l = adj_mc.tolist()
    logmc_a_l = np.log10(mc_a_l)
    # Compute Log of PBR
    pb_c_l = cur_pb.tolist()
    logpb_c_l = np.log10(pb_c_l)
    pb_a_l = adj_pb.tolist()
    logpb_a_l = np.log10(pb_a_l)
    # Compute Log of BB/MC
    logrelbb_c = np.log10(rel_bb_size_c)
    logrelbb_a = np.log10(rel_bb_size_a)
    # Compute Log of SR
    sr_l=sr.tolist()
    logsr_l=np.log10(sr_l)
                        
    # Merge data
    stats = zip(adj_mcap.tolist(),\
                stdev.tolist(),\
                beta_list,\
                bb_dates,\
                bb_am.tolist(),\
                bb_oc,\
                bb_price,\
                current_price, \
                logsr_l,\
                rel_bb_size_c,\
                logmc_c_l,\
                logpb_c_l,\
                logrelbb_c,\
                rel_bb_size_a,\
                logmc_a_l,\
                logpb_a_l,\
                logrelbb_a,\
                ret_post, \
                abn_ret_post, \
                ret_pre_25d,\
                ret_pre_50d, \
                ret_pre_100d, \
                ret_pre_150d,\
                ret_pre_250d,\
                abn_ret_pre_25d,\
                abn_ret_pre_50d, \
                abn_ret_pre_100d,\
                abn_ret_pre_150d,\
                abn_ret_pre_250d)

    stats_df = pd.DataFrame(data = stats, index = ticker_list, \
                              columns = ['Adj.MC (M)',\
                                         'Std. Dev.',\
                                         'Beta',\
                                         'Buyback Date',\
                                         'Buyback Amount',\
                                         'No. of BB Announcements',\
                                         'Share price at BB date',\
                                         'Last available share price',\
                                         'log10(SR)',\
                                         'BB / MC',\
                                         'log10(MC)',\
                                         'log10(PBR)',\
                                         'log10(BB/MC)',\
                                         'BB / AdjMC',\
                                         'log10(AdjMC)',\
                                         'log10(AdjPBR)',\
                                         'log10(BB/AdjMC)',\
                                         'Return post',\
                                         'Abn. Return post',\
                                         'Return 25d pre',\
                                         'Return 50d pre',\
                                         'Return 100d pre',\
                                         'Return 150d pre',\
                                         'Return 250d pre',\
                                         'Abn. return 25d pre',\
                                         'Abn. return 50d pre',\
                                         'Abn. return 100d pre',\
                                         'Abn. return 150d pre',\
                                         'Abn. return 250d pre',\
                                         ]) 

    full_info = pd.concat([fin, stats_df], axis=1)
    return full_info


def pre_ret_calc(ticker_list,days):
    '''

    Version 1.0, MPPA @ 18:55 23.06.14

    Compute share price return for <days> trading days prior to buyback
    
    '''
    price = bb_ts.time_shift_prices(ticker_list)
    price_bb_date = price[:][0]
    first_day = -price.columns[0] 
    if days <= first_day:
        price_pre = price[:][(-days)]
    else:
        price_pre = price[:][(-first_day)]
    retn = price_bb_date/price_pre-1
    return retn.tolist()


def pre_abn_ret_calc(ticker_list,days):
    '''

    Version 1.0, MPPA @ 18:55 23.06.14

    Compute share price abn. return for <days> trading days prior to buyback
    Assume all betas = 1
    
    '''
    bench = bb_ts.time_shift_benchmark(ticker_list)
    price = bb_ts.time_shift_prices(ticker_list)
    bench_bb_date = bench[:][0]
    price_bb_date = price[:][0]
    first_day = -price.columns[0] 
    if days <= first_day:
        bench_pre = bench[:][(-days)]
        price_pre = price[:][(-days)]
    else:
        bench_pre = bench[:][(-first_day)]
        price_pre = price[:][(-first_day)]
    retn_p = price_bb_date/price_pre-1
    retn_b = bench_bb_date/bench_pre-1
    retn = retn_p - retn_b
    return retn.tolist()


def rank(input_series, bot_val, top_val):
    '''

    Version 1.0, MPPA @ 00:45 08.07.2014

    Generate a ranking for the imput Series with bot_val corresponing to 0.167
    and top_val corresponding to 0.833. Value of rank is capped at 0 and 1.
    '''
    ticker_list = input_series.index.tolist()
    top_rank = 5
    bot_rank = 1
    coef = float((top_rank-bot_rank)/(top_val - bot_val))
    offset = float(bot_rank - coef*bot_val)
    ranks = []
    max_rank = top_rank + 1
    min_rank = bot_rank - 1

    for ticker in ticker_list:
        para = input_series[ticker]
        out = float(coef*para + offset)
        # Cap Ranking
        if out<min_rank:
            out = min_rank
        elif out>max_rank:
            out = max_rank
        # Set to minimum if NaN
        if out != out:
            out = min_rank
        # Normalize
        out = out / max_rank
        ranks.append(out)

    rank = pd.Series(data = ranks, index = ticker_list)
    return rank

def ret_calc(ticker_list, bb_dates, delay_days, hold_years):
    '''
    Version 1.0, MPPA @ 21:00 29.07.2014

    Compute the returns of a set of tickers
    '''
    prices = bb_l.load_price_df(ticker_list)
    bench_p = bb_l.load_benchmark_df()

    num_ticks = len(ticker_list)
    
    price_dates = prices.T.index.tolist()
    max_date = price_dates[len(price_dates)-1]
    min_date = price_dates[0]
    
    buy_del = relativedelta(days=delay_days)
    sel_del = relativedelta(days=delay_days,years=hold_years)
    one_day = relativedelta(days=1)
    
    trans_dates = []
    port_num = []
    stock = []
    returns = []
    bench_ret = []
    trans_prices = []
    
    for i in range(num_ticks):
        ticker = ticker_list[i]
        bb_date = pd.to_datetime(bb_dates[i])
        buy_date = bb_date + buy_del
        sel_date = bb_date + sel_del
        buy_date = buy_date.strftime("%Y-%m-%d")
        sel_date = sel_date.strftime("%Y-%m-%d")

        while buy_date not in price_dates:
            if buy_date > max_date:
                buy_date = max_date
                break # Abort if after price data
            if buy_date < min_date:
                buy_date = min_date
                break # Abort if more recent than price data
            buy_date = pd.to_datetime(buy_date)
            buy_date = buy_date + one_day
            buy_date = buy_date.strftime("%Y-%m-%d")

        while sel_date not in price_dates:
            if sel_date > max_date:
                sel_date = max_date
                break # Abort if after price data
            if sel_date < min_date:
                sel_date = min_date
                break # Abort if more recent than price data
            sel_date = pd.to_datetime(sel_date)
            sel_date = sel_date + one_day
            sel_date = sel_date.strftime("%Y-%m-%d")
        
        buy_price = float(prices[buy_date][ticker])
        sel_price = float(prices[sel_date][ticker])
        bench_buy = float(bench_p[buy_date])
        bench_sel = float(bench_p[sel_date])
        ret = (sel_price/buy_price-1)*100
        ret_b = (bench_sel/bench_buy-1)*100
        
        if ret == ret:
            trans_dates.append(buy_date)
            trans_dates.append(sel_date)
            port_num.append(1)
            port_num.append(-1)
            stock.append(ticker)
            stock.append(ticker)
            returns.append(0)
            returns.append(ret)
            trans_prices.append(buy_price)
            trans_prices.append(sel_price)
            bench_ret.append(0)
            bench_ret.append(ret_b)
            
    out = zip(trans_dates,port_num, trans_prices, returns, bench_ret)
    out = pd.DataFrame(out, index=stock,\
                       columns=['Date','B/S','Price','Return', 'Bench Ret.'])
    out = out.sort_values(by ='Date')
    out['#Stocks'] = out['B/S'].cumsum()    
    r = out['Return'].mean()*2
    rb = out['Bench Ret.'].mean()*2
    s = out['#Stocks'].max()
    tot = pd.DataFrame([' ',0,0,r,rb,s], columns=['Total'],index=out.columns).T
    out = pd.concat([out,tot])
    
    return out

def quick_ret_calc(prices, bench_p, bb_dates, delay_days, hold_years):
    '''
    Version 1.0, MPPA @ 21:00 29.07.2014

    Compute the returns of a set of tickers
    '''
    ticker_list = prices.index.tolist()
    num_ticks = len(ticker_list)
    if num_ticks == 0: return [0,0]
    
    price_dates = prices.T.index.tolist()
    max_date = price_dates[len(price_dates)-1]
    min_date = price_dates[0]
    
    buy_del = relativedelta(days=delay_days)
    sel_del = relativedelta(days=delay_days,years=hold_years)
    one_day = relativedelta(days=1)

    p = 0
    b = 0
    ar = 0
    unused = 0
    
    for i in range(num_ticks):
        ticker = ticker_list[i]
        bb_date = pd.to_datetime(bb_dates[i])
        #print ticker
        #print bb_date
        #print buy_del
        
        buy_date = bb_date + buy_del
        sel_date = bb_date + sel_del
        buy_date = buy_date.strftime("%Y-%m-%d")
        sel_date = sel_date.strftime("%Y-%m-%d")

        while buy_date not in price_dates:
            if buy_date > max_date:
                buy_date = max_date
                break # Abort if after price data
            if buy_date < min_date:
                buy_date = min_date
                break # Abort if more recent than price data
            buy_date = pd.to_datetime(buy_date)
            buy_date = buy_date + one_day
            buy_date = buy_date.strftime("%Y-%m-%d")

        while sel_date not in price_dates:
            if sel_date > max_date:
                sel_date = max_date
                break # Abort if after price data
            if sel_date < min_date:
                sel_date = min_date
                break # Abort if more recent than price data
            sel_date = pd.to_datetime(sel_date)
            sel_date = sel_date + one_day
            sel_date = sel_date.strftime("%Y-%m-%d")
 
        buy_price = float(prices[buy_date][ticker])
        sel_price = float(prices[sel_date][ticker])
        bench_buy = float(bench_p[buy_date])
        bench_sel = float(bench_p[sel_date])
        ret = (sel_price/buy_price-1)*100
        ret_b = (bench_sel/bench_buy-1)*100
        
        if ret == ret:
            p = p + ret/float(num_ticks)
            b = b + ret_b/float(num_ticks)
            ar = ar + (ret-ret_b)/float(num_ticks)
        else:
            unused = unused + 1

    p = p*float(num_ticks)/float(num_ticks-unused)
    b = b*float(num_ticks)/float(num_ticks-unused)
    ar = ar*float(num_ticks)/float(num_ticks-unused)
    
    return [ar,p,b]
