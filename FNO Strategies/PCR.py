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
	temp3 = temp2.rolling(sma-1).mean()             # summation[(a-b)^2 ]/ (sma - 1)
	sigma = temp3.apply(lambda x : math.sqrt(x))    #sigma is the standard deviation
	return sigma

def fetch_data(string1,string2,string3,filename):
	w = quandl.get(string1,authtoken = string2, start_date = string3)
	w.to_csv(filename)
	w = pd.read_csv(filename)
	return w

#the data pulled from quandl and stored locally for faster execution
Data1 = fetch_data( "CHRIS/CME_SP1", "mq-W7Z-QXBDZ1MxaN-Vy", "2014-12-12" ,"local_future.csv")
Data = fetch_data("CBOE/SPX_PC","mq-W7Z-QXBDZ1MxaN-Vy", "2014-12-12","local_data.csv")

Data['future'] = Data1['Last']
Data['PCR'] = Data['S&P PUT-CALL RATIO'] # PCR IS Put Call Ratio

sma = 20 #............................the moving average window length
k = 1 # ..............................constant representing 'k' times sigma away from moving average(for Bollinger Bands)
l = 1 #...............................constant representing 'l' times sigma away from Bollinger bands( for stoploss band)
flag = 1 #............................flag is there to begin first transaction--- transaction should start with LBB/UBB crossing only
pro = 0 #.............................profit variable
transaction_start_price = 0
buy_flag = False 
sell_flag = False
abs_SL = 5
mtm = list()
order = list()#...........................order is  a list which contains the orders:- BUY/SELL/DO_Nothing
profit = list()
buy_sell = list()
stoploss = list()
trade_cause = list()
order_details = list()


Data['mAvg'] = Data['PCR'].rolling(sma).mean()   #calculating the moving average of the PCR
Data['PCR_prev'] = Data['PCR'].shift(1)          #moving average shifted ahead to check for crossover


sigma = variance_calculator(Data['PCR'],Data['mAvg'],sma)#calculating the standard deviation
k_sigma = k*sigma
l_sigma = l*sigma

Data['UBB'] = Data['mAvg'].add(k_sigma) #.........upper bollinger band
Data['USL'] = Data['UBB'].add(l_sigma)#...........upper stoploss band
Data['LBB'] = Data['mAvg'].subtract(k_sigma)#.....lower bollinger band
Data['LSL'] = Data['LBB'].subtract(l_sigma)#......lower stoploss band
Data['order'] = pd.Series() #.....................order is  a list which contains the orders:- BUY/SELL/DO_Nothing

s = Data['PCR'].size#.................size of the PCR series

# logic to generate 'buy' and 'sell' signals starts here ==========================================================

#this loop checks for PCR crossing LBB,UBB,MaVG,stoploss_bands and places the buy/sell order..

for i in range(s):
	
	pro = 0 # profit at each trade
	#variables to be used for comarison
	future_cost = Data['future'][i]#...........cost of big S&P 500 futures bought
	PCR      =   Data['PCR'][i]#...............current putcall ratio value
	PCR_prev  =   Data['PCR_prev'][i]#.........previous day's put call ratio (for crossover check)
	LBB      =   Data['LBB'][i] #..............lower bollinger band
	UBB      =   Data['UBB'][i]#...............upper bollinger band
	mAvg     =   Data['mAvg'][i]#..............moving average
	USL      =   Data['USL'][i]#...............upper stoploss band
	LSL      =   Data['LSL'][i] #..............lower stoploss band
    
    #comparisons stored as boolean variables to place order accordingly
	UBB_cross        =   (PCR > UBB) and (PCR_prev < UBB)# .......Check if PCR crosses upper bollinger band
	LBB_cross        =   (PCR < LBB) and (PCR_prev > LBB)# .......Check if PCR crosses lower bollinger band
	mAvg_cross_up    =   (PCR > mAvg) and (PCR_prev < mAvg)#......Check if PCR crosses moving average low to high
	mAvg_cross_down  =   (PCR < mAvg) and (PCR_prev > mAvg)#......Check if PCR crosses moving average high to low
	USL_cross        =   (PCR > USL)  and  (PCR_prev < USL)#......Check if PCR crosses upper stoploss band
	LSL_cross        =   (PCR < LSL)  and  (PCR_prev > LSL)#......Check if PCR crosses lower stoploss band

	if(UBB_cross and (not buy_flag) and flag ==1): #...........places "BUY" order if PCR crosses upper bollinger band to open a trade
		flag = 0
		buy_flag = True      
		sell_flag = False
		transaction_start_price = future_cost #............price at which S&P 500 future bought when order is placed
		order_details = [1,"Buy" , "UBB crossed" , "0" , "position taken"]
	
	elif (LBB_cross and (not sell_flag) and flag ==1): #.......places "SELL" order if PCR crosses lower bollinger band to open a trade
		flag = 0
		sell_flag = True  
		buy_flag = False
		transaction_start_price = future_cost
		order_details = [-1,"Sell" , "LBB crossed" , "0" , "position taken"]
	
	elif (mAvg_cross_up and flag==0 and (not buy_flag)) : #........places "BUY" order if PCR crosses mAvg from low to high to close a trade  
		flag = 1
		buy_flag = False 
		sell_flag = False
		pro = future_cost -transaction_start_price
		order_details = [1,"Buy" , "mAvg crossed" , "0" , "position closed"]
		
	elif( LSL_cross and flag == 0 and (not buy_flag)):#......places "BUY" order if PCR crosses lower stoploss band to close a trade
		flag = 1
		buy_flag = False
		sell_flag = False
		pro = future_cost - transaction_start_price
		order_details = [1,"Buy" , "LSB crossed" , "stoploss executed" , "position closed"]
	elif( (future_cost - transaction_start_price) > abs_SL and flag == 0 and (not buy_flag)):#......places "BUY " order if PCR crosses lower stoploss #absolute value
		flag = 1
		buy_flag = False
		sell_flag = False
		pro = future_cost - transaction_start_price
		order_details = [1,"Buy" , "LSB crossed" , "stoploss executed abs" , "position closed"]		
				
	elif (mAvg_cross_down and flag==0 and (not sell_flag)):#.....places "SELL" order if PCR crosses mAvg from high to low to close a trade
		flag = 1
		sell_flag = False
		buy_flag = False
		pro = -(Data['future'][i] - transaction_start_price)
		order_details = [-1,"Sell" , "mAvg crossed (h to l)" , "0" , "position closed"]
					
	elif(USL_cross and flag==0 and (not sell_flag)):# ..places "SELL" order if PCR crosses upper stoploss band to close a trade
		flag = 1
		sell_flag = False
		buy_flag = False
		pro = -(Data['future'][i] - transaction_start_price)
		order_details = [-1,"Sell" , "USB crossed" , "stoploss executed" , "position closed"]
	
	elif((-future_cost + transaction_start_price) > abs_SL and flag==0 and (not sell_flag)):# ..places "SELL" order if PCR crosses upper stoploss #absolute value
		flag = 1
		sell_flag = False
		buy_flag = False
		pro = -(Data['future'][i] - transaction_start_price)
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

Data['placed_order'] = pd.Series(order) #...............................converting list to pandas series
Data['cost'] = -(Data['placed_order'].multiply(Data['future'])) *500# ..cost at each transaction
Data['out'] = Data['cost'].cumsum()# ...................................out is the cumulative cost profit/loss after transactions till now
Data['buy_sell'] = pd.Series(buy_sell)
Data['profit'] = -pd.Series(profit) * 500
Data['stoploss'] = pd.Series(stoploss)
Data['trade_cause']  = pd.Series(trade_cause)
Data['mtm'] = pd.Series(mtm)
print Data['out']



output = pd.DataFrame() #....final output to be stored in excel file
output['date'] = Data1['Date']
output['Close'] = Data['future']
output['PCR'] = Data['PCR']
output['placed_order'] = Data['placed_order']
output['buy_sell'] = Data['buy_sell']
output['trade_cause'] =  Data['trade_cause']
output['PnL'] = Data['profit']
output['mtm'] = Data['mtm']
output['stoploss'] = Data['stoploss']
output['Cash Account'] = Data['out']
output.to_excel('PCR_SL_output.xlsx', sheet_name='Sheet1')

#plt.plot(order)
plt.plot(Data['PCR'])
plt.plot(Data['mAvg'])
plt.plot(Data['UBB'])
plt.plot(Data['LBB'])
#plt.plot(Data['out'])
plt.show()


#Copyright QuantInsti Quantitative Learning Private Limited
