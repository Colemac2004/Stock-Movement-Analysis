import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
import time
#function for getting tickers
def make_request():
    headers={"User-Agent":"coalbucket23@gmail.com"}
    company_ticker_json=requests.get("https://www.sec.gov/files/company_tickers.json",headers=headers)
    return company_ticker_json

#function for turning into dataframe
def dataframe_json(df):
    df=pd.DataFrame(df.json())
    return df

def dataframe(df):
    df=pd.DataFrame(df)
    return df

#function for existing in yahoo finiance database
def finance_exists(ticker):
    try:
        stock=yf.Ticker(ticker)
        #check if it contains symbol
        if 'symbol' in stock.info and stock.info['symbol'] == ticker:
            return True
        else:
            return False
    except Exception as e:
        print(f"an error occurred while checking ticker {ticker}: {e}")
        return False

#function for getting last 30 days info
def last_30_days_data(ticker):
    #define todays date
    today_date=datetime.now()
    start_date=today_date-timedelta(days=30)
    data=yf.download(ticker,start=start_date,end=today_date)
    return data

#function to find the last indexed stock so i dont have to start the process all over
def check_last_stock():
    #first we need to get the number of stocks in database
    cur.execute("SELECT count(*) FROM stocks")
    result=cur.fetchone()
    count=result[0]
    #now we need to get the last stock ticker
    cur.execute("SELECT ticker FROM stocks WHERE id=%s",(count,))
    last_stock_ticker=cur.fetchone()
    last_stock_ticker=last_stock_ticker[0]
    #okay now we need to find what number this stock is in the company tickers .json
    company_tickers=make_request()
    #turn into df
    company_df=dataframe_json(company_tickers)
    #find the id of a specific ticker
    for x in range (0,company_df.shape[1]):
        ticker=company_df[str(x)]['ticker']
        if ticker == last_stock_ticker:
            return x
        else:
            pass
    return 0
        




#for psycopg2, connect to database
conn = psycopg2.connect(
    dbname='Stock_Movement',
    user='postgres',
    password='',
    host='localhost', 
    port='5432'        
)
cur = conn.cursor()




#get company tickers
company_tickers=make_request()
#turn into dataframe
company_tickers=dataframe_json(company_tickers)

#check for last indexed stock
#index=int(check_last_stock())
#print(index)
#for loop to loop through all columns
for x in range(0,company_tickers.shape[1]):
    #get ticker
    ticker=company_tickers[str(x)]['ticker']
    #now check if it exists in yahoo finiance
    if finance_exists(ticker) == True:
        #if exists now get the info for last 30 days
        data=last_30_days_data(ticker)
        #turn into datafrae
        data_df=dataframe(data)
        
        #for this stock get each date for the last 30 days
        for i in range(0,30):
            #got the date
            date=((datetime.now()-timedelta(days=i)).date())
            #now get the high and low for that date
            try:
                """Use Try to Handle weekends and holidays"""
                high=float(data_df['High'][str(date)])
                low=float(data_df['Low'][str(date)])
                volume=int(data_df['Volume'][str(date)])
                open_price=float(data_df['Open'][str(date)])
                close_price=float(data_df['Close'][str(date)])
                adj_close=float(data_df['Adj Close'][str(date)])
                #calculate the difference as a percentage of total stock price
                percent=(high-low)/low
                percent_rounded=round(percent, 2)
                #now we do a if statement for if the percentage difference between high and low is .2 or above
                if percent_rounded >= 0.2:
                    """now we have to add the date stock and percentage to database"""
                    #define database query and execute and commit
                    insert_query="INSERT INTO stocks (ticker,date,high,low,open_price,close_price,volume,adj_close,percentage_change) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    try:
                        cur.execute(insert_query,(ticker,date,high,low,open_price,close_price,volume,adj_close,percent_rounded))
                        conn.commit()
                        time.sleep(.2)
                        print(f"Inserted Into Database: {percent_rounded}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    pass
            except Exception as e:
                pass

    else:
        pass
cur.close()
conn.close()