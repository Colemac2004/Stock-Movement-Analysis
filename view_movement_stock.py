import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

#psycopg2
conn = psycopg2.connect(
    dbname='Stock_Movement',
    user='postgres',
    password='',
    host='localhost', 
    port='5432'        
)
cur = conn.cursor()


#Select * From database
def get_data(df):
    #define and execute
    all_query="SELECT * FROM stocks"
    cur.execute(all_query)
    #fetch and set df
    data_response=cur.fetchall()
    return data_response

def get_pieces(df):
    data=get_data(df)
    #now we make new row in loop for each iteration and concat
    for x in data:
        new_row=pd.DataFrame({'lows': [x[4]],'percent':[x[5]]})
        df=pd.concat([df,new_row],ignore_index=True)
    return df





#okay so we have to make a dataframe from our postgres database
#initalize low dataframe
df=pd.DataFrame(columns=['lows','percent'])

#get lows and percent in dataframe
df=get_pieces(df)


#math plot lib time

#figure size
plt.figure(figsize=(18, 12)) 
#define scatter
plt.scatter(df['lows'],df['percent'],color='blue',s=100)
#labels 
plt.xlabel('Low Prices')
plt.ylabel('Percent Changes')
#title
plt.title('Low Prices vs Percent Changes')
plt.grid()
plt.show()

print(df)
cur.close()
conn.close()
