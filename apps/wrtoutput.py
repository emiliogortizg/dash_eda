# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from app import app
from .read_data import df, column_names, output_name
from .tools import get_feature_type

#df = read_data.df
#column_names = read_data.column_names
#output_name = read_data.output_name

'''
    Layout to compare each feature with the output. It includes variable
    selection and the graph
'''

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column-out',
                options=[{'label': i, 'value': i} for i in column_names],
                value='state'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='main-graph-out')
])


@app.callback(
    dash.dependencies.Output('main-graph-out', 'figure'),
    [dash.dependencies.Input('xaxis-column-out', 'value')])
def update_graph(column_name):
    '''
        Callback to update the graph as a function of the selected feature
    '''
    type_ = get_feature_type(df, column_name)

    if type_ == 'categorical':
        partial_df = df[[column_name, output_name]]
    elif type_ == 'quantitative':
        # Discretize the quantitative variable
        discrete = pd.qcut(
            df[column_name],
            100,
            duplicates='drop')
        discrete_df = pd.concat(
            [discrete, df[output_name]],
            axis=1,
            sort=False)
        discrete_df = discrete_df.sort_values(by=column_name)
        partial_df = discrete_df

    # Calculating the probability of output = 1 conditionated
    # to each value in the variable (categorical or discretized)
    # Also a regularized probability with a 0.5 prior to remove
    # the effect of low count values with high probability
    common = partial_df.groupby([column_name])[output_name].sum()
    total = partial_df.groupby([column_name])[output_name].count()
    value2p = common * 1.0 / total
    value2pn = (common + 5.0) / (total + 10.0)

    # Sort by probability for categorical variables
    if type_ == 'categorical':
        value2pn = value2pn.sort_values(ascending=False)

    # Preparing visualization inputs
    keys = ['c'+str(key) for key in value2pn.keys()]
    values = [value2p[key] for key in value2pn.keys()]
    valuesn = [value2pn[key] for key in value2pn.keys()]

    # Two bar graphs for both probabilities
    trace1 = go.Bar(
        x=keys,
        y=values,
        name='P(y=1|'+column_name+')'
    )
    trace2 = go.Bar(
        x=keys,
        y=valuesn,
        name='Regularized P'
    )

    return {
        'data': [
            trace1,
            trace2
        ],
        'layout': {
            'xaxis': {'title': column_name}
        }
    }
