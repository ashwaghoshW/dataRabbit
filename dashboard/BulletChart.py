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
df2=df.copy()
df2['Target'] = df2['Target'].div(100000).round(2)
df2['Sales'] = df2['Sales'].div(100000).round(2)
Target=(df2.iat[1,1])
Sales=(df2.iat[1,2])



app = DjangoDash('BulletChart', external_stylesheets=external_stylesheets, add_bootstrap_links=True)


app.layout =html.Div([dbc.Row([
                    dbc.Col([
                            html.Div([html.H4("Feb Sales"),],style={'textAlign':'center'}),
                            html.Div([html.H6("All values in ₹ lacs"),],style={'textAlign':'center'}),
                            dcc.Graph(id='pie',config={'displaylogo':False},style={'height':250},
                            figure=go.Figure(go.Indicator(

                                                           mode = "number+gauge+delta", value = Sales,
                                                            domain = {'x': [0.1, 1], 'y': [0, 1]},
                                                            title = {'text':"<b>Sales</b><br><span style='color: gray; font-size:0.8em'>₹ lacs</span>", 'font': {"size": 14}},
                                                            delta = {'reference': Target},
                                                            number = {'prefix': "₹"},
                                                            gauge = {
                                                                'shape': "bullet",
                                                                'axis': {'range': [None, 2],
                                                                'tickprefix':'₹'},
                                                                'threshold': {
                                                                    'line': {'color': "red", 'width': 2},
                                                                    'thickness': 0.75,
                                                                    'value': Target},
                                                                'steps': [
                                                                    {'range': [0, 1], 'color': "lightgray"},
                                                                    {'range': [1, 1.5], 'color': "gray"}]}

                                                          )
                                             )



                                    )

                            ],style={'padding':'2%'})
                        ])

                    ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ",)
