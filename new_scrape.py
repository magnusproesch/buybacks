import mechanize
from bs4 import BeautifulSoup
import requests
import datetime
import re

date = ""
ticker = ""
name = ""
buyback = ""
unit = ""
val = 0

count = 0
count1 = 0
string =[]
start = 0
stop = 0
extract = []

stock_list = []
date_list = []
bb_list = []

#Load reference database by external function


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
        count1 = count1 + 1
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
                print date
            if count == 2:
                ticker = extract[extract.find(">")+1:len(extract)]
                print ticker
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
                
                print buyback
        
        date_list.append(date)
        stock_list.append(ticker)
        bb_list.append(val)

        print count1

    #Scrape the relevant info for all announcements in EVEN rows
    for item in soup.select(".ecoCalAltContent"):
        count1 = count1 + 1
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
                print date
            if count == 2:
                ticker = extract[extract.find(">")+1:len(extract)]
                print ticker
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

master = [date_list, stock_list, bb_list]
print master
  

