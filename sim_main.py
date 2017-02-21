import sim_rank as s_r
import bb_calc as bb_c
import bb_load as bb_l
import time

data =  s_r.load_stats()
# Perform simulations
s_r.simulate_rank(data,2000)
'''
# Test return calc
rank_cutoff = 0.75
ticker_list = data[data['Total Rank'] > rank_cutoff].\
                             index.values.tolist()
prices = bb_l.load_price_df(ticker_list)
bench_p = bb_l.load_benchmark_df()
bb_d = data['Buyback Date'][ticker_list]

start_time = time.time()
a = bb_c.quick_ret_calc(prices, bench_p, bb_d.tolist(), 14, 3)
print '##>> Calculation time:', "%.4f" %(time.time() - start_time), 'sec\n'
start_time = time.time()
b = bb_c.ret_calc(ticker_list, bb_d.tolist(), 14, 3)
print '##>> Calculation time:', "%.4f" %(time.time() - start_time), 'sec\n'
'''
