# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app import app
from .read_data import df, column_names
from .tools import get_feature_type

#df = read_data.df
#column_names = read_data.column_names


'''
    Layout for one variable analysis. It includes variable selection
    and the graph
'''

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column-one',
                options=[{'label': i, 'value': i} for i in column_names],
                value='state'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='main-graph-one')
])


@app.callback(
    dash.dependencies.Output('main-graph-one', 'figure'),
    [dash.dependencies.Input('xaxis-column-one', 'value')])
def update_graph(xaxis_column_name):
    '''
        Callback to update the graph as a function of the selected feature
    '''
    type_ = get_feature_type(df, xaxis_column_name)
    x = df[xaxis_column_name]
    if type_ == 'quantitative':
        return {
            'data': [
                go.Histogram(x=x)
            ],
            'layout': {
                'xaxis': {'title': xaxis_column_name}
            }
        }
    else:
        counts = x.value_counts()
        keys = counts.keys()
        if keys.dtype is not object:
            keys = ['c' + str(k) for k in keys]
        return {
            'data': [
                {'x': keys, 'y': counts, 'type': 'bar'}
            ],
            'layout': {
                'xaxis': {'title': xaxis_column_name}
            }
        }
