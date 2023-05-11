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
df2.rename(columns={'Target': 'Target in lacs ₹', 'Sales': 'Sales in lacs ₹'}, inplace=True)
app = DjangoDash('TabularRepresentation', external_stylesheets=external_stylesheets, add_bootstrap_links=True)

app.layout =html.Div([dbc.Row([
                                dbc.Col([
                                        dt.DataTable(
                                                        id='table1',
                                                        columns=[{"name": i, "id": i} for i in df.columns],
                                                        data=df.to_dict('records'),
                                                         style_data_conditional=[
                                                            {
                                                                'if': {'row_index': 'odd'},
                                                                'backgroundColor': 'rgb(248, 248, 248)'
                                                            },
                                                              {'if': {
                                                                    'column_type': 'any'  # 'text' | 'any' | 'datetime' | 'numeric'
                                                                },
                                                                'textAlign': 'center'
                                                            },
                                                        ],
                                                        style_header={
                                                            'backgroundColor': 'rgb(230, 230, 230)',
                                                            'fontWeight': 'bold',
                                                            'border': '1px solid black',
                                                            'textAlign': 'center',
                                                        },
                                                        style_cell={

                                                                       'border': '1px solid black' ,
                                                                    },

                                                        )
                                            ],xs=12,sm=12, md=12,lg=5,xl=5, style={'padding':'2%'}),
                                dbc.Col([
                                        dt.DataTable(
                                                    id='table2',
                                                    columns=[{"name": i, "id": i} for i in df2.columns],


                                                    data=df2.to_dict('records'),
                                                     style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            'backgroundColor': 'rgb(248, 248, 248)'
                                                        },
                                                        {
                                                            'if': {
                                                                    'filter_query': '{Target in lacs ₹} < {Sales in lacs ₹}',
                                                            },
                                                            'backgroundColor': '#3D9970'
                                                        },
                                                          {'if': {
                                                                'column_type': 'any'  # 'text' | 'any' | 'datetime' | 'numeric'
                                                            },
                                                            'textAlign': 'center'
                                                        },
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(230, 230, 230)',
                                                        'fontWeight': 'bold',
                                                        'border': '1px solid black',
                                                        'textAlign': 'center',
                                                    },
                                                    style_cell={

                                                                   'border': '1px solid black' ,
                                                                },

                                                )],xs=12,sm=12, md=12,lg=5,xl=5,style={'padding':'2%'})
                                ],justify='center')
                                ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ",)
