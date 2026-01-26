
import pandas as pd
import numpy as np
import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import plotly    
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import warnings
warnings.filterwarnings('ignore')
'''
# Function to backtest any strategy by using parameter         
    #Dataframe, 
    #strategy_type(long/short),entry_criteria,exit_criteria
    #positional_field ,price_field(example Close price),stoploss_pct(stop loss pct),target_pct,only_profit(should wait for trade to be in profit True/False)
'''
def backtest_strategy_stoploss(df, strategy_type,lst_entry_criteria,lst_exit_criteria, positional_field,price_field,stoploss_pct,target_pct,only_profit):
    df['buy_price']=0.0000
    df['sell_price']=0.0000
  
    df['buy_time']=None
    df['sell_time']=None
    exit_reason_field=positional_field+'_exit_flag'
    df[positional_field]=0
    df[exit_reason_field]=''
    pos=0

    last_buy_price=0.00
    last_sell_price=0.00
    
    for d in range(0,len(df)):
        entry_flag=lst_entry_criteria[d]
        exit_flag=lst_exit_criteria[d]
        curr_price=df[price_field].iloc[d]
        curr_time=df.index[d]
        stoploss_exit=False
        target_exit=False
        only_profit_exit=False
        exit_reason=''
        
        if stoploss_pct!=0:
            if (strategy_type=='long')&(last_buy_price>0):
                if ((curr_price-last_buy_price)*100/last_buy_price)<stoploss_pct:
                    stoploss_exit=True
                    exit_reason='SLM'
            elif (strategy_type=='short')&(last_sell_price>0):    
                if ((last_sell_price-curr_price)*100/curr_price)<stoploss_pct:
                    stoploss_exit=True
                    exit_reason='SLM'
                    
        if target_pct!=0:
            if (strategy_type=='long')&(last_buy_price>0):
                if ((curr_price-last_buy_price)*100/last_buy_price)>target_pct:
                    target_exit=True
                    exit_reason='TRM'
            elif (strategy_type=='short')&(last_sell_price>0):    
                if ((last_sell_price-curr_price)*100/curr_price)>target_pct:
                    target_exit=True
                    exit_reason='TRM'

        if only_profit==True:
            if (strategy_type=='long')&(last_buy_price>0):
                if ((curr_price-last_buy_price)*100/last_buy_price)>0:
                    only_profit_exit=True
            elif (strategy_type=='short')&(last_sell_price>0):    
                if ((last_sell_price-curr_price)*100/curr_price)>0:
                    only_profit_exit=True
        else:
            only_profit_exit=True

        if exit_flag:
            exit_reason='ECM'
            
        if entry_flag&(pos==0) :
             if strategy_type=='long':
                df['buy_price'].iat[d]= df[price_field].iloc[d]
                last_buy_price=df[price_field].iloc[d]
                df[positional_field].iat[d]=1
             elif strategy_type=='short':
                df['sell_price'].iat[d]= df[price_field].iloc[d]
                last_sell_price=df[price_field].iloc[d]
                df[positional_field].iat[d]=-1
             pos=1
        elif (exit_flag|stoploss_exit|target_exit)& only_profit_exit & (pos==1) :
             df[exit_reason_field].iat[d]=exit_reason
             
             if strategy_type=='long':
                df['sell_price'].iat[d]= df[price_field].iloc[d]
                last_sell_price=df[price_field].iloc[d]
                df[positional_field].iat[d]=-1
             elif strategy_type=='short':
                df['buy_price'].iat[d]= df[price_field].iloc[d]
                last_buy_price=df[price_field].iloc[d]
                df[positional_field].iat[d]=1
             pos=0

    df_temp=df[df[positional_field]!=0].copy()
    
    df_temp['buy_time']=df_temp.index
    df_temp['sell_time']=df_temp.index

    df_buy=df_temp[df_temp.buy_price>0][['buy_price','buy_time']]
    df_buy.reset_index(drop=True,inplace=True)
    
    df_sell=df_temp[df_temp.sell_price>0][['sell_price','sell_time']]
    df_sell.reset_index(drop=True,inplace=True)
    
    long= pd.concat([df_buy,df_sell],axis=1,copy=True)
    
    if len(long)>0:
        if ~(long['sell_price'].iloc[-1]>0):
            long['sell_price'].iat[-1]=curr_price
            long['sell_time'].iat[-1]=curr_time
            
    
    long["returns"]=(long["sell_price"]-long["buy_price"])*100/long["buy_price"]
    long['cum_returns']=(long['sell_price']/long['buy_price']).cumprod()
    #long['investment_period']=(long['sell_time']-long['buy_time'])

    short= pd.concat([df_buy,df_sell],axis=1,copy=True)
    
    if len(short)>0:
        if ~(short['buy_price'].iloc[-1]>0):
            short['buy_price'].iat[-1]=curr_price
            short['buy_time'].iat[-1]=curr_time
            
    short["returns"]=(short["sell_price"]-short["buy_price"])*100/short["buy_price"]
    short['cum_returns']=(short['sell_price']/short['buy_price']).cumprod()
    #short['investment_period']=(short['buy_time']-short['sell_time'])
    
    if strategy_type=='long':
        return df,long
    else:
        return df,short

'''
# Function to generate backtest reports
'''
def backtest_reports_local(df_summary,lot_size,trx_charge):
    #print("investment period", df_summary['investment_period'].sum())
    #print("number of transactions", df_summary['investment_period'].count())
    print("Sum of returns in %", df_summary['returns'].sum())
    print("Average returns per transaction in %", df_summary['returns'].mean())
    print("Absolute returns", df_summary['returns_abs'].sum())
    print("Absolute returns per trx", df_summary['returns_abs'].sum()/df_summary['returns_abs'].count())
    print("Max drawdown for a trx", df_summary[df_summary.returns_abs<0]['returns_abs'].min())
    print("Max returns for a trx", df_summary[df_summary.returns_abs>0]['returns_abs'].max())
    print("Losing trx", df_summary[df_summary.returns_abs<0]['returns_abs'].count())
    print("Winning trx", df_summary[df_summary.returns_abs>0]['returns_abs'].count())
    print("Win/Lose ratio ", (df_summary[df_summary.returns_abs>0]['returns_abs'].count())/(df_summary[df_summary.returns_abs<0]['returns_abs'].count()))
    
    df_summary.index=df_summary.buy_time
    df_summary['returns2']=np.round((np.int64(df_summary['returns']/.5))*.5,0)
    
    g1=df_summary[['returns2']].cumsum().plot(figsize=(9,6))
    #fig.autofmt_xdate()
    #ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    plt.tight_layout()

    plt.show(g1)

    plt.title("Percentage Returns vs Count of transactions")
    
    g3=sns.countplot(x="returns2",
     data=df_summary)
    
    plt.show(g3)

'''
Function to fetch data for the algorithm 
'''

def fetch_data() :
    path='/Users/sunilguglani/Downloads/'
    path='/Users/sunilguglani/anaconda3/lib/Algos/Algo_Trading_Webinar/'
    filename='Chana Gram Futures Historical Data_2.csv'
    df=pd.read_csv(path+filename,header=0)
    df.rename(columns={'Price':'Close'}, inplace=True)
    df["Date"]=pd.to_datetime(df.Date)
    df.sort_values(by='Date', inplace=True)
    df.index=df.Date
    for pfield in ['Open','High','Low','Close']:
        df[pfield] = pd.to_numeric(df[pfield].str.replace(',', ''))
    return df

'''
Function to write buy/sell signals for the algo
'''
def bb(df_temp,price_field,strategy_type,roll,low,up):
    level_low=low
    level_up=up
    rollback=roll
    df_temp['sma']=df_temp[price_field].rolling(rollback).mean()
    df_temp['std']=df_temp[price_field].rolling(rollback).std()
    df_temp['level_low']=(df_temp['sma']-level_low*df_temp['std'])
    df_temp['level_up']=(df_temp['sma']+level_up*df_temp['std'])
    
    if strategy_type=='long':
        boll_entry=(df_temp['level_low']>df_temp[price_field])
        boll_exit=(df_temp['level_up']<df_temp[price_field])

    if strategy_type=='short':
        boll_exit=(df_temp['level_low']>df_temp[price_field])
        boll_entry=(df_temp['level_up']<df_temp[price_field])

    return df_temp,boll_entry,boll_exit

'''
Function to draw candlestick chart for the script
'''
def draw_cndl_chart(df):
    trace = go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
    
                    close=df['Close'])
    data2 = [trace]
    
    plot(data2)

'''
main Function 
'''

def bb_backtest_positional(script,lot_size,trx_charges,slippages,roll,low,up):

    summary_min_grand=pd.DataFrame()
    df_temp_grand=pd.DataFrame()

    df=fetch_data()
        
    #draw_cndl_chart(df)

    for strat_type in ['long','short']:
        df_temp=df.copy()
        price_field='Close'
        
        strategy_type=strat_type
        df_temp,boll_entry,boll_exit=bb(df_temp,price_field,strategy_type,roll,low,up)

        if strategy_type=='long':
            final_entry=boll_entry
            final_exit=boll_exit
        elif strategy_type=='short':    
            final_entry=boll_entry
            final_exit=boll_exit
        
        positional_field='pos_bb'
        price_field='Close'
        stoploss_pct=-2
        target_pct=10
        only_profit=False
        
        df_temp,summary_min=backtest_strategy_stoploss(df_temp, strategy_type,list(final_entry),list(final_exit), positional_field,price_field,stoploss_pct,target_pct,only_profit)
        
        summary_min['returns_abs']=(summary_min['sell_price']-summary_min['buy_price'])*lot_size
        summary_min['returns_abs']=summary_min['returns_abs']-trx_charges
        summary_min['strat_type']=strat_type
        
        summary_min_grand=summary_min_grand.append(summary_min)
        df_temp_grand=df_temp_grand.append(df_temp)
    return summary_min_grand,df_temp_grand



'''
invoking the main Function 
'''
script='Chana'
print('**************BACKTEST RESULTS OF : ', script, '************************')
lot_size=1
trx_charges=0
bid_ask_parity=0
slippages=bid_ask_parity

'''
invoking the main Function 
'''
def Combination(lstA,lstB,lstC):
    lstAll=[]
    for a in lstA:
        for b in lstB:
            for c  in lstC:
              lstAll.append([a,b,c])
    return lstAll

# Function to generate mini backtest reports
print("roll,low,up,lst_strat_type,returns,mean_returns,max_dd,win_lose_r")
def backtest_reports_local2(roll,low,up,df_summary,lot_size,trx_charge):
    print(roll,low,up, round(df_summary['returns'].sum(),2),round(df_summary['returns'].mean(),2),round(df_summary[df_summary.returns_abs<0]['returns'].min(),2),
    round((df_summary[df_summary.returns_abs>0]['returns'].count())/
          (df_summary[df_summary.returns_abs<0]['returns'].count()),2))
    
    return (df_summary['returns'].sum(),
    df_summary['returns'].mean(),
    df_summary[df_summary.returns_abs<0]['returns'].min(),
    (df_summary[df_summary.returns_abs>0]['returns'].count())/(df_summary[df_summary.returns_abs<0]['returns'].count()))

roll_v=[12,17,20,22,23,24,28,34,38,40]
low_v=[1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8,3]
up_v=[1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8,3]

lstAll=Combination(roll_v,low_v,up_v)
lstCols=['roll','low','up','returns','avg_returns','max_loss','win_lose']
df_optimizor=pd.DataFrame()

for l in lstAll:
    roll,low,up=l[0],l[1],l[2]
    summary_min_grand,df_temp_grand=bb_backtest_positional(script,lot_size,trx_charges,slippages,roll,low,up)
    #summary_min_grand['investment_period']=np.abs(summary_min_grand['sell_time']-summary_min_grand['buy_time'])
    returns,avg_returns,max_loss,win_lose= backtest_reports_local2(roll,low,up,summary_min_grand,1,0)
    df_t=pd.DataFrame([roll,low,up,returns,avg_returns,max_loss,win_lose])
    df_optimizor=df_optimizor.append(df_t.T)
    
df_optimizor.columns=lstCols
df_optimizor.dropna(inplace=True)
max_pct_returns=df_optimizor['returns'].max()

optimized_roll=int(df_optimizor[df_optimizor.returns==max_pct_returns]['roll'].iloc[0])
optimized_low=float(df_optimizor[df_optimizor.returns==max_pct_returns]['low'].iloc[0])
optimized_up=float(df_optimizor[df_optimizor.returns==max_pct_returns]['up'].iloc[0])

print('returns,optimized_roll,optimized_low,optimized_up')
print(round(max_pct_returns,2),optimized_roll,optimized_low,optimized_up)

summary_min_grand,df_temp_grand=bb_backtest_positional(script,lot_size,trx_charges,
                                                       slippages,optimized_roll,optimized_low,optimized_up)

backtest_reports_local(summary_min_grand,1,0)


df_temp_grand['signals']=np.where((df_temp_grand['buy_price']!=0),1,
                                     np.where((df_temp_grand['sell_price']!=0),-1,0))

df_temp_grand.sort_index(inplace=True)
df_temp_grand.plot(y=['signals','level_up','level_low','Close'],
                   secondary_y=['signals'], figsize=(10,8))
