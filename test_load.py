import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame, read_csv
import time

source = open('scrape_database.csv','r')

time_beg = 0
time_end = 1


if time_beg <= 0: time_beg = 0
if time_end <= 1: time_end = time.strftime("%Y-%m-%d")

time_beg = pd.to_datetime(time_beg)
time_end = pd.to_datetime(time_end)

print time_beg
print time_end

raw_ticker_list = []
ticker_list = []

line = source.readline()

while line !='':
        
        bb_date = pd.to_datetime(line[:line.find(",")])
        
        if (bb_date < time_end) & (bb_date > time_beg):
            ticker = line[line.find(",") + 1 : line.rfind(",")]

            if ticker not in raw_ticker_list:
                raw_ticker_list.append(str(ticker))

        line = source.readline()

source.close()

print raw_ticker_list
print len(raw_ticker_list)

ticker_list = raw_ticker_list

df = read_csv('financial_data.csv')
full_ticker_df = df['Unnamed: 0']
ind = df.columns.tolist()
ind.pop(0)
full_ticker = full_ticker_df.tolist()
print full_ticker
print len(full_ticker)
df = df.T
df = df[1:]
df.columns = full_ticker
r = df[full_ticker]
print r.T
