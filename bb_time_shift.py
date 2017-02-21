import bb_load as bb_l
import bb_group as bb_g
from pandas import DataFrame, Series

def time_shift_norm_prices(ticker_list):
    '''

    SUPPORT FUNCTION

    Version 1.1: MSP @ 16:30 08.05.14

    (list of tickers)-> df shifted times

    shifts time of prices accourding to buyback announcement
    and returns normalized returns (buyback date = 100)

    '''

    # Load data
    bb = bb_g.group_bb_df(-1,-1)
    prices = bb_l.load_price_df(ticker_list)

    # Determine dates
    bb_dates = bb[ticker_list].T['Date'].tolist()
    first_bb_date = bb_dates[0]
    last_bb_date = bb_dates[0]
    ind = []
    bb_price = []
    dates_pre = 0
    dates_post = 0
    price_dates = prices.columns.tolist()
    num_dates = len(price_dates)
    first_price_date = price_dates[0]
    last_price_date = price_dates[num_dates-1]

    for i in range(len(bb_dates)):
        bb_dates[i] = str(bb_dates[i]) # Convert elements to unicode strings
        ind.append(price_dates.index(bb_dates[i])) # Price at announcement day
        bb_price.append(float(prices.iat[i,ind[i]]))         
        if first_bb_date > bb_dates[i]:
            first_bb_date = bb_dates[i]
            dates_pre = ind[i]
        if last_bb_date <= bb_dates[i]:
            last_bb_date = bb_dates[i]
            dates_post = num_dates - ind[i]-1

    # Compute and assemble DataFrame
    norm_ts_prices = DataFrame(index = range(-dates_pre,dates_post+1))
    
    for i in range(len(ticker_list)):
        p = prices.ix[ticker_list[i],ind[i]-dates_pre:ind[i]+dates_post+1]
        p_n = p/bb_price[i]*100
        norm_ts_prices[ticker_list[i]] = p_n.tolist()

    norm_ts_prices = norm_ts_prices.T
    
    return norm_ts_prices



def time_shift_prices(ticker_list):
    '''

    SUPPORT FUNCTION

    Version 1.1: MSP @ 16:30 08.05.14

    (list of tickers)-> df shifted times

    shifts time of prices accourding to buyback announcement (t=0)

    '''

    # Load data
    bb = bb_g.group_bb_df(-1,-1)
    prices = bb_l.load_price_df(ticker_list)

    # Determine dates
    bb_dates = bb[ticker_list].T['Date'].tolist()
    first_bb_date = bb_dates[0]
    last_bb_date = bb_dates[0]
    ind = []
    bb_price = []
    dates_pre = 0
    dates_post = 0
    price_dates = prices.columns.tolist()
    num_dates = len(price_dates)
    first_price_date = price_dates[0]
    last_price_date = price_dates[num_dates-1]
    for i in range(len(bb_dates)):
        bb_dates[i] = str(bb_dates[i]) # Convert elements to unicode strings
        ind.append(price_dates.index(bb_dates[i])) # Price at announcement day
        bb_price.append(float(prices.iat[i,ind[i]]))         
        if first_bb_date > bb_dates[i]:
            first_bb_date = bb_dates[i]
            dates_pre = ind[i]
        if last_bb_date <= bb_dates[i]:
            last_bb_date = bb_dates[i]
            dates_post = num_dates - ind[i]-1

    # Compute and assemble DataFrame
    ts_prices = DataFrame(index = range(-dates_pre,dates_post+1))
    for i in range(len(ticker_list)):
        p = prices.ix[ticker_list[i],ind[i]-dates_pre:ind[i]+dates_post+1]
        ts_prices[ticker_list[i]] = p.tolist()

    ts_prices = ts_prices.T

    return ts_prices


def time_shift_norm_benchmark(ticker_list):
    '''

    SUPPORT FUNCTION

    Version 1.1: MSP @ 16:30 08.05.14

    (list of tickers)-> df shifted times

    Returns a DataFrame containing benchmark values shifted according to
    buyback announcements (bb date = 0) and normalized such that it equals 100
    at the buyback date

    '''

    # Load data
    bb = bb_g.group_bb_df(-1,-1)
    prices = bb_l.load_price_df(ticker_list)
    benchmark = bb_l.load_benchmark_df()
    
    # Determine dates
    bb_dates = bb[ticker_list].T['Date'].tolist()
    first_bb_date = bb_dates[0]
    last_bb_date = bb_dates[0]
    ind = []
    bb_price = []
    dates_pre = 0
    dates_post = 0
    price_dates = prices.columns.tolist()
    num_dates = len(price_dates)
    first_price_date = price_dates[0]
    last_price_date = price_dates[num_dates-1]
    for i in range(len(bb_dates)):
        bb_dates[i] = str(bb_dates[i]) # Convert elements to unicode strings
        ind.append(price_dates.index(bb_dates[i])) # Price at announcement day
        bb_price.append(float(prices.iat[i,ind[i]]))         
        if first_bb_date > bb_dates[i]:
            first_bb_date = bb_dates[i]
            dates_pre = ind[i]
        if last_bb_date <= bb_dates[i]:
            last_bb_date = bb_dates[i]
            dates_post = num_dates - ind[i]-1

    # Compute and assemble DataFrame
    norm_ts_benchmark = DataFrame(index = range(-dates_pre,dates_post+1))
    for i in range(len(ticker_list)):
        b = benchmark[ind[i]-dates_pre:ind[i]+dates_post+1]/benchmark[ind[i]]*100
        norm_ts_benchmark[ticker_list[i]] = b.tolist()

    norm_ts_benchmark = norm_ts_benchmark.T

    return norm_ts_benchmark

def time_shift_benchmark(ticker_list):
    '''

    SUPPORT FUNCTION

    Version 1.1: MSP @ 16:30 08.05.14

    (list of tickers)-> df shifted times

    Returns a DataFrame containing benchmark values shifted according to
    buyback announcements (bb date = 0) 

    '''

    # Load data
    bb = bb_g.group_bb_df(-1,-1)
    prices = bb_l.load_price_df(ticker_list)
    benchmark = bb_l.load_benchmark_df()
    benc_name = bb_l.load_benchmark_name()

    # Determine dates
    bb_dates = bb[ticker_list].T['Date'].tolist()
    first_bb_date = bb_dates[0]
    last_bb_date = bb_dates[0]
    ind = []
    bb_price = []
    dates_pre = 0
    dates_post = 0
    price_dates = prices.columns.tolist()
    num_dates = len(price_dates)
    first_price_date = price_dates[0]
    last_price_date = price_dates[num_dates-1]
    for i in range(len(ticker_list)):
        bb_dates[i] = str(bb_dates[i]) # Convert elements to unicode strings
        ind.append(price_dates.index(bb_dates[i])) # Price at announcement day
        bb_price.append(float(prices.iat[i,ind[i]]))         
        if first_bb_date > bb_dates[i]:
            first_bb_date = bb_dates[i]
            dates_pre = ind[i]
        if last_bb_date <= bb_dates[i]:
            last_bb_date = bb_dates[i]
            dates_post = num_dates - ind[i]-1

    # Compute and assemble DataFrame
    ts_benchmark = DataFrame(index = range(-dates_pre,dates_post+1))
    for i in range(len(ticker_list)):
        b = benchmark[ind[i]-dates_pre:ind[i]+dates_post+1]
        ts_benchmark[ticker_list[i]] = b.tolist()

    ts_benchmark = ts_benchmark.T
    
    return ts_benchmark

def time_shifted_abn_ret(ticker_list, betas=[1]):
    '''

    SUPPORT FUNCTION


    Version 1.0: MPPA @ 19:30 01.07.14

    (list of tickers, *list of betas)-> df shifted times

    Returns a DataFrame containing abnormal return relative to buyback date
    buyback date announcements (bb date in column 0) 

    '''

    if len(betas)<len(ticker_list):
        betas.extend([1]*(len(ticker_list)-len(betas)))

    # Load data
    norm_price = time_shift_norm_prices(ticker_list)
    norm_bench = time_shift_norm_benchmark(ticker_list)

    betas = Series(betas, index=ticker_list)
    df = DataFrame(index = norm_price.index, columns = norm_price.columns)
    
    days = norm_price.columns.tolist()
    for i in range(len(days)):
        if days[i]<0: #if pre buyback date
            ret_bench = (100/norm_bench[days[i]]-1)*100
            ret_price = (100/norm_price[days[i]]-1)*100
        else: #if post buyback date
            ret_bench = norm_bench[days[i]]-100
            ret_price = norm_price[days[i]]-100
        df[days[i]] = ret_price - betas * ret_bench

    return df
