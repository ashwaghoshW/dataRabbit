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
df2['Base'] = df.apply(lambda row: row.Target*-1, axis=1)
df2["Empty"]= df.apply(lambda row: row.Target*0, axis=1)

app = DjangoDash('Butterfly', external_stylesheets=external_stylesheets, add_bootstrap_links=True)
fig2_data= go.Bar(name='Sales', x=df2['Sales'], y=df2['Month'],   xaxis="x2", yaxis= "y2", marker_color='#138808', orientation='h')
fig1_data= go.Bar(name='Target', x=df2['Target'], y=df2['Month'],   marker_color='#FF9933',orientation='h')

data=[fig1_data,fig2_data]
layout=go.Layout(hovermode="closest",

                 title={
                        'text': 'Target Vs Sales',
                         'y':0.9,
                         'x':0.5,
                         'xanchor': 'center',
                         'yanchor': 'top'},

                 xaxis= dict(

                                range=[2000000, 0],
                                domain= [0, 0.5],
                                autorange= True,
                                title='Target',
                                titlefont_size=14,
                                tickprefix="₹"
                            ),
                 yaxis= dict(
                                autorange=True,
                                title='Month',
                                titlefont_size=14,
                                showticklabels=True,

                              ),

                 xaxis2= dict(

                                range = [0, 2000000],
                                anchor= "y2",
                                domain=[0.5, 1],
                                autorange= True,
                                showticklabels=True,
                                title='Sales',
                                tickprefix="₹"
                          ),
                 yaxis2= dict(
                                anchor="x2",
                                domain = [0, 1],
                                autorange= True,
                                showticklabels=False,
                                tickfont=dict(family='Rockwell', color='#000080', size=16)
                      ),
                    )
app.layout =html.Div([dbc.Row([
                    dbc.Col([
                    dcc.Graph(id='BarChart',config={'displaylogo':False},
                        figure=go.Figure(data=data,layout=layout)
                             )
                            ],xs=12,sm=12, md=12,lg=12,xl=12, style={'padding':'2%'})
                    ])
                    ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ")
