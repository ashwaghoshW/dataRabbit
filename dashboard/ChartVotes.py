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
import sqlite3
from django.conf import settings
external_stylesheets=[dbc.themes.LITERA]

app = DjangoDash('ChartVotes', external_stylesheets=external_stylesheets, add_bootstrap_links=True)

def GetNames():
    conn = sqlite3.connect(settings.BASE_DIR/'db.datarabbit')
    df = pd.read_sql_query("SELECT name FROM Votes", conn)
    conn.close()
    return df

def GetVoteCount():
    conn = sqlite3.connect(settings.BASE_DIR/'db.datarabbit')
    df = pd.read_sql_query("SELECT * FROM VoteCount", conn)
    conn.close()
    return df

def GetTotalVote():
    conn = sqlite3.connect(settings.BASE_DIR/'db.datarabbit')
    CountDF = pd.read_sql_query("SELECT COUNT(*) FROM Votes", conn)
    conn.close()
    Cn=CountDF.values[0][0]
    return Cn

def GenerateGraph():
    TotalVotes=GetTotalVote()
    Votes=GetVoteCount()
    # TV=TotalVotes.values[0][0]
    FPVotes=Votes[Votes["FirstPreference"]>0]
    SPVotes=Votes[Votes["SecondPreference"]>0]
    TPVotes=Votes[Votes["ThirdPreference"]>0]
    figPie = make_subplots(rows=3, cols=1, specs=[[{'type':'domain'}], [{'type':'domain'}], [{'type':'domain'}]])
    figPie.add_trace(go.Pie(labels=FPVotes['GraphName'], values=FPVotes['FirstPreference'], name="First Preference", title="First Preference"),
              row=1, col=1)
    figPie.add_trace(go.Pie(labels=SPVotes['GraphName'], values=SPVotes['SecondPreference'], name="Second Preference", title="Second Preference"),
              row=2, col=1)
    figPie.add_trace(go.Pie(labels=TPVotes['GraphName'], values=TPVotes['ThirdPreference'], name="Third Preference", title="Third Preference"),
              row=3, col=1)
    figPie.update_layout(height=800, title='Vote distribution-chart preference', showlegend = True)
    figPie.update_layout(title_x=0.5)
    return figPie

Votes=GetVoteCount()
TotalVotes=GetTotalVote()
# print(TotalVotes)

def InsertVote(name,FP,SP,TP):

    try:
        conn = sqlite3.connect(settings.BASE_DIR/'db.datarabbit')
        # print("before cursor")
        cursor = conn.cursor()

        sqlite_insert_query = """INSERT INTO Votes(name,'First Preference', 'Second Preference', 'Third Preference') VALUES(?, ?, ?, ?);"""
        data_tuple = (name, FP, SP, TP)

        count = cursor.execute(sqlite_insert_query,data_tuple)
        conn.commit()
        result="Thank you for Vote!"

        # print("Record inserted successfully into SqliteDb_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        result="Sorry!, Voting failed, Please try again."
    finally:
        if (conn):
            conn.close()

    return result

Names=GetNames()
Votes=GetVoteCount()
# print(Votes.head())
h=40
# VotingOptions = pd.DataFrame({'Graph':['Tabular representation', 'Pie chart', 'Donut chart', 'Speedometer', 'Bar/Column chart', 'Stacked bar/column chart', 'Bar inside bar chart', 'Bullet chart', 'Scatter plot', 'Line chart', 'Area chart', 'Butterfly chart', 'Bar chart with line chart', 'Bar chart with scatter plot', 'Other, Read my comment'],
# 'Code':['TR','PC','DC','SM','BCC','SBC','BIB','BULC','SC','LC','AC','BUTC','BCLC','BCSC','OC']})

# print(VotingOptions)




app.layout =html.Div([dbc.Row([
                    dbc.Col([
                    dbc.Alert("What is your preference for representing Target Vs Achievements?", color="info"),
                    dbc.Alert("Vote For Your favourite chart", color="primary"),

                    html.P("Your First Name and Last name is used for unique identification of your vote, to store only authentic vote in the system. Your name will not be displayed anywhere on site. To remain anonymous while voting, You can choose any name of your choice; though not recommended because it leads to faulty output."),
                    html.Hr(),
                            # row for input names
                            dbc.Row([
                                     dbc.Col([
                                                dbc.Label("First Name"),
                                                dbc.Input(id="fname", placeholder="Your first name...", type="text",value=""),

                                             ],xs=12,sm=12, md=6,lg=6,xl=6),
                                     dbc.Col([
                                                dbc.Label("Last Name"),
                                                dbc.Input(id="lname", placeholder="Your last name.....", type="text",value=""),
                                             ],xs=12,sm=12, md=6,lg=6,xl=6),
                                   ]),
                        html.Hr(),
                            dbc.Row([
                                                  dbc.Col([

                                                  html.Label("First Preference"),
                                                  dcc.Dropdown(
                                                  id='FirstPreference',
                                                  options=[
                                                        {'label': 'Tabular representation', 'value': 'TR'},
                                                        {'label': 'Pie chart', 'value': 'PC'},
                                                        {'label': 'Donut chart', 'value': 'DC'},
                                                        {'label': 'Speedometer', 'value': 'SM'},
                                                        {'label': 'Bar/Column chart', 'value': 'BCC'},
                                                        {'label': 'Stacked bar/column chart', 'value': 'SBC'},
                                                        {'label': 'Bar inside bar chart', 'value': 'BIB'},
                                                        {'label': 'Bullet chart', 'value': 'BULC'},
                                                        {'label': 'Scatter plot', 'value': 'SC'},
                                                        {'label': 'Line chart', 'value': 'LC'},
                                                        {'label': 'Area chart', 'value': 'AC'},
                                                        {'label': 'Butterfly chart', 'value': 'BUTC'},
                                                        {'label': 'Bar chart with line chart', 'value': 'BCLC'},
                                                        {'label': 'Bar chart with scatter plot', 'value': 'BCSC'},
                                                        {'label': 'Other, Read my comment', 'value': 'OC'},


                                                          ],
                                                   value='TR',
                                                   style={'backgroundColor':'#D3D3D3', 'text-overflow': 'ellipsis' },

                                                              ),
                                                            ]),
                                    ]),
                                     dbc.Row([
                                                      dbc.Col([
                                                      html.Label("Second Preference"),
                                                      dcc.Dropdown(
                                                      id='SecondPreference',
                                                      options=[
                                                            {'label': 'Tabular representation', 'value': 'TR'},
                                                            {'label': 'Pie chart', 'value': 'PC'},
                                                            {'label': 'Donut chart', 'value': 'DC'},
                                                            {'label': 'Speedometer', 'value': 'SM'},
                                                            {'label': 'Bar/Column chart', 'value': 'BCC'},
                                                            {'label': 'Stacked bar/column chart', 'value': 'SBC'},
                                                            {'label': 'Bar inside bar chart', 'value': 'BIB'},
                                                            {'label': 'Bullet chart', 'value': 'BULC'},
                                                            {'label': 'Scatter plot', 'value': 'SC'},
                                                            {'label': 'Line chart', 'value': 'LC'},
                                                            {'label': 'Area chart', 'value': 'AC'},
                                                            {'label': 'Butterfly chart', 'value': 'BUTC'},
                                                            {'label': 'Bar chart with line chart', 'value': 'BCLC'},
                                                            {'label': 'Bar chart with scatter plot', 'value': 'BCSC'},
                                                            {'label': 'Other, Read my comment', 'value': 'OC'},
                                                              ],
                                                       value='TR',
                                                       style={'backgroundColor':'#D3D3D3', 'text-overflow': 'ellipsis'},

                                                                  ),

                                                              ]),
                                              ]),
                                    dbc.Row([
                                                      dbc.Col([
                                                      html.Label("Third Preference"),
                                                      dcc.Dropdown(
                                                      id='ThirdPreference',
                                                      options=[
                                                            {'label': 'Tabular representation', 'value': 'TR'},
                                                            {'label': 'Pie chart', 'value': 'PC'},
                                                            {'label': 'Donut chart', 'value': 'DC'},
                                                            {'label': 'Speedometer', 'value': 'SM'},
                                                            {'label': 'Bar/Column chart', 'value': 'BCC'},
                                                            {'label': 'Stacked bar/column chart', 'value': 'SBC'},
                                                            {'label': 'Bar inside bar chart', 'value': 'BIB'},
                                                            {'label': 'Bullet chart', 'value': 'BULC'},
                                                            {'label': 'Scatter plot', 'value': 'SC'},
                                                            {'label': 'Line chart', 'value': 'LC'},
                                                            {'label': 'Area chart', 'value': 'AC'},
                                                            {'label': 'Butterfly chart', 'value': 'BUTC'},
                                                            {'label': 'Bar chart with line chart', 'value': 'BCLC'},
                                                            {'label': 'Bar chart with scatter plot', 'value': 'BCSC'},
                                                            {'label': 'Other, Read my comment', 'value': 'OC'},


                                                              ],
                                                       value='TR',
                                                       style={'backgroundColor':'#D3D3D3', 'text-overflow': 'ellipsis'},

                                                                  ),
                                                                ]),


                                    ]),
                                    html.Br(),
                                    html.Hr(),
                                    html.Br(),
                                    html.Div(

                                             dbc.Button("Vote", id="VoteButton",color="secondary", className="mr-2"),
                                             style={'textAlign':'center'}),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(id="VoteOutput"),



                            ],xs=12,sm=12, md=6,lg=6,xl=6),#FIRST CLUMN END

                    dbc.Col([
                                html.Div( html.H4(dbc.Badge(id="VoteBadge",color='dark', style={'textAlign':'center','margin-left':'20%'})),),
                                dcc.Graph(
                                         id='VoteResult',config={'displaylogo':False},style={'width':"100%"},
                                         ),
                                 # dcc.Interval(
                                 #                id='interval-component',
                                 #                interval=300000, # 5 min
                                 #                n_intervals=0
                                 #             )

                            ],xs=12,sm=12, md=6,lg=6,xl=6)#second col
                            ]),
                              ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ")




@app.callback(
            Output('VoteOutput','children'),
           [Input('VoteButton','n_clicks')],
           [State('fname','value'),State('lname','value'),State('FirstPreference','value'),State('SecondPreference','value'),State('ThirdPreference','value')]
    )
def update_output(n_clicks,fname,lname,firstPreference, secondPreference, thirdPreference):
    Names=GetNames()
    if n_clicks:
        if fname=="" or lname=="":
            return "Please enter your name"
        else:
            name=str(fname.lower())+str(lname.lower())
            # print(name)
            if name in Names['name'].values:
                return "{} {}, you have already voted with same name".format(fname,lname)
            else:
                if firstPreference==secondPreference or firstPreference==thirdPreference or secondPreference==thirdPreference:
                    return "Please choose different preferences"
                else:
                    Res=InsertVote(name, firstPreference, secondPreference, thirdPreference)

                    TotalVotes=GetTotalVote()
                    return "{} {}, ".format(fname,lname)+Res


@app.callback(
            Output('VoteResult','figure'),
           [Input('VoteButton','n_clicks')])
def updateGraph(n_clicks):
    figPie=GenerateGraph()
    if n_clicks:
        figPie=GenerateGraph()
    return figPie



@app.callback(
            Output('VoteBadge','children'),
           [Input('VoteButton','n_clicks')])
def updateBadge(n_clicks):
    TotalVotes=GetTotalVote()
    if n_clicks:
        TotalVotes=GetTotalVote()
    VoteBadgestr=str(TotalVotes)+" people voted here! "
    return VoteBadgestr
