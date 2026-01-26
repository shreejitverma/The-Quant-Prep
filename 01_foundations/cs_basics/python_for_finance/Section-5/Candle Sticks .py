
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Plotting Candle sticks 
# 
# The following code will help you to plot an interactive graph of the S&P 500 index using candlesticks.

# In[ ]:


from iexfinance import get_historical_data 
from datetime import datetime

start = datetime(2017, 1, 1) # starting date: year-month-date
end = datetime(2018, 5, 13) # ending date: year-month-date

df = get_historical_data('SPY', start=start, end=end, output_format='pandas') 
df.head()


# In[ ]:


# Importing the necessary packages

import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.finance import candlestick_ohlc
from bokeh.plotting import figure, show, output_file


# In[ ]:


# Indexing 
import pandas as pd
w = 12*60*60*1000 # half day in ms
df.index = pd.to_datetime(df.index)


# ## Remember:
# 
# 1. If the opening price is greater than the closing price then a green candle stick has to be created to represent the day. 
# 2. If the opening price is less than the closing price then a red candlestick is to be created to represent the day.
# 1. We will use 'inc' and 'dec' as the varieble to capture this facr further in the code

# In[ ]:


inc = df.close > df.open
dec = df.open > df.close


# In[ ]:


# The various 'interactions' we want in our candlestick graph. This is an argument to be passed in figure () from bokeh.plotting

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

# Pan: It helps you pan/move the plot

# Wheel Zoom: You can zoom in using the wheel of your mouse

# Box Zoom: You can zoom in by creating a box on the specific area of the plot. Use the mouse, click and drag to create the box

# Reset: If you want to reset the visualisation of the plot

# Save: Saving the plot (entire or the part which you want) as an image file


# In[ ]:


# Passing the arguments of our bokeh plot

p = figure(x_axis_type="datetime", tools= TOOLS, plot_width=1000, title="SPY Candlestick")


# In[ ]:


from math import pi

# The orientation of major tick labels can be controlled with the major_label_orientation property.
# This property accepts the values "horizontal" or "vertical" or a floating point number that gives
# the angle (in radians) to rotate from the horizontal.

p.xaxis.major_label_orientation = pi/4


# In[ ]:


# Alpha signifies the floating point between 0 (transparent) and 1 (opaque).
# The line specifies the alpha for the grid lines in the plot.

p.grid.grid_line_alpha = 0.3


# In[ ]:


# Configure and add segment glyphs to the figure

p.segment(df.index,df.high,df.index,df.low,color="red")


# In[ ]:


# Adds vbar glyphs to the Figure

p.vbar(df.index[inc],w,df.open[inc],df.close[inc], fill_color="#1ED837",line_color="black")
p.vbar(df.index[dec],w,df.open[dec],df.close[dec], fill_color="#F2583E",line_color="black")


# In[ ]:


# Generates simple standalone HTML documents for Bokeh visualization

output_file("candlestick.html", title="candlestick.py example")  


# In[ ]:


# The graph will open in another tab of the browser

show(p)

# The code ends here


# ### In the upcoming iPython notebook:
# 
# We will learn about Functions in Python
# 
# Happy Learning!
