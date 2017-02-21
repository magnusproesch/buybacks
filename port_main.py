'''

Version 0.1, MSP @ 16:53 02.07.14 

'''

import time
fundamental_time = time.time() # Start clock

print '\n   ########################################################'
print '   #####         BUYBACK - Portfolio manager           ####'
print '   #####               Magnus S. Proesch               ####'
print '   #####              Matthias P.P. Amble              ####'
print '   #####                    (C)2014                    ####'
print '   ########################################################\n'

print 'Loading libraries...'
import port_func as pf
import numpy as np
import pandas as pd

print '-> Processing time:', "%.2f" %(time.time() - fundamental_time), 'sec\n'

#Update the total portfolio with buy and sell
update = raw_input('Update transaction list?(y/n): ')

if update == 'y':
    current = pf.load_transactions()
    pf.write_portfolio(current)

#Consolidate the current portfolio

#Analyse the current portfolio

#Portf prices
see = raw_input('See the P&L? (y/n) : ')
if see == 'y':
    df = pf.get_current_prices() 
    print df
    

    #Portf weighted market value
    #Portf return and abn return
    #Portf risk profile

#Analyse the total portfolio

    #Portf prices
    #Portf weighted market value
    #Portf return and abn return
    #Portf risk profile
    
#Simulate
