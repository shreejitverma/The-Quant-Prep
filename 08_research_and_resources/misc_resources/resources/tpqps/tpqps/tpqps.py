#
# Python Module
# with Wrapper Class
# for Plotly Streaming API
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
# Autor: Michael Schwed
#
import zmq
import datetime
import configparser
import plotly.plotly as ply
import plotly.tools as plyt
from plotly.graph_objs import Scatter, Bar

NO_TOKENS_ERROR = '''Can not find any streaming tokens, please
generate and add streaming tokens to the configuration file.'''

NO_TOKENS_LEFT_ERROR = '''No stream token left,
to proceed add new tokens on your plotly account and
add them to the configuration file.'''

NO_CRED_ERROR = 'Credentials are missing in the configuration file.'


class tpqps(object):
    ''' A class for the easy implementation of streaming plots with Plotly.
    '''

    def __init__(self, config_file, title, filename='', subplot_rows=1,
                 subplot_columns=1, maxpoints=50, token_number=0):
        ''' Returns a ploty_stream instance.

        Parameters
        ==========
        title: str
            the title of the plot
        subplot_rows: int
            number of subplot rows, default is 1
        subplot_columns: int
            number of subplot columns, default is 1
        maxpoints: int
            the number of points a trace contains, default is 50
        token_number: int
            the position of the first streaming token in the token list
            used by the instance, default is 0
        '''
        config = configparser.ConfigParser()
        config.read(config_file)
        self.user_name = config['plotly']['user_name']
        self.api_key = config['plotly']['api_key']
        if self.user_name == '' or self.api_key == '':
            raise IOError(NO_CRED_ERROR)
        ply.sign_in(self.user_name, self.api_key)

        self.api_tokens = list(config['plotly']['api_tokens'].split(','))
        if len(self.api_tokens) == 0:
            self.api_tokens = self.class_stream_tokens
            if len(self.api_tokens) == 0:
                raise IOError(NO_TOKENS_ERROR)

        self.filename= filename
        self.sources = dict()
        self.source_id = 0
        self.traces = list()
        self.data = list()
        self.maxpoints = maxpoints
        self.token_number = token_number
        self.context = zmq.Context()
        self.poller = zmq.Poller()
        self.title = str(title)
        self.cols = subplot_columns
        self.rows = subplot_rows
        self.subplots = dict()
        self.layout = dict()
        self.plot_url = ''
        self.fig = None
        for r in range(self.rows):
            for c in range(self.cols):
                self.subplots[r * self.cols + c] = subplot(r, c)
        self.add_layout(layout={'title': self.title})

    def init_plot(self, auto_open=False):
        ''' Initializes the plot and returns the plot url;
            is called by either start_streaming or get_plot_url.
        '''
        if len(self.traces) == 0:
            raise ValueError('No traces given')
        specs = list()
        titles = list()
        for r in range(self.rows):
            specs_r = list()
            for c in range(self.cols):
                specs_r.append(self.subplots[r * self.cols + c].spec)
                titles.append(self.subplots[r * self.cols + c].title)
            specs.append(specs_r)

        self.fig = plyt.make_subplots(rows=self.rows, cols=self.cols,
                                      specs=specs, subplot_titles=titles,
                                      shared_xaxes=False,
                                      shared_yaxes=False)

        for r in range(self.rows):
            specs_r = list()
            for c in range(self.cols):
                for t in self.subplots[r * self.cols + c].traces:
                    self.fig.append_trace(t.trace, r + 1, c + 1)
        self.fig.update(data=[{}, {'yaxis': 'y2'}])
        for target in self.layout:
            if target == 'main':
                self.fig['layout'].update(**self.layout[target])
            else:
                self.fig['layout'][target].update(**self.layout[target])

        self.plot_url = ply.plot(self.fig, filename=self.filename)

    def add_layout(self, target="", layout={}):
        ''' Adds layout information of the plot.

        Parameters
        ==========
        target: object
            the object the layout should be applied on; if empty,
            the whole plot is set as target
        layout: dict
            a dictionary containing the key/value pairs of the new layout
        '''
        if target == '':
            target = 'main'
        if target not in self.layout:
            self.layout[target] = layout
        elif len(layout) == 0:
            del self.layout[target]
        else:
            self.layout[target].update(layout)

    def add_data_source(self, host, port):
        ''' Adds a datasource to the instance'''
        socket = self.add_socket(host, port)
        socket.setsockopt_string(zmq.IDENTITY, str(self.source_id))

        self.sources[self.source_id] = socket
        self.source_id += 1
        self.poller.register(socket, zmq.POLLIN)
        return socket

    def add_trace(self, kind, data_source, name=None, row=1,
                  col=1, parse_data=None, maxpoints=None,
                  mode='lines+markers', xaxis='x', yaxis='y'):
        ''' Adds a new trace object to a subplot.

        Parameters
        ==========
        kind: str
            the kind of graphical object, one of "scatter" or "bars"
        name: str
            the name of the trace, appears for example in the legend
        data_source: object
            a data source object as defined by plotly_stream.add_data_source
        row and col: ints
            the subplot to append the trace object to
        parse_data: object
            an optional callback function to parse the data recieved
            from a server; the function must accept a string
            (the incoming message) and returns the x and y data.
        maxpoints: int
            the number of points the trace contains, default is  maxpoints
            of the plot.
        '''
        if self.token_number >= len(self.api_tokens):
            raise ValueError(NO_TOKENS_LEFT_ERROR)
        if maxpoints is None:
            maxpoints = self.maxpoints
        if name is None:
            name = 'Stream %s' % self.api_tokens[self.token_number]
        if kind == 'scatter':
            trace = stream_trace(self.api_tokens[self.token_number],
                                 data_source, name, maxpoints,
                                 (row - 1) * self.cols + col - 1,
                                 parse_data, mode=mode, xaxis=xaxis, yaxis=yaxis)
        elif kind == 'bars':
            trace = stream_bars(self.api_tokens[self.token_number],
                                data_source, name, maxpoints,
                                (row - 1) * self.cols + col - 1,
                                parse_data, xaxis=xaxis, yaxis=yaxis)
        self.token_number += 1
        self.traces.append(trace)
        self.data.append(trace.trace)
        self.subplots[(row - 1) * self.cols + col - 1].append_trace(trace)

        return trace

    def set_max_points(self, maxpoints):
        ''' Sets the maximum number of points plotted by each trace.
        '''
        if type(maxpoints) != int:
            raise TypeError("maxpoints must be of type int")
        elif maxpoints > 0:
            self.maxpoints = maxpoints

    def get_plot_url(self):
        ''' Returns the plot url, must be called after all other settings.
        '''
        if self.plot_url == "":
            self.init_plot()
        return self.plot_url

    def start_streaming(self, auto_open=True):
        ''' Starts streaming, must be called after all other settings.

        Parameters
        ==========
        auto_open: boolean
            if True (default) the method tries to open a browser
            with the new plot
        '''
        if self.plot_url == "":
            self.init_plot()
            print("Plot url: %s" % self.plot_url)

        for trace in self.traces:
            trace.stream.open()

        while True:
            try:
                socks = dict(self.poller.poll())
            except KeyboardInterrupt:
                break

            for socket in socks:
                socket_id = int(socket.getsockopt_string(zmq.IDENTITY))
                msg = socket.recv_string()

                for trace in self.traces:
                    if trace.data_source == socket_id:
                        x, y = trace.parse_data(msg)
                        trace.write_to_stream({'x': x, 'y': y})
                        trace.old_value = y
                        for t in self.subplots[trace.subplot_id].traces:
                            if t.data_source != socket_id:
                                if t.old_value is not None:
                                    t.write_to_stream(
                                        {'x': x, 'y': t.old_value})

    def add_socket(self, host, port):
        ''' Add a new socket
        '''
        socket = self.context.socket(zmq.SUB)
        socket.connect('tcp://%s:%s' % (host, port))
        socket.setsockopt_string(zmq.SUBSCRIBE, u'')
        return socket

    def set_subplot_title(self, r, c, title):
        '''Sets the title of a subplot'''
        self.subplots[(r - 1) * self.cols + c - 1].title = title

    def set_subplot_specs(self, r, c, spec):
        '''Sets the spec of a subplot'''
        self.subplots[(r - 1) * self.cols + c - 1].spec = spec


class data_source(object):
    ''' Class to generate the data sources used by plotly_stream.
    '''

    def __init__(self, host, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect('tcp://%s:%s' % (host, port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')

    def get_data(self):
        return self.socket.recv_string()


class stream_trace(object):
    ''' Class to instantiate the streamed scatter objects used by plotly_stream.
    '''
    def parse_data(cls, msg):
        ''' Default callback function for streamed scatter objects;
            used if no other callback is given.
        '''
        parts = msg.split()
        t = datetime.datetime.now()
        y = float(parts[1])
        return t, y

    def __init__(self, stream_token, data_source, name,
                 maxpoints, subplot_id, parse_data=None,
                 mode='lines+markers', xaxis='x', yaxis='y'):
        self.old_value = None
        self.data_source = int(data_source.getsockopt_string(zmq.IDENTITY))
        self.name = name
        self.trace = Scatter(x=[], y=[],
                             stream=dict(token=stream_token,
                                         maxpoints=maxpoints),
                             name=name, mode=mode,
                             connectgaps=True, xaxis=xaxis,
                             yaxis=yaxis)
        self.stream = ply.Stream(stream_token)
        self.subplot_id = subplot_id
        if parse_data is not None:
            self.parse_data = parse_data

    def open_stream(self):
        self.stream.open()

    def write_to_stream(self, data):
        self.stream.write(data)

    def close_stream(self):
        self.stream.close()

    def set_parse_data(self, callback):
        self.parse_data = callback


class stream_bars(object):
    ''' Class to generate the streamed bars objects used by plotly_stream.
    '''

    def __init__(self, stream_token, data_source, name,
                 maxpoints, subplot_id, parse_data=None,
                 xaxis='x1', yaxis='y1'):
        self.data_source = int(data_source.getsockopt_string(zmq.IDENTITY))
        self.name = name
        self.bar_labels = list()
        self.trace = Bar(x=[], y=[],
                         stream=dict(token=stream_token, maxpoints=maxpoints),
                         name=name,
                         xaxis=xaxis,
                         yaxis=yaxis)
        self.stream = ply.Stream(stream_token)
        self.subplot_id = subplot_id
        if parse_data is not None:
            self.parse_data = parse_data

    def parse_data(self, msg):
        ''' Default callback function for streamed bars objects;
            used if no other callback is given.
        '''
        parts = msg.split(",")
        y = [float(p) for p in parts]
        if len(self.bar_labels) == len(y):
            x = self.bar_labels
        else:
            x = [str(i + 1) for i in range(len(y))]
        return x, y

    def open_stream(self):
        self.stream.open()

    def write_to_stream(self, data):
        data.update({'type': 'bar'})
        self.stream.write(data)

    def close_stream(self):
        self.stream.close()

    def set_parse_data(self, callback):
        self.parse_data = callback


class subplot(object):
    ''' Class to instantiate subplot object as used by ploty_stream.
    '''

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.spec = dict()
        self.title = ''
        self.traces = list()

    def set_title(self, title):
        self.title = title

    def set_spec(self, spec):
        self.spec = spec

    def append_trace(self, trace):
        self.traces.append(trace)
