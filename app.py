# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from monzoviz.source import MonzoData
data = MonzoData('data/monzo.csv')
df = data.get_outgoings()
categories = data.get_categories()
from monzoviz import plot

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output# Load Data
app = JupyterDash(external_stylesheets=[dbc.themes.BOOTSTRAP])

categories = data.get_categories()
categories = categories[1:]


controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Category"),
                dcc.Dropdown(
                    id="category-variable",
                    options=[
                        {"label": col, "value": col} for col in categories
                    ],
                    value="Bills",
                ),
            ]
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Monzo Plot"),
        html.Hr(),
        html.H3("Grouped Outgoings Per Month"),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="outgoings-graph"), md=8),
            ],
            align="center",
        ),
        html.H3("Outgoings Over Time"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=plot.plotly_ongoing_balance(df)), md=12),
            ],
            align="center",
        ),
    ],
    fluid=True,
)



@app.callback(
    Output("outgoings-graph", "figure"),
    [
        Input("category-variable", "value"),
    ],
)
def make_graph(category):
    # minimal input validation, make sure there's at least one cluster
    df_category = df[df['category'] == category]
    return plot.plotly_stacked_bar(df_category, 'entity')


if __name__ == '__main__':
    app.run_server(debug=True, port=12000)
