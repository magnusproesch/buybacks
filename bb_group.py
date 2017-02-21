import bb_load as bb_l
import pandas as pd
from pandas import DataFrame, read_csv, to_datetime
from dateutil.relativedelta import relativedelta

def group_bb_df(time_beg, time_end):

    '''
    SUPPORT FUNCTION
    
    Version 2.0: MPPA/MSP @ 19:50 05.05.14

    (int(time_range)) -> df

    Loads list of buybacks within <time_range> months and returns dataframe
    with unique index of tickers and merged buyback dates and amounts

    '''

    df = bb_l.load_buyback_df(time_beg, time_end).T
    #df_g = df.groupby(level=0)

    raw_names = df.index.tolist()
    raw_dates = df['Date'].tolist()
    raw_amounts = df['Amount'].convert_objects(convert_numeric = True).tolist()
    #raw_amounts = pd.to_numeric(df['Amount']).tolist()

    price_dates = bb_l.load_benchmark_df().T.index.tolist()
    max_date = price_dates[len(price_dates)-1]
    min_date = price_dates[0]
    one_day = relativedelta(days=1)

    new_names = []
    new_dates = []
    new_amounts = []
    occurances = []
    
    for i in range(len(raw_names)):
        name = raw_names[i]
        if name not in new_names:
            date = raw_dates[i]
            amount = float(raw_amounts[i])
            occurance = 1
            dates = [date]
            amounts = [amount]
            
            for j in range(i+1,len(raw_names)):
                date_n = raw_dates[j]
                name_n = raw_names[j]
                amount_n = float(raw_amounts[j])

                if name == name_n:
                    if date != date_n:
                        amounts.append(amount_n)    
                        dates.append(date_n)
                        occurance = occurance + 1
                    else:
                        if amount != amount_n:
                            amounts.append(amount_n)    
                            dates.append(date_n)

            tot_amount = 0 # REDUNDANT
            factor = 1 #Adjustable
            max_am = amount
            
            for am in amounts:
                # Compute the total aggregated amount (REDUNDANT)
                tot_amount = tot_amount + am*factor 
                # Choose the max amount of all dates
                if am > max_am:
                    max_am = am

            # Choose the most recent date        
            for day in dates:
                if day > date:
                    date = day

            # Move date to next trading day after announcement
            while date not in price_dates:
                if date > max_date: break # Abort if after price data
                if date < min_date: break # Abort if more recent than price data
                date = to_datetime(date)
                date = date + one_day
                date = date.strftime("%Y-%m-%d")

            new_names.append(name)
            new_dates.append(date)
            new_amounts.append(amount)
            occurances.append(occurance)

    df = zip(new_dates, new_amounts, occurances)

    if len(new_names)>0:
        df = DataFrame(data=df,index=new_names,columns=['Date','Amount'\
                                                        ,'No. of BB announ.'])
    else:
        df = DataFrame(index=new_names,columns=['Date','Amount'\
                                                        ,'No. of BB announ.'])

    return df.T
