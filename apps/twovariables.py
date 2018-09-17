# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app import app
from .read_data import df, column_names
from .tools import get_feature_type, get_feature_and_axis

#df = read_data.df
#column_names = read_data.column_names

'''
    Layout for two variable analysis. It includes variables selection,
    mode (linear, log in case of quantitative variables) and the graph
'''

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in column_names],
                value='state'
            ),
            dcc.RadioItems(
                id='xaxis-mode',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in column_names],
                value='annual_revenue'
            ),
            dcc.RadioItems(
                id='yaxis-mode',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='main-graph')
])


@app.callback(
    dash.dependencies.Output('main-graph', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-mode', 'value'),
     dash.dependencies.Input('yaxis-mode', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_mode, yaxis_mode):
    '''
        Callback to update the graph as a function of the selected
        features and their mode (linear or log)
    '''
    x, xaxis = get_feature_and_axis(df, xaxis_column_name, xaxis_mode)
    y, yaxis = get_feature_and_axis(df, yaxis_column_name, yaxis_mode)

    return {
        'data': [go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis=xaxis,
            yaxis=yaxis,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
        )
    }


'''
    Callbacks to hide the radio buttons which allows to choose
    between linear and log modes for quantitative variables
'''


@app.callback(
    dash.dependencies.Output('xaxis-mode', 'className'),
    [dash.dependencies.Input('xaxis-column', 'value')])
def hide_xmode_on_categorical(xaxis_column):
    '''
        Callback to hide the Linear/Log radio buttons when
        is selected a categorical variable for the x axis
    '''
    type_ = get_feature_type(df, xaxis_column)
    if type_ is not 'quantitative':
        return 'hidden'
    else:
        return ''


@app.callback(
    dash.dependencies.Output('yaxis-mode', 'className'),
    [dash.dependencies.Input('yaxis-column', 'value')])
def hide_ymode_on_categorical(yaxis_column):
    '''
        Callback to hide the Linear/Log radio buttons when
        is selected a categorical variable for the y axis
    '''
    type_ = get_feature_type(df, yaxis_column)
    if type_ is not 'quantitative':
        return 'hidden'
    else:
        return ''
