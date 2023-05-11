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
##Model
#importing all the datasetsat once
# Categories=pd.read_excel('assets/Northwind.xlsx',sheet_name=0)
# Customers=pd.read_excel('assets/Northwind.xlsx',sheet_name=1)
# Employees=pd.read_excel('assets/Northwind.xlsx',sheet_name=2)
OrderDetails=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=3)
# print(OrderDetails.head())
Orders=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=4)
Products=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=5)
Shippers=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=6)
# Suppliers=pd.read_excel('assets/Northwind.xlsx',sheet_name=7)
SalesAgg=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=8)
OpsAgg=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=9)
Material=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=10)
Freight=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=11)
Freight['Freight']=Freight['Freight'].map('${:,.2f}'.format)
MonthlySalesnTarget=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=12)
EmployeeSalesnTarget=pd.read_excel('dashboard/assets/Northwind.xlsx',sheet_name=13)
# print(EmployeeSalesnTarget.head(10))
POS=Material[['Products_on_Shelf','Discontinued']]
PS=Material[['Stocked','Understocked']]
# MatVal=PS.head(1)
US=Material[['Processed','Pending']]
# print(Frieght)
OST=SalesAgg[SalesAgg['Period']=='Today']
OST1=OST[['Order','Sales']]
OST1['Sales']=OST1['Sales'].map('${:,.2f}'.format)
maskDiscontinued=Products['Discontinued']==1
DiscontinuedProducts=Products.loc[maskDiscontinued].reset_index()
ContinuedProducts=Products.loc[-maskDiscontinued].reset_index()
ContinuedProductsDT=ContinuedProducts[['ProductName','UnitsInStock','UnitsOnOrder','ReorderLevel','Supplier']]
# print(ContinuedProductsDT.head())

OrderDetails['Order_Date']=OrderDetails['Order_Date'].astype('datetime64[ns]')
# print(OrderDetails.head())
Today_Date=max(OrderDetails['Order_Date'])
CurrentMonth=Today_Date.month
CurrentYear=Today_Date.year
TodayshipStatusPie = px.pie(OpsAgg,values='Today', names='range',hole=0.3, title='Shiping Status Today')
MaterialStatusPie=px.pie(PS,values=PS.iloc[0], names=PS.columns, hole=0.3,title='Material status')
UnderstockedStatusPie=px.pie(US,values=US.iloc[0], names=US.columns, hole=0.3,title="Product's under order")

#Sales_tab
SalesSeriesDaily=OrderDetails[['Order_Date','Sales','Discount']]
SalesSeriesDaily['Order_Date']=pd.to_datetime(SalesSeriesDaily['Order_Date'])
startDate20 = np.datetime64(date(2020, 1, 1))
endDate20 = np.datetime64(date(2020, 12, 31))

mask20 = (SalesSeriesDaily['Order_Date'] >= startDate20) & (SalesSeriesDaily['Order_Date'] <= endDate20)
filteredSSD20=SalesSeriesDaily.loc[mask20]

external_stylesheets=[dbc.themes.LITERA]
# app = dash.Dash(external_stylesheets=external_stylesheets)
##View
#Over view tab

Overview_content=html.Div([

                   dbc.Row(
                          [dbc.Col([html.H4('Performance Dashboard',style={'textAlign':'center'})],

                   xs=12,sm=12, md=12,lg=12,xl=12
                           )],justify='center'
                           ),
                  dbc.Row([
                        dbc.Col([
                                 dbc.RadioItems(
                                        options=[
                                                {"label": "Week To Date (WTD)", "value": 'wtd'},
                                                {"label": "Month To Date(MTD)", "value": 'mtd'},
                                                {"label": "Year To Date (YTD)", "value ": 'ytd'}
                                                ],
                                                  value='wtd',
                                                  id="rangeInput",
                                                  inline=True,
                                                  switch=True,
                                                  className='sm',
                                                  style={'textAlign':'center','backgroundColor':'#D3D3D3','border':'double'}

                                             )
                                             ]
                                         )#Col end1
                                         ], justify='center'),

                  dbc.Row([

                           dbc.Col([
                           html.Div([
                                     html.Br(),
                                     html.H6('Today',style={'textAlign':'center'}),
                                     html.Hr(),
                                     dbc.Table.from_dataframe(OST1,striped=True, bordered=True, hover=True, dark=True, size='sm', style={'textAlign':'center','font':'10'}),
                                    ]),
                            # html.Hr(),

                           html.Div([

                                       html.Div([

                                     dcc.Graph(id='TodayshipStatus',
                                                   figure=TodayshipStatusPie,
                                                   config={'displaylogo':False},
                                                   style={'height':'250px'}
                                               ),

                                     html.H4(dbc.Badge('Freight Today   '+ '$'+str(Freight['Freight'][0]),color='dark', style={'textAlign':'center','margin-left':'10%'})),
                                     dcc.Graph(id='MaterialStatus',
                                                   figure=MaterialStatusPie,
                                                   config={'displaylogo':False},
                                                   style={'height':'250px'}
                                                ),
                                     ])
                                     ])
                           ],xs=12,sm=12, md=12,lg=3,xl=3),
                           dbc.Col([
                           html.Br(),
                           html.Div([html.H6(id='rangeTitle1',style={'textAlign':'center'}),
                                     html.Hr(),
                                    html.H4(dbc.Badge(id='OrdersPerPeriod',color='dark'),style={'textAlign':'center','margin-top':'14%'}),
                                    html.Div(
                                     dcc.Graph(id='salesgauge',config={'displaylogo':False}, style={'height':'250px'})
                                              ),
                                     html.Br(),
                                     html.H4(dbc.Badge(id='FreightByRange',color='dark'),style={'textAlign':'center'}),
                                     html.Div([
                                     dcc.Graph(id='RangeShipStatus',
                                     config={'displaylogo':False},
                                     style={'height':'250px'})
                                              ]),
                                              dbc.Modal([
                                              dbc.ModalHeader("Understocked Products"),
                                              dbc.ModalBody(dcc.Graph(
                                                                     figure=UnderstockedStatusPie,
                                                                     config={'displaylogo':False},
                                                                       style={'height':'250px'}
                                              )),
                                              dbc.ModalFooter(
                                                  dbc.Button("Close", id="close", color="dark",className="ml-auto")
                                              ),
                                              ],
                                              id="modal",
                                              ),


                                     ]),

                           ],xs=12,sm=12, md=12,lg=3,xl=3),
                           dbc.Col([
                                   html.Br(),
                                   html.H6('Order Details',style={'textAlign':'center'}),
                                   html.Hr(),

                                   dbc.Row([
                                             dbc.Col([
                                             dcc.Dropdown(
                                                         options=[
                                                                  {'label': 'Sales', 'value': 'Sales'},
                                                                  {'label': 'Quantity', 'value': 'Quantity'},
                                                                  {'label': 'Discount', 'value': 'Discount'}
                                                                  ],
                                                                  value='Sales',
                                                                  id='SeriesValue',
                                                                  style={'backgroundColor':'#D3D3D3'}

                                                          ),
                                                          ],xs=6,sm=6, md=6,lg=6,xl=6),
                                            dbc.Col([
                                             dcc.Dropdown(
                                                         options=[
                                                                  {'label': 'Supplier', 'value': 'Supplier'},
                                                                  {'label': 'Category', 'value': 'Category'},
                                                                  {'label': 'Employee', 'value': 'Employee_name'},
                                                                  {'label': 'Customer Country', 'value': 'C_Country'},
                                                                  {'label': 'Supplier Country', 'value': 'S_Country'}
                                                                  ],
                                                                  value='Category',
                                                                  id='SeriesNames',
                                                                  style={'backgroundColor':'#D3D3D3'}

                                                          )
                                                          ],xs=6,sm=6, md=6,lg=6,xl=6),
                                                          ]),
                                    dbc.Row([
                                    dbc.Col([
                                    html.Div([
                                    dcc.Graph(id="seriesBarDisplay", config={'displaylogo':False},style={'height':'583px'}),
                                    dbc.Modal([
                                    dbc.ModalHeader("Product Details"),
                                    dbc.ModalBody(dcc.Graph(
                                                           id='ProductDetails',
                                                           config={'displaylogo':False},
                                                             style={'height':'400px'}
                                    )
                                    ),
                                    dbc.ModalFooter(
                                        dbc.Button("Close", id="pclose", color="dark",className="ml-auto"),
                                                      )
                                    ],
                                    id="Productmodal",
                                    scrollable=True,

                                    ),
                                              ])
                                            ],xs=12,sm=12, md=12,lg=12,xl=12)
                                            ])

                                   ],
                            xs=12,sm=12, md=12,lg=6,xl=6)

                  ]),

                ],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch ",),

SalesDept_content=html.Div([

dbc.Row(
       [dbc.Col([html.H4('Sales Department',style={'textAlign':'center'})
                ],
xs=12,sm=12, md=12,lg=12,xl=12
             )
       ],justify='center'
       ),

        dbc.Row([dbc.Col([
                           html.Div([
                                    dbc.RadioItems(
                                                 options=[
                                                         {"label": "SALES", "value": 'Sales'},
                                                         {"label": "Discount", "value": 'Discount'},
                                                         ],
                                                           value='Sales',
                                                           id="selectTrend",
                                                           inline=True,
                                                           switch=True,
                                                           className='sm',
                                                  style={'textAlign':'center','backgroundColor':'#D3D3D3','border':'double'}),
                                                  html.Div([
                                                  dcc.Graph(id='annualTrend',
                                                  config={'displaylogo':False},style={'height':'300px'})
                                                            ]),
                                                  html.Div([
                                                  dcc.Graph(id='MonthlyTrends',
                                                  config={'displaylogo':False},style={'height':'300px'})
                                                            ]),
                                                 ])

                                                 ,


                        ])# Col end1

                ]),#row end1
                dbc.Row([
                         dbc.Col([
                                  html.Div([

                                            dcc.Dropdown(
                                                        options=[
                                                                 {'label': 'Department Performance', 'value': 'Department'},
                                                                 {'label': 'Neeta Pillai', 'value': 'Neeta'},
                                                                 {'label': 'Satish Charde', 'value': 'Satish'},
                                                                 {'label': 'Kareena Mishra', 'value': 'Kareena'},
                                                                 {'label': 'Rita Sharma', 'value': 'Rita'},
                                                                 {'label': 'Manish Mittal', 'value': 'Manish'},
                                                                 {'label': 'Shoib Khan', 'value': 'shoib'},
                                                                 {'label': 'Ankita Lokhande', 'value': 'Ankita'},
                                                                 {'label': 'Minal Shah', 'value': 'Minal'}
                                                                 ],
                                                                 value='Department',
                                                                 id='SalesSeriesValue',
                                                                 style={'backgroundColor':'#D3D3D3'},

                                                         )
                                                         ])
                                                         ]),
                                dbc.Col([
                                        html.Div([
                                    dcc.Dropdown(
                                                options=[
                                                        {'label': '2020', 'value': '2020'},
                                                        {'label': '2019', 'value': '2019'},
                                                        {'label': '2018', 'value': '2018'},
                                                                              ],
                                                                              value='2020',
                                                                              id='yearSelectionValue',
                                                                              style={'backgroundColor':'#D3D3D3'},

                                                                      ),
                                           ])


                                 ])#Col end2

                ]),#row end2

                dbc.Row([
                         dbc.Col([
                                  html.Div([
                                            dcc.Graph(id='PerformanceBar',config={'displaylogo':False})

                                          ])

                                 ])

                ])#Row end3

],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch mh-100",)#Container end


OpsDept_content=html.Div([
                                dbc.Row(
                                       [dbc.Col([html.H4('Operations Department',style={'textAlign':'center'})
                                                ],
                                xs=12,sm=12, md=12,lg=12,xl=12
                                             )
                                       ],justify='center'
                                       ),
                                       dbc.Row([
                                                dbc.Col([
                                                html.Div([html.H6('Transport',style={'textAlign':'center'})]),
                                                html.Div([dbc.Table.from_dataframe(Freight[['Period','Freight']],striped=True, bordered=True, hover=True, dark=True, size='sm', style={'textAlign':'center','font':'10'})]),
                                                html.Div([html.H6('Shippers',style={'textAlign':'center'})]),
                                                html.Div([
                                                dcc.Dropdown(
                                                            options=[
                                                                     {'label': '2018', 'value': '2018'},
                                                                     {'label': '2019', 'value': '2019'},
                                                                     {'label': '2020', 'value': '2020'},
                                                                     ],
                                                                     value='2020',
                                                                     id='SelectYear',
                                                                     style={'backgroundColor':'#D3D3D3'},

                                                             ),
                                                          dcc.Graph(id='ShippersPie',
                                                                    config={'displaylogo':False},
                                                                      # style={'height':'400px'}
                                                                    )
                                                ])
                                                ],xs=12,sm=12, md=6,lg=6,xl=6),
                                                dbc.Col([
                                                #Material section
                                                html.Div([html.H6('Material',style={'textAlign':'center'})]),
                                                dbc.Table.from_dataframe(POS,striped=True, bordered=True, hover=True, dark=True, size='sm', style={'textAlign':'center','font':'10'}),
                                                 dbc.Button("Discontinued Products List", id="Dopen", color="dark"),
                                                dbc.Modal([
                                                dbc.ModalHeader("Discontinued Products"),
                                                dbc.ModalBody(html.Div([dbc.Table.from_dataframe(DiscontinuedProducts[['ProductName','Supplier','S_Country']],striped=True, bordered=True, hover=True, dark=True, size='sm', style={'textAlign':'center','font':'10'})])),
                                                dbc.ModalFooter(
                                                    dbc.Button("Close", id="Dclose", color="dark",className="ml-auto")
                                                ),
                                                ],
                                                id="Discontinuedmodal",
                                                ),
                                                html.Hr(),
                                                html.Div([dt.DataTable(
                                                                      id='table',
                                                                      columns=[{"name": i, "id": i} for i in ContinuedProductsDT.columns],
                                                                      data=ContinuedProductsDT.to_dict('records'),
                                                                      page_size=12,
                                                                      style_cell={'textAlign': 'center',
                                                                                  'font_size':'10px',
                                                                                  'color':'black',
                                                                                  'overflow': 'hidden',
                                                                                  'textOverflow': 'ellipsis',
                                                                                  'width':'20px',
                                                                                  'minWidth':'20px',
                                                                                  'maxWidth':'20px',
                                                                                  },
                                                                                  style_as_list_view=True,
                                                                                  tooltip_data=[
                                                                                               {
                                                                                               column: {'value': str(value), 'type': 'markdown'
                                                                                                        }for column, value in row.items()
                                                                                               } for row in ContinuedProductsDT.to_dict('rows')
                                                                                               ],
                                                                                                tooltip_duration=None,
                                                                                                sort_action='native',
                                                                                                sort_mode='multi',
                                                                                                sort_by=[],
                                                                                style_data_conditional=[
                                                                                                       {
                                                                                                       'if': {'row_index': 'odd'},
                                                                                                       'backgroundColor': '#C0C0C0'
                                                                                                        }
                                                                                                        ],
                                                                                style_header={
                                                                                              'backgroundColor': '#C0C0C0',
                                                                                              'fontWeight': 'bold'
                                                                                             }
                                                                         )#DataTable end
                                                                         ])#Div end
                                                ],xs=12,sm=12, md=6,lg=6,xl=6)

                                       ]),#Row end2

                                       dbc.Row([
                                                dbc.Col([
                                                          html.H6('Freight Analysis',style={'textAlign':'center'}),
                                                                      dbc.Row([
                                                                               dbc.Col([
                                                                               dcc.Dropdown(
                                                                                           options=[
                                                                                                    {'label': '2018', 'value': '2018'},
                                                                                                    {'label': '2019', 'value': '2019'},
                                                                                                    {'label': '2020', 'value': '2020'},
                                                                                                    ],
                                                                                                    value='2020',
                                                                                                    id='SelectYear2',
                                                                                                    style={'backgroundColor':'#D3D3D3'},
                                                                                            ),
                                                                                ],xs=6,sm=6, md=3,lg=3,xl=3),
                                                                               dbc.Col([
                                                                                        dcc.Dropdown(
                                                                                                     options=[
                                                                                                             {'label': 'Shipper', 'value': 'Shipper'},
                                                                                                             {'label': 'Employee Name', 'value': 'Employee_Name'},
                                                                                                             {'label': 'Shipment Status', 'value': 'Status'},
                                                                                                             ],
                                                                                                     value='Status',
                                                                                                     id='SelectCriteria',
                                                                                                     style={'backgroundColor':'#D3D3D3'},
                                                                                                      ),

                                                                               ],xs=6,sm=6, md=3,lg=3,xl=3)#Col end3 inner

                                                                      ],justify="center"),#Row End3 inner
            dbc.Row([
                     dbc.Col([
                              dcc.Graph(id='FreightAnalysisGraph',
                              config={'displaylogo':False},
                                        )
                     ])
            ])

                                                ])#Col end3
                                       ])#Row end3
],style={'padding':'1%','backgroundColor':'white','overflow':'hidden'}, className = "align-self-stretch",)

##Controller
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Dashboard', external_stylesheets=external_stylesheets, add_bootstrap_links=True)
app.layout=html.Div(dbc.Tabs(
                    [
                     dbc.Tab(Overview_content,label="Overview",tab_id='Overview_tab'),
                     dbc.Tab(SalesDept_content,label="Sales",tab_id='Sales_tab'),
                     dbc.Tab(OpsDept_content,label="Operations",tab_id='Operations_tab'),

],
style={'backgroundColor':'#BEBEBE','overflow':'hidden'},
id='tabs Container',
active_tab='Overview_tab',
),
)
#Controller Operations_tab******************************************
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("Discontinuedmodal", "is_open"),
    [Input("Dopen", "n_clicks"), Input("Dclose", "n_clicks")],
    [State("Discontinuedmodal", "is_open")],
             )(toggle_modal)


@app.callback(
              Output('ShippersPie','figure'),
              [Input('SelectYear','value')]
)
def CreateShippersPie(year):
    FilteredShippers=Shippers[Shippers['Year']==int(year)].reset_index()
    figPie = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    figPie.add_trace(go.Pie(labels=FilteredShippers['CompanyName'], values=FilteredShippers['Orders'], name="Orders Shipped", title="Orders Shipped"),
              1, 1)
    figPie.add_trace(go.Pie(labels=FilteredShippers['CompanyName'], values=FilteredShippers['Freight'], name="Freight Charged", title="Freight Charged"),
              1, 2)
    figPie.update_layout(title='Orders Vs Freight', showlegend = False)

    return figPie

@app.callback(
            Output('FreightAnalysisGraph','figure'),
           [Input('SelectCriteria','value'),Input('SelectYear2','value')]
    )
def CreateFreightGraph(Criteria,year):
    filteredO=Orders[Orders['Year']==int(year)].reset_index()
        # print(filteredO.head())
    FreightAnalysisGraph1=px.scatter(filteredO,x='C_ShipCountry',y='S_Country',size='Freight',color=Criteria,
                                     labels={'C_ShipCountry':"Customer's Country",
                                              'S_Country':"Supplier's Country"})
    FreightAnalysisGraph1.update_traces(
                                       marker=dict(
                                                  line=dict(width=2,
                                                            # color='DarkSlateGrey'
                                                             color='white'
                                                            )
                                                 )
                                        )


    return FreightAnalysisGraph1

#Controller_Sales_Tab*********************************************
@app.callback(
              Output('PerformanceBar','figure'),
              [Input('SalesSeriesValue','value'),Input('yearSelectionValue','value')]
)
def CreatePerformancebar(SalesSeries,year):
    filteredMonthlySalesnTarget=MonthlySalesnTarget[MonthlySalesnTarget['Year']==int(year)]
    filteredemployeeSalesntarget=EmployeeSalesnTarget[EmployeeSalesnTarget['Year']==int(year)]

    fig=go.Figure()
    if SalesSeries=='Department':
        fig.add_trace(go.Bar(x=filteredMonthlySalesnTarget['Month'],y=filteredMonthlySalesnTarget['Target'],name='Department Sales Target'))
        fig.add_trace(go.Bar(x=filteredMonthlySalesnTarget['Month'],y=filteredMonthlySalesnTarget['Sales'],name='Department Sales Performance',width=0.5,marker_color=filteredMonthlySalesnTarget['Performance'],showlegend=False))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='green', symbol='square'),
                       legendgroup='Target Achieved', showlegend=True, name='Target Acheived'))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='red', symbol='square'),
                       legendgroup='Target Fall Short', showlegend=True, name='Target Fall Short'))
        fig.update_layout(barmode="overlay",hovermode ='closest')
    else:
        filteredemployeeSalesntargetInd=filteredemployeeSalesntarget[filteredemployeeSalesntarget['Employee']==SalesSeries]
        fig.add_trace(go.Bar(x=filteredemployeeSalesntargetInd['Month'],y=filteredemployeeSalesntargetInd['Target'],name='Sales Target'))
        fig.add_trace(go.Bar(x=filteredemployeeSalesntargetInd['Month'],y=filteredemployeeSalesntargetInd['Sales'],name='Total Sales',width=0.5,marker_color=filteredemployeeSalesntargetInd['Performance'],showlegend=False))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='green',symbol='square'),
                       legendgroup='Target Achieved', showlegend=True, name='Target Acheived'))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='red', symbol='square'),
                       legendgroup='Target Fall Short', showlegend=True, name='Target Fall Short'))
        fig.update_layout(barmode="overlay", hovermode ='closest')


    return fig
@app.callback(
              Output('MonthlyTrends','figure'),
              [Input('selectTrend','value')]
              )
def createTrendMonthly(trendInput):
    if trendInput=="Sales":
        MonthlyTrendComparison=px.line(MonthlySalesnTarget,x='Month',y='Sales',color='Year',title='Monthly Sales Trend Comparison')
        MonthlyTrendComparison.update_layout(title_x=0.5)
    else:

        MonthlyTrendComparison=px.line(MonthlySalesnTarget,x='Month',y='Discounts',color='Year',title='Monthly Discount Trend Comparison')
        MonthlyTrendComparison.update_layout(title_x=0.5)
    return MonthlyTrendComparison

@app.callback(
             Output('annualTrend','figure'),
            [Input('selectTrend','value')]
            )
def createTrendAnnual(trendInput):
    if trendInput=="Sales":
        annualsalesTrendLine20=px.line(filteredSSD20,x='Order_Date',y='Sales',title='Daily Sales Trend 2020')
        annualsalesTrendLine20.update_layout(title_x=0.5)
    else:
        annualsalesTrendLine20=px.line(filteredSSD20,x='Order_Date',y='Discount',title='Daily Discount Trend 2020')
        annualsalesTrendLine20.update_layout(title_x=0.5)

    return annualsalesTrendLine20




#Controller-Overview_tab*****************************************
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("modal", "is_open"),
    [Input("MaterialStatus", "clickData"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
             )(toggle_modal)
app.callback(
    Output("Productmodal", "is_open"),
    [Input("seriesBarDisplay", "clickData"), Input("pclose", "n_clicks")],
    [State("Productmodal", "is_open")],
             )(toggle_modal)

@app.callback(Output('rangeTitle1','children'),
                [Input('rangeInput','value')]
                )
def assignTitle(rangeInput):

    if rangeInput=='wtd':
        title='WTD'
    elif rangeInput=='mtd':
        title='MTD'
    else:
        title='YTD'
    return html.H6(title)

@app.callback(Output('OrdersPerPeriod','children'),
                [Input('rangeInput','value')]
                )
def assignOrders(rangeInput):
    orders=0
    order1=0
    title=""
    if rangeInput=='wtd':
        orders=SalesAgg[SalesAgg['Period']=='WTD']
        order1=orders['Order'][1]
        title='WTD '
    elif rangeInput=='mtd':
        orders=SalesAgg[SalesAgg['Period']=='MTD']
        order1=orders['Order'][2]
        title='MTD '
    else:
        orders=SalesAgg[SalesAgg['Period']=='YTD']
        order1=orders['Order'][3]
        title='YTD '


    return title+str(order1)+' Orders'

@app.callback(Output('salesgauge','figure'),
                [Input('rangeInput','value')]
                )
def addSalesfig(rangeInput):
    orders=[]
    salesVal=0
    targetVal=0
    rangeTitle2=''
    if rangeInput=='wtd':
        orders=SalesAgg[SalesAgg['Period']=='WTD']
        salesVal=orders['Sales'][1]
        targetVal=orders['Target'][1]
        rangeTitle2='WTD'
    elif rangeInput=='mtd':
        orders=SalesAgg[SalesAgg['Period']=='MTD']
        salesVal=orders['Sales'][2]
        targetVal=orders['Target'][2]
        rangeTitle2='MTD'
    else:
        orders=SalesAgg[SalesAgg['Period']=='YTD']
        salesVal=orders['Sales'][3]
        targetVal=orders['Target'][3]
        rangeTitle2='YTD'
    axisrange=0
    if salesVal > targetVal:
        axisrange=salesVal+1000
    else:
        axisrange=targetVal+1000

    fig = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = salesVal,
    domain = {'x': [0.1, 1], 'y': [0, 1]},
    name='Sales',
    title = {'text' :"<b>Sales </b>"+rangeTitle2},
    delta = {'reference': targetVal,
              },
    gauge = {
        'axis': {'range': [None,axisrange ]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': targetVal},
        }))
    fig.update_layout(height = 250)
    return fig

@app.callback(Output('RangeShipStatus','figure'),
                    [Input('rangeInput','value')]
                    )
def addRangeShipPie(rangeInput):
        title=""
        range=''
        if rangeInput=='wtd':
            title='WTD Shipping Status'
            range='WTD'
        elif rangeInput=='mtd':
            title='MTD Shipping Status'
            range='MTD'
        else:
            title='YTD Shiping Status'
            range='YTD'

        RangeShipStatusPie=px.pie(OpsAgg,values=range, names='range',hole=0.3, title=title)
        return RangeShipStatusPie

@app.callback(Output('FreightByRange','children'),
                [Input('rangeInput','value')]
                )
def assignFreight(rangeInput):
    FreightDV=0
    title=""
    if rangeInput=='wtd':
        title="WTD"
        FreightDV=Freight.at[1,'Freight']
    elif rangeInput=='mtd':
        title='MTD'
        FreightDV=Freight.at[2,'Freight']
    else:
        title='YTD'
        FreightDV=Freight.at[3,'Freight']
    return title+' Freight '+'$'+str(FreightDV)
@app.callback(Output('seriesBarDisplay','figure'),
                [Input('SeriesValue','value'),Input('SeriesNames','value'),Input('rangeInput','value')]
                )
def assignBarGraph(value1,value2,rangeInput):
    startDate=Today_Date
    endDate=Today_Date
    if rangeInput=='wtd':
        today = Today_Date
        startDate = today - timedelta(days=today.weekday())
        endDate = startDate + timedelta(days=6)
    elif rangeInput=='mtd':
        startDate=Today_Date.replace(day=1)
        endDate=Today_Date.replace(day = calendar.monthrange(Today_Date.year, Today_Date.month)[1])
    else:
        startDate = np.datetime64(date(Today_Date.year, 1, 1))
        endDate = np.datetime64(date(Today_Date.year, 12, 31))

    mask = (OrderDetails['Order_Date'] >= startDate) & (OrderDetails['Order_Date'] <= endDate)
    filteredOD=OrderDetails.loc[mask]
    aggFilterOD=filteredOD.groupby([value2])[[value1]].agg('sum').reset_index()
    aggFilterODSorted=aggFilterOD.sort_values(by=value1, ascending=True)

    series_Bar=px.bar(aggFilterODSorted,x=value1,y=value2,orientation='h')
    if value1=='Sales':
        series_Bar.update_xaxes(tickprefix="$")
    elif value1=='Discount':
        series_Bar.update_xaxes(tickprefix="$")
    else:
        pass
    if value2=='Employee_name':
        value2_N="Employee"
    elif value2=='C_Country':
        value2_N='Customer Country'
    elif value2=='S_Country':
        value2_N="Supplier Country"
    else:
        value2_N=value2


    series_Bar.update_layout(title='{} Vs {}'.format(value2_N,value1),title_x=0.5)

    return series_Bar

@app.callback(
    Output("ProductDetails", "figure"),
    [Input('SeriesValue','value'),Input('SeriesNames','value'),Input('rangeInput','value'),Input("seriesBarDisplay", "clickData")]
             )
def CreateProductBar(value1,value2,rangeInput,clickData):
    startDate=Today_Date
    endDate=Today_Date
    if rangeInput=='wtd':
        today = Today_Date
        startDate = today - timedelta(days=today.weekday())
        endDate = startDate + timedelta(days=6)
    elif rangeInput=='mtd':
        startDate=Today_Date.replace(day=1)
        endDate=Today_Date.replace(day = calendar.monthrange(Today_Date.year, Today_Date.month)[1])
    else:
        startDate = np.datetime64(date(Today_Date.year, 1, 1))
        endDate = np.datetime64(date(Today_Date.year, 12, 31))

    mask = (OrderDetails['Order_Date'] >= startDate) & (OrderDetails['Order_Date'] <= endDate)
    filteredOD=OrderDetails.loc[mask]
    aggFilterOD=filteredOD.groupby([value2,'ProductName'])[[value1]].agg('sum').reset_index()
    # print(aggFilterOD.head())
    if clickData is None:
        clickedBar=aggFilterOD[value2][0]
    else:
        clickedBar=clickData['points'][0]['y']


    aggFilterODbyPN=aggFilterOD.loc[aggFilterOD[value2]==clickedBar]
    aggFilterODSortedbyPN=aggFilterODbyPN.sort_values(by=value1, ascending=True)

    # print(aggFilterODSortedbyPN.head())

    Product_Bar=px.bar(aggFilterODSortedbyPN,x=value1,y='ProductName',orientation='h')
    if value1=='Sales':
        Product_Bar.update_xaxes(tickprefix="$")
    elif value1=='Discount':
        Product_Bar.update_xaxes(tickprefix="$")
    else:
        pass

    if value2=='Employee_name':
        value2_N="Employee"
    elif value2=='C_Country':
        value2_N='Customer Country'
    elif value2=='S_Country':
        value2_N="Supplier Country"
    else:
        value2_N=value2


    Product_Bar.update_layout(title='{} Vs {}'.format(value2_N,value1),title_x=0.5)

    return Product_Bar

# if __name__=='__main__':
#     app.run_server(debug=True)
