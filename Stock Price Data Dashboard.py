#PART 1 - IMPORT NECESSARY TOOLS AND SETUP GRAPH

# Import all necessary Python libraries
from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file

#Time span of analysis
start = datetime.datetime(YYYY,MM,DD)
end = datetime.datetime(YYYY,MM,DD)

#Create a dataframe containing our stock prices from start and end date
df = data.DataReader(name='Insert Stock Symbol Here', data_source = "yahoo", start=start, end=end)

#Create a graph 
p = figure(x_axis_type='datetime',width =1000,height=300, sizing_mode='scale_width')

#Graph title
p.title.text = "Stock Price Graph"

#----------------------------------------------------------------------------------#
#PART 2 - VISUALIZE CANDLESTICK GRAPH USING BOKEH RECTANGLES 

#Define a function that shows if the stock price increased, decreased, or remained stagnant for a given day.  
def incr_decr(c,o):
    
    if c > o:
        value = 'Increase'
    elif c < o:
        value = 'Decrease'
    else:
        value = 'Equal'
    return value

#Create a new column in the dataframe showing if the stock price increased, decreased, or remained stagnant.
df['Status'] = [incr_decr(c,o) for c,o in zip(df.Close,df.Open)]

#Central point of rectangle 
df['Middle'] = (df.Open+df.Close)/2

#Height of rectangle
df['Height'] = abs(df.Open-df.Close)

#Width of rectangle defined by 12 hours and converted to milliseconds
hours = 12*60*60*1000

#Create vertical segments for highest and lowest points of a rectangle
p.segment(df.index, df.High, df.index, df.Low, color = 'Black')

#Create rectangles for price increases
p.rect(df.index[df.Status == 'Increase'], df.Middle[df.Status == 'Increase'], hours, 
       df.Height[df.Status == 'Increase'],fill_color='green',line_color='black')

#Create rectangles for price decreases
p.rect(df.index[df.Status == 'Decrease'], df.Middle[df.Status == 'Decrease'], hours, 
       df.Height[df.Status == 'Decrease'],fill_color='red',line_color='black')


#Create output file and display graph in webpage
output_file("SPDD.html")
show(p)

