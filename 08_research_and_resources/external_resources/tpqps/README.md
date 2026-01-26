
<img src="http://hilpisch.com/tpq_logo.png" alt="The Python Quants" width="35%" align="right" border="0"><br>

# tpqps

## Streaming Plots with Plotly

`tpqps` is a wrapper class for the streaming API of http://plot.ly.

The package is authored and maintained by The Python Quants GmbH. &copy; Dr. Yves J. Hilpisch. MIT License.

## Disclaimer

The `tpqps` package is intended as a technological illustration only. It comes with no warranties or representations, to the extent permitted by applicable law.

## Installation

Installing from source via `Git` and `Github`:

    git clone https://github.com/yhilpisch/tpqps
    cd tpqps
    python setup.py install
    
Using `pip` in combination with `Github`:

    pip install git+git://github.com/yhilpisch/tpqps

## Connection

In order to connect to the API, you need to have an **account with Plotly** (https://plot.ly). Once logged in to you account, you can create an API key and ans streaming API tokens. These are expected to be stored in a configuration file, with a filename of `plotly.cfg`, for instance, as follows:

    [plotly]
    user_name = user_name_...
    api_key = api_key_...
    api_tokens = token1,token2,token3,token4,...

You can then create a streaming plot object as follows.


```python
import tpqps
```


```python
ps = tpqps.tpqps('plotly.cfg', 'Plot Title')
```


```python
[_ for _ in ps.__dir__() if not _.startswith('__')]
```




    ['user_name',
     'api_key',
     'api_tokens',
     'sources',
     'source_id',
     'traces',
     'data',
     'maxpoints',
     'token_number',
     'context',
     'poller',
     'title',
     'cols',
     'rows',
     'subplots',
     'layout',
     'plot_url',
     'fig',
     'init_plot',
     'add_layout',
     'add_data_source',
     'add_trace',
     'set_max_points',
     'get_plot_url',
     'start_streaming',
     'add_socket',
     'set_subplot_title',
     'set_subplot_specs']



## Documentation

More details will follow that describe the usage of `tpqps`.

<img src="http://hilpisch.com/tpq_logo.png" alt="The Python Quants" width="35%" align="right" border="0"><br>

<a href="http://tpq.io" target="_blank">http://tpq.io</a> | <a href="http://twitter.com/dyjh" target="_blank">@dyjh</a> | <a href="mailto:training@tpq.io">training@tpq.io</a>
