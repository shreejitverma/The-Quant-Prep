#importing required packages
import pandas as pd
import quandl
import matplotlib.pyplot as plt
import math
def fetch_data(string1,string2,string3,filename):
	w = quandl.get(string1,authtoken = string2, start_date = string3)
	w.to_csv(filename)
	w = pd.read_csv(filename)
	return w

#the data pulled from quandl and stored locally for faster execution
Data1 = fetch_data( "CHRIS/CME_SP1", "mq-W7Z-QXBDZ1MxaN-Vy", "2014-12-12" ,"local_future.csv")
Data = fetch_data("CBOE/VIX", "zaYDtiD-pcyPCwWr3_Py", "2014-12-12","VIX_data.csv")

Data['future'] = Data1['Last']
Data['VIX'] = Data['VIX Close']

mtm = list()
order_details = list()
order = list()#.........................a list which stores the transactions ( -1:"BUY" , 1:"SELL" , 0:"DO NOTHING")
profit = list()
buy_sell = list() #.....................a list which tells buy/sell in words!
stoploss = list()
pro = 0 # profit( which happens( +/-) at the end of each transaction )
v=0 #.................................. V is the buying price and 3/4 % above v will be the selling price
thresh = 22  #..........................VIX threshold for placing a buy order 
change_1 = 5 #..........................% above which to sell for a profit
change_2 = 5 #..........................% below which to sell in a stoploss
buy_flag = False#.......................indicates if last order was a buy 
sell_flag = True # ....................indicates if last order is a sell
s = Data['future'].size#................size of the VIX dataset
c_1 = (1 + (change_1)/float(100) ) #....c_1 is the value above which the sell order will execute in a successful trade
c_2 = (1 - (change_2)/float(100) ) #....c_2 is the value below which a sell order will execute in  a stoploss

#buy/sell order logic begins=======================================================================================================
for i in range(s):
	pro = 0

	if(Data['VIX'][i] >=thresh and (not buy_flag)): #........IF THRESHOLD IS CROSSED THEN "BUY"
		order_details = [-1,"Buy" , "0", "position taken"]
		buy_flag = True
		sell_flag =False
		v = Data['future'][i] #..............................PRICE AT WHICH WE "BUY"                       
	
	elif(Data['future'][i] >= (c_1)*v and (not sell_flag)):#...IF future price is c_1 times v, then "SELL" ( profit )
		buy_flag = False
		sell_flag = True
		pro = (Data['future'][i] - v) #profit= (selling price - the buying price)
		order_details = [1,"Sell" , "0", "position closed"]
		
	elif(Data['future'][i] <= (c_2)*v and (not sell_flag)):#...IF future price is c_2 times v , then "SELL" ( loss )
		buy_flag = False
		sell_flag = True
		pro = (Data['future'][i] - v)
		order_details = [1,"Sell" , "Stoploss executed", "position closed"] 
	else:
		if(buy_flag ==1): x = (Data['future'][i] - v ) * 500* 2
		else: x = "0"
		order_details = [0,"No trade" , "0", x]
	
	profit.append(pro)
	order.append(order_details[0])
	buy_sell.append(order_details[1])
	stoploss.append(order_details[2])
	mtm.append(order_details[3])

	
#buy/sell logic ends================================================================================================================

Data['stoploss'] = pd.Series()
Data['mtm'] = pd.Series(mtm)
Data['placed_order'] = pd.Series(order)
Data['stoploss'] = pd.Series(stoploss)
Data['buy_sell'] = pd.Series(buy_sell)
Data['profit'] = pd.Series(profit) *500*2
Data['cost'] = (Data['placed_order'].multiply(Data['future'])) *500*2 #the cost at each transaction : buy/sell * (future price)
Data['out'] = Data['cost'].cumsum() # out is the cumulative cost... profit/loss after transactions till now
print (Data['out'])

output = pd.DataFrame() #....final output to be stored in excel file
output['date'] = Data['Date']
output['Close'] = Data['future']
output['VIX'] = Data['VIX']
output['placed_order'] = Data['placed_order']
output['buy_sell'] = Data['buy_sell']
output['profit'] = Data['profit']
output['mtm'] = Data['mtm']
output['account'] = Data['out']
output['stoploss'] = Data['stoploss']
output.to_excel('VIX_SL_output.xlsx', sheet_name='Sheet1')

#plt.plot(Data['placed_order'] * 1000)
plt.plot(Data['out'])
#plt.plot(Data['future'])
#plt.plot(Data['VIX'])
plt.show()
