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

df=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=15)
Total=df['Feb'].sum()
FTotal='{:,.2f}'.format(Total)


app = DjangoDash('SimplePieChart', external_stylesheets=external_stylesheets, add_bootstrap_links=True)
data=[go.Pie(labels=df['Category'], values=df['Feb'])]
layout=go.Layout(title={
       'text': 'Target Vs Sales',
        'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'} )
app.layout =html.Div([dbc.Row([
                    dbc.Col([
                            html.H6(dbc.Badge("Feb Target= ₹"+str(FTotal),color='dark'),style={'textAlign':'center','margin-top':'14%'}),
                            dcc.Graph(id='PieChart',
                                    figure=go.Figure(data=data,layout=layout), config={'displaylogo':False}, style={'height':'400px'}
                                      )
                            ], style={'padding':'1%','height':'500px'})

                              ])
                    ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ",)
