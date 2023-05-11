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
df2['Sales_Gap'] = df.apply(lambda row: row.Target - row.Sales, axis=1)
df2['Sales Gap'] = df2.apply(lambda row: abs(row.Sales_Gap), axis=1)
df2['Colour'] = np.where(df2['Sales']>df2['Target'], "Green", "Red")
df2['Label'] = np.where(df2['Sales']>df2['Target'], "Achieved", "Gap")
df2['Total Sales']=np.where(df2['Sales']>df2['Target'], df2["Target"], df2['Sales'])
df2_Lead=df2[df2["Label"]=="Achieved"]
df2_Lag=df2[df2["Label"]=="Gap"]



app = DjangoDash('StackedBarChart', external_stylesheets=external_stylesheets, add_bootstrap_links=True)
data=[
go.Bar(name='Sales', x=df2['Month'], y=df2['Total Sales'], marker_color='indianred'),
go.Bar(name='Sales Lead', x=df2_Lead['Month'], y=df2_Lead['Sales Gap'],  marker_color=df2_Lead['Colour']),
go.Bar(name='Sales Lag', x=df2_Lag['Month'], y=df2_Lag['Sales Gap'],  marker_color=df2_Lag['Colour']),


]
layout=go.Layout(barmode='stack', hovermode="closest",
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
                             )
                            ])
                             ])
                    ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ",)
