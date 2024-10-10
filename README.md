# Stock-Movement-Analysis
## This Project First Gets all Stocks/ETf's that File with the SEC
# Next it analyses the past 30 days Stock Movement for Each one
# Out of All Stock if finds each stock that has had a Difference of 20% or greater for their high and low for the day
# It then Records this to a Postgres Database with the ticker name, date, high,low, and percentage difference
# I then have another file that you can use matplotlib to see the difference in stock prices and their difference in percentage for the day
# As Expected there is a high corelation with pennystocks having the highest difference
# The Next file Then takes these stocks and dates and extracts Each One That has a Stock Price Greater than any dollar amount, in the code it has 10 dollars
# It then takes each of these stocks, gets the unique data of first occurance in the database traces back 20 days
# It then records the volume and average volume for 20 to 5 days back then records the volume and average volume for 5 to present back.
# it then compares these volumes and sees the corelation within the rise of volume corelated to the percentage difference in the stocks high and low
