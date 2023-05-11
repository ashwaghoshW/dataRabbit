import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
#from server import app
import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta, date
import calendar
from django_plotly_dash import DjangoDash
external_stylesheets=[dbc.themes.LITERA]


df=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=14)
df2=df[0:12].copy()


app = DjangoDash('SimpleBarChart', external_stylesheets=external_stylesheets, add_bootstrap_links=True)
data=[
go.Bar(name='Sales', x=df2['Month'], y=df2['Sales'], marker_color='indianred'),
go.Bar(name='Target', x=df2['Month'], y=df2['Target'],  marker_color='lightsalmon')]
layout=go.Layout( barmode='group',
                  yaxis=dict(title='Sales',titlefont_size=14,tickprefix="₹"),
                  xaxis=dict(title='Month',titlefont_size=14),
                  title={
                          'text': 'Target Vs Sales',
                           'y':0.9,
                           'x':0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                )
app.layout =html.Div([dbc.Row([
                    dbc.Col([
                    dcc.Graph(id='BarChart',config={'displaylogo':False},
                    figure=go.Figure(data=data,layout=layout)
    # figure.update_layout(barmode='stack')
                             )
                            ])
                    ])
                    ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ",)
