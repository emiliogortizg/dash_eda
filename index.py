# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import flask
from app import app
from apps import onevariable, twovariables, wrtoutput


'''
    Main layout to show a menu with links to the different views
        - One variable analysis
        - Two variable analysis
        - W.r.t output analysis
'''
app.layout = html.Div([
    html.Div(id='links', children=[
        html.Div(id='onevariable', children=[
            dcc.Link('One variable', href='/onevariable'),
        ], className='link'),

        html.Div(id='twovariables', children=[
            dcc.Link('Two variables', href='/twovariables'),
        ], className='link'),

        html.Div(id='wrtoutput', children=[
            dcc.Link('W.r.t. output', href='/wrtoutput'),
        ], className='link')
    ], className='buttons'),
    html.Hr(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    '''
        Callback to change the view
    '''
    if pathname == '/onevariable':
        return onevariable.layout
    elif pathname == '/twovariables':
        return twovariables.layout
    elif pathname == '/wrtoutput':
        return wrtoutput.layout
    else:
        return onevariable.layout


'''
    Callbacks to change which button is active in the menu
'''


def toggle_path_button(check_path):
    def toggle_button(pathname):
        if check_path == pathname:
            return 'link active'
        else:
            return 'link'
    return toggle_button


for check_path in ['onevariable', 'twovariables', 'wrtoutput']:
    app.callback(
        Output(check_path, 'className'),
        [Input('url', 'pathname')])(toggle_path_button('/'+check_path))


'''
    Serving css stylesheets
'''

css_directory = 'css'
stylesheets = ['main.css']
static_css_route = '/static/'


@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                stylesheet
            )
        )
    return flask.send_from_directory(css_directory, stylesheet)


for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/static/{}".format(stylesheet)})


if __name__ == '__main__':
    app.run_server(debug=True)
