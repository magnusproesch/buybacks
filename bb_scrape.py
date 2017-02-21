
from bs4 import BeautifulSoup
import urllib2
import datetime
import re
import csv
import sys
import time
import bb_load as bb_l
import pandas as pd
import requests

#Scrape the web for new buybacks
def scrape_buybacks():

    '''

    (NoneType) -> scraped_database.csv, database=open('scrape_database.csv', 'r')


    Version 3.0, MSP @ 11:00 04.06.16
    
    '''


    #Define some of the variables used
    start_time = time.time()
    stock_list = []
    date_list = []
    bb_list = []
    not_added = int(0)
    full_switch = 'y'

    #Load reference database by external function
    try:
        existing_database = read_existing_scrapefile()
        print ('Comparing existing database to new buybacks.')
        first = existing_database[0]
        first_date = first[0:first.find(',')]
        full_switch = raw_input('Do a full search beyond the most recent date '\
                   +'in database? y/n: ')
    except (IOError, Warning):
        print 'Warning: No prior database available.', '\n' \
          'No reference check will be conducted; proceed with a new database file.', '\n'
        existing_database = []
        first_date = 0
    
    
    #Run a for loop to scrape all 5 pages of data
    for numb in ('1', '2', '3', '4', '5'):
        url = ("http://www.rttnews.com/CorpInfo/StockBuybacks.aspx?PageNum=" + numb)

        try: #Scrape the page
            soup = BeautifulSoup(requests.get(url).content, "html.parser")

        except (Warning, IOError): #Inform of any problems
            print 'Failed to scrape page number ' + numb + '.' + '\n' \
                  'The remote host could have terminated the connection.' + '\n' \
                  'Scraping terminated; try to run the program again.'
            sys.exit(0)

        
        end_search = False

        #Scrape the relevant info for all announcements in ODD rows
        for item in soup.select(".ecoCalContent"):
            count = 0
            
            #Scrape the relevant info for an individual announcement
            for numb in ["1","2","3","4","5","6"]:
                string = ".tblContent" + numb
                count = count + 1
                
                start = int(str(item.select(string)).find('">') + 2)
                stop = int(str(item.select(string)).find('</'))
                
                extract = str(item.select(string))[start:stop]

                if count == 1:
                    date = extract
                    y = int(date[date.rfind("/")+1:len(date)])+2000
                    try:
                        d = int(date[date.find("/")+1:len(date)-date.find("/")-2])
                    except ValueError:
                        d = 1
                    m = int(date[0:date.find("/")])
                    date = datetime.datetime(y,m,d).strftime("%Y-%m-%d")
                   
                if count == 2:
                    ticker = extract[extract.find(">")+1:len(extract)]

                    if ticker.find(",") > 0: 
                        while ticker.count(",") > 1: # strip until unly one comma left
                            ticker = ticker[ticker.find(",")+1:len(ticker)] # Strip before first comma
                        ticker = ticker[0:ticker.find(",")] # Strip after second comma
                    if ticker.find(".") > 0: 
                        ticker = ticker[0:ticker.find(".")]

                    ticker = filter(str.isupper, ticker)
                   
                if count == 4:
                    buyback = extract
                    unit = buyback.join(re.findall("[a-zA-Z]+", buyback))
                    val = re.findall(r"[-+]?\d*\.\d+|\d+", buyback)
                    val = float(val[0])

                    if unit == "":
                        val = val / 1000000
                    elif unit == "K":
                        val = val / 1000
                    elif unit == "Bln":
                        val = val * 1000
                    
            date_list.append(date)
            stock_list.append(ticker)
            bb_list.append(val)

            #Build the aggregated list and removing buybacks
            #already in the existing buyback database

            teststr = str(date)+','+str(ticker)+','+str(val)
            
            if teststr in existing_database:
                date_list.pop()
                stock_list.pop()
                bb_list.pop()
                not_added = not_added + 1

        #Scrape the relevant info for all announcements in EVEN rows
        for item in soup.select(".ecoCalAltContent"):
            count = 0
            
            #Scrape the relevant info for an individual announcement
            for numb in ["1","2","3","4","5","6"]:
                string = ".tblContent" + numb
                count = count + 1
                
                start = int(str(item.select(string)).find('">') + 2)
                stop = int(str(item.select(string)).find('</'))
                
                extract = str(item.select(string))[start:stop]

                if count == 1:
                    date = extract
                    y = int(date[date.rfind("/")+1:len(date)])+2000
                    try:
                        d = int(date[date.find("/")+1:len(date)-date.find("/")-2])
                    except ValueError:
                        d = 1
                    m = int(date[0:date.find("/")])
                    date = datetime.datetime(y,m,d).strftime("%Y-%m-%d")
                    
                if count == 2:
                    ticker = extract[extract.find(">")+1:len(extract)]

                    if ticker.find(",") > 0: 
                        while ticker.count(",") > 1: # strip until unly one comma left
                            ticker = ticker[ticker.find(",")+1:len(ticker)] # Strip before first comma
                        ticker = ticker[0:ticker.find(",")] # Strip after second comma
                    if ticker.find(".") > 0: 
                        ticker = ticker[0:ticker.find(".")]

                    ticker = filter(str.isupper, ticker)

                if count == 4:
                    buyback = extract
                    unit = buyback.join(re.findall("[a-zA-Z]+", buyback))
                    val = re.findall(r"[-+]?\d*\.\d+|\d+", buyback)
                    val = float(val[0])

                    if unit == "":
                        val = val / 1000000
                    elif unit == "K":
                        val = val / 1000
                    elif unit == "Bln":
                        val = val * 1000
                              
            date_list.append(date)
            stock_list.append(ticker)
            bb_list.append(val)

            #Build the aggregated list and removing buybacks
            #already in the existing buyback database

            teststr = str(date)+','+str(ticker)+','+str(val)
            
            if teststr in existing_database:
                date_list.pop()
                stock_list.pop()
                bb_list.pop()
                not_added = not_added + 1

    #Make a master list              
    master = [date_list, stock_list, bb_list]

    with open('scrape_database.csv', 'ab') as scrapefile:
      file_writer = csv.writer(scrapefile)

      for i in range(len(master[0])):
        file_writer.writerow([x[i] for x in master])

    sort_existing_scrapefile()
    
    print '\n', '---------------------------------------------------------'
    print 'MODULE: NEW SHARE BUYBACKS FROM STOCKMAVEN.COM.'
    print 'Output: ' + str(len(date_list)) + \
          ' buyback(s) added to scrape_database.csv.'
    print '        ' + str(not_added) + ' buyback(s) scraped but not added to database'
    print 'Run-time:', "%.2f" %(time.time() - start_time), 'sec'
    print '---------------------------------------------------------' + '\n'


#Read the existing scrapefile into a list for comparison
def read_existing_scrapefile():

    '''
    (file open for reading) -> list of str

    Read and return each row in the scrapefile
    comprising date, ticker, and amount of a buyback and return
    a list of strings containing this information

    Precondition: the file scrapefile.csv must be available in
    the root directory
    
    '''

    scrape_database = open('scrape_database.csv','r')

    line = scrape_database.readline().strip('\n')
    
    existing_database = []
    
    while line !='':
        existing_database.append(str(line))
        line = scrape_database.readline().strip('\n')

    scrape_database.close()
    
    return existing_database    

# Sort the existing scrapefile by descending dates
def sort_existing_scrapefile():
    '''

    Version update: MSP @ 00:12 29.04.14
    
    ( ) -> ( )

    Sort the buyback database (scrape_database.csv) by descending dates.
    
    '''

    c = bb_l.load_buyback_df(-1,-1).T.sort('Date',ascending=False)
    d = c.index.tolist()
    c['Ticker'] = d
    e = c['Date'].tolist()
    f = c[['Ticker','Amount']]
    f.index = e
    f.to_csv('scrape_database.csv', header=False)
