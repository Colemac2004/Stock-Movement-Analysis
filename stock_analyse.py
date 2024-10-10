import pandas as pd
import psycopg2
import requests
import yfinance as yf
from datetime import datetime, timedelta


#connect to database
conn = psycopg2.connect(
    dbname='Stock_Movement',
    user='postgres',
    password='J7BFG12749!',
    host='localhost', 
    port='5432'        
)
cur = conn.cursor()


#define function for selecting low
def select_from_database(minimum_low):
    #query
    select_query=f"SELECT * FROM stocks WHERE low > {minimum_low};"
    cur.execute(select_query)
    #now fetch
    return cur.fetchall()

#function for adding data to dataframe
def add_to_data_frame(data,df):
    for x in data:
        new_row=pd.DataFrame({'date':[x[2]],'ticker':[x[1]],'percentage':[x[9]]})
        df=pd.concat([df,new_row],ignore_index=True)
    return df

#function for getting date on a specifc number of days back
def get_date_back(date,days_back):
    #define date format
    date_format="%Y-%m-%d"
    date_object=datetime.strptime(date,date_format)
    #initalize count of weekdays
    count=0
    current_date=date_object
    #loop until come to number of desired weekdays
    while count < days_back:
        current_date-=timedelta(days=1)
        #check if current days if a weekday
        if current_date.weekday()<5:
            count+=1
            
    return current_date.date()

#function for getting volume data
def get_volume_data(ticker,start_date,end_date):
    stock_data=yf.Ticker(ticker)
    data=stock_data.history(start=start_date, end=end_date)
    #get volume
    volume=data['Volume']
    #okay now we have to turn into array
    volume_array=[]
    for x in volume:
        volume_array.append(x)
    return volume_array

def average_volume_data(array):
    if len(array)==0:
        print("Volume array is empty")
        return 0
    return sum(array)/len(array)
#get stock data
data=select_from_database(10)

#declare dataframe
stock_df=pd.DataFrame(columns=['date','ticker','percentage'])

#add data to dataframe
response=add_to_data_frame(data,stock_df)

#define ticker_dates
ticker_dates={}

#now we should go through each one by one
for x in range(0,response.shape[0]):
    #okay now we can define the date ticker and percentage for each iteration
    date=response.iloc[x]['date']
    ticker=response.iloc[x]['ticker']
    percentage=response.iloc[x]['percentage']
    #now we need to append unqiue stocks
    if ticker not in ticker_dates:
        ticker_dates[ticker]=date
    else:
        if date < ticker_dates[ticker]:
            ticker_dates[ticker]=date


#iterating through unique tickers and dates
for ticker,date in ticker_dates.items():
    #get date for 20 days back
    days_back_20=get_date_back(date,20)
    #now get date for 5 days back
    days_back_5=get_date_back(date,5)

    #okay now we have to get volume data
    volume_20_array=get_volume_data(ticker,days_back_20,days_back_5)
    volume_5_array=get_volume_data(ticker,days_back_5,date)
    #check for volume data
    if not volume_20_array:
        print(f"{ticker}: No volume data")
    if not volume_5_array:
        print(f"{ticker}: No Volume Data")
    #average volume data
    average_volume_20=average_volume_data(volume_20_array)
    average_volume_5=average_volume_data(volume_5_array)
    #okay now define other metrics
    if average_volume_5 !=0 and average_volume_20 !=0:
        subtracted_average_volume=average_volume_5-average_volume_20
        print(subtracted_average_volume)
#close
cur.close()
conn.close()

