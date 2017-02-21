### get fundamentals
#data = quandl.get_table("ZACKS/FC", ticker="MSFT")

ticker = input('ticker: ')
string = "SF0/"+ticker+"_Revenue_MRY"
revenue = quandl.get(string)
