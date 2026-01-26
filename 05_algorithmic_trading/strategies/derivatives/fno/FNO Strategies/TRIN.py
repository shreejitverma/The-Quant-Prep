#Copyright QuantInsti Quantitative Learning Private Limited

#importing required libraries
import pandas as pd
import quandl
import matplotlib.pyplot as plt
import math

def variance_calculator(series,series_average,win_len):
	sma = win_len
	temp = series.subtract(series_average)          # a-b
	temp2 = temp.apply(lambda x: x**2)              #(a-b)^2
	temp3 = temp2.rolling(sma-1).mean()             # summation[(a-b)^2 ]/ (sma -1)
	sigma = temp3.apply(lambda x : math.sqrt(x))    #sigma is the standard deviation
	return sigma


Data1 = quandl.get("CHRIS/CME_SP1", authtoken="mq-W7Z-QXBDZ1MxaN-Vy", start_date="2014-12-12")
declining = quandl.get("URC/NYSE_DEC", authtoken = "mq-W7Z-QXBDZ1MxaN-Vy", start_date="2014-12-12")
advancing = quandl.get("URC/NYSE_ADV", authtoken = "mq-W7Z-QXBDZ1MxaN-Vy",start_date="2014-12-12")
adv_vol = quandl.get("URC/NYSE_ADV_VOL", authtoken = "mq-W7Z-QXBDZ1MxaN-Vy",start_date="2014-12-12")
dec_vol = quandl.get("URC/NYSE_DEC_VOL", authtoken = "mq-W7Z-QXBDZ1MxaN-Vy",start_date="2014-12-12")
Data = declining
Data['declining'] = declining['Numbers of Stocks']
Data['advancing'] = advancing['Numbers of Stocks']
Data['dec_vol'] = dec_vol['Numbers of Stocks']
Data['adv_vol'] = adv_vol['Numbers of Stocks']
merged = Data.join(Data1)
merged = merged.fillna(method ='ffill')
Data = merged
#finding the TRIN value using the number and volume of advancing & declining stocks
tem1 = Data['advancing'].divide(Data['declining'])
tem2 = Data['adv_vol'].divide(Data['dec_vol'])
tem = tem1.divide(tem2)#TRIN value
Data['TRIN'] = tem
Data['TRIN'] = Data['TRIN'].apply(lambda x: math.log(x))# applying log to the lopsided TRIN and storing the new TRIN
Data['future'] = Data['Last']
Data.to_csv("tempr_data.csv")
Data = pd.read_csv("tempr_data.csv")


sma = 22 #............................the moving average window length
k = 1.5 # ............................constant representing 'k' times sigma away from moving average(for Bollinger Bands)
l = 2 #...............................constant representing 'l' times sigma away from Bollinger bands( for stoploss band)
inv = 0
pro = 0#..............................profit variable
flag = 1 #............................flag is there for the first transaction--- transaction should start with LBB/UBB crossing only
buy_flag = False
sell_flag = False
transaction_start_price = 0
abs_SL = 25
mtm = list()
order_details = list()
order = list()#.......................order is  a list which contains the orders:- BUY/SELL/DO_Nothing
profit = list()
buy_sell = list()
stoploss = list()
trade_cause = list()


Data['mAvg'] = Data['TRIN'].rolling(sma).mean()         #calculating the moving average of the TRIN
Data['TRIN_prev'] = Data['TRIN'].shift(1)               #moving average shifted ahead to check for crossover
Data.to_csv("tempr_data.csv")                           #data stored in tempr_data.csv excel file
Data = pd.read_csv("tempr_data.csv")                    
#calculating the standard deviation
sigma = variance_calculator(Data['TRIN'],Data['mAvg'],sma)#calculating the standard deviation
k_sigma = k*sigma
l_sigma = l * sigma

Data['UBB'] = Data['mAvg'].add(k_sigma) #.........upper bollinger band
Data['LBB'] = Data['mAvg'].subtract(k_sigma) #....lower bollinger band
Data['USL'] = Data['UBB'].add(l_sigma) #..........upper stoploss band
Data['LSL'] = Data['LBB'].subtract(l_sigma)#......lower stoploss band
Data['order'] = pd.Series() #.....................order is  a list which contains the orders:- BUY/SELL/DO_Nothing

s = Data['TRIN'].size#..............size of the TRIN series

# logic to generate 'buy' and 'sell' signals starts here ========================================================================
#--------------------------------------------------------------------------------------------------------------------------------
#this loop checks for TRIN crossing LBB,UBB,MaVG AND PLACES THE BUY/SELL ORDER

for i in range(s):
	
    pro = 0 # profit at each trade
    #variables to be used for comarison
    future_cost = Data['future'][i]#...........cost of big S&P 500 futures bought
    TRIN      =   Data['TRIN'][i]#.............current TRIN ratio value
    TRIN_prev  =   Data['TRIN_prev'][i]#.......previous day's TRIN ratio (for crossover check)
    LBB      =   Data['LBB'][i] #..............lower bollinger band
    UBB      =   Data['UBB'][i]#...............upper bollinger band
    mAvg     =   Data['mAvg'][i]#..............moving average
    USL      =   Data['USL'][i]#...............upper stoploss band
    LSL      =   Data['LSL'][i] #..............lower stoploss band
    
    #comparisons stored as boolean variables to place order accordingly
    UBB_cross        =   (TRIN > UBB) and (TRIN_prev < UBB)# .......Check if TRIN crosses upper bollinger band
    LBB_cross        =   (TRIN < LBB) and (TRIN_prev > LBB)# .......Check if TRIN crosses lower bollinger band
    mAvg_cross_up    =   (TRIN > mAvg) and (TRIN_prev < mAvg)#......Check if TRIN crosses moving average low to high
    mAvg_cross_down  =   (TRIN < mAvg) and (TRIN_prev > mAvg)#......Check if TRIN crosses moving average high to low
    USL_cross        =   (TRIN > USL)  and  (TRIN_prev < USL)#......Check if TRIN crosses upper stoploss band
    LSL_cross        =   (TRIN < LSL)  and  (TRIN_prev > LSL)#......Check if TRIN crosses lower stoploss band

    if(UBB_cross and (not buy_flag) and flag ==1): #...........places "BUY" order if TRIN crosses upper bollinger band to open a trade
        flag = 0
        buy_flag = True      
        sell_flag = False
        transaction_start_price = future_cost #............price at which S&P 500 future bought when order is placed
        order_details = [1,"Buy" , "UBB crossed" , "0" , "position taken"]
	
    elif (LBB_cross and (not sell_flag) and flag ==1): #.......places "SELL" order if TRIN crosses lower bollinger band to open a trade
        flag = 0
        sell_flag = True  
        buy_flag = False
        transaction_start_price = future_cost
        order_details = [-1,"Sell" , "LBB crossed" , "0" , "position taken"]
	
    elif (mAvg_cross_up and flag==0 and (not buy_flag)) : #........places "BUY" order if TRIN crosses mAvg from low to high to close a trade  
        flag = 1
        buy_flag = False 
        sell_flag = False
        pro = future_cost -transaction_start_price
        order_details = [1,"Buy" , "mAvg crossed" , "0" , "position closed"]
		
    elif( LSL_cross and flag == 0 and (not buy_flag)): #......places "BUY" order if TRIN crosses lower stoploss band to close a trade
        flag = 1
        buy_flag = False
        sell_flag = False
        pro = future_cost - transaction_start_price
        order_details = [1,"Buy" , "LSB crossed" , "stoploss executed" , "position closed"]
    
    elif((future_cost - transaction_start_price) > abs_SL and flag == 0 and (not buy_flag)):#......places "BUY " order if TRIN crosses lower stoploss #absolute value
        flag = 1
        buy_flag = False
        sell_flag = False
        pro = future_cost - transaction_start_price
        order_details = [1,"Buy" , "LSB crossed" , "stoploss executed abs" , "position closed"]		

    elif (mAvg_cross_down and flag==0 and (not sell_flag)):#.....places "SELL" order if TRIN crosses mAvg from high to low to close a trade
        flag = 1
        sell_flag = False
        buy_flag = False
        pro = -(future_cost - transaction_start_price)
        order_details = [-1,"Sell" , "mAvg crossed (h to l)" , "0" , "position closed"]
    
    elif(USL_cross and flag==0 and (not sell_flag)):# ..places "SELL" order if TRIN crosses upper stoploss band to close a trade
        flag = 1
        sell_flag = False
        buy_flag = False
        pro = -(future_cost - transaction_start_price)
        order_details = [-1,"Sell" , "USB crossed" , "stoploss executed" , "position closed"]

    elif((-future_cost + transaction_start_price) > abs_SL and flag==0 and (not sell_flag)): # ..places "SELL" order if PCR crosses upper stoploss absolute #value
        flag = 1
        sell_flag = False
        buy_flag = False
        pro = -(future_cost - transaction_start_price)
        order_details = [-1,"Sell" , "USB crossed" , "stoploss executed_abs" , "position closed"]

    else:
        if(buy_flag==0 and sell_flag==0): tempo = "0"
        else:
            if(buy_flag==1 and sell_flag==0): tempo = (Data['future'][i] -transaction_start_price) * 500
            if(buy_flag==0 and sell_flag==1): tempo= (-Data['future'][i] +transaction_start_price) * 500
        order_details = [0,"No trade" , "no trade" , "0" , tempo]
	

    profit.append(pro)
    order.append(order_details[0])
    buy_sell.append(order_details[1])
    trade_cause.append(order_details[2])
    stoploss.append(order_details[3])
    mtm.append(order_details[4])

#------------------------------------------------------------------------------------------------------------------------------
#buy/sell logic ends================================================================================================================

Data['placed_order'] = pd.Series(order) #..............................converting list to pandas series
Data['cost'] = -(Data['placed_order'].multiply(Data['future'])) *500# ..cost at each transaction
Data['out'] = Data['cost'].cumsum()# ..................................out is the cumulative cost profit/loss after transactions till now
Data['buy_sell'] = pd.Series(buy_sell)
Data['profit'] = -pd.Series(profit) * 500
Data['stoploss'] = pd.Series(stoploss)
Data['trade_cause']  = pd.Series(trade_cause)
Data['mtm'] = pd.Series(mtm)
print (Data['out'])

output = pd.DataFrame() #....final output to be stored in excel file
output['date'] = Data['Date']
output['Close'] = Data['future']
output['TRIN'] = Data['TRIN']
output['placed_order'] = Data['placed_order']
output['buy_sell'] = Data['buy_sell']
output['trade_cause'] =  Data['trade_cause']
output['PnL'] = Data['profit']
output['mtm'] = Data['mtm']
output['stoploss'] = Data['stoploss']
output['Cash Account'] = Data['out']
output.to_excel('TRIN_SL_output.xlsx', sheet_name='Sheet1')


#plt.plot(order)
plt.plot(Data['TRIN'])
plt.plot(Data['mAvg'])
plt.plot(Data['UBB'])
plt.plot(Data['LBB'])
#plt.plot(Data['out'])
plt.show()

#Copyright QuantInsti Quantitative Learning Private Limited
