import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import random
import re
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input

#from plotly.subplots import make_subplots
import datetime
import math



######################################################################################################################
######################################################################################################################
#######################################         1.  Data              ################################################
######################################################################################################################
######################################################################################################################

####################################################################################
#######################   Page 1 - Plot1.   Flatten the Curve      ################
####################################################################################
# def calculate_growth_rate_WORLD(df):
    
#     df = df.drop(['Province/State', 'Lat', 'Long'], axis = 1)

#     df =  df.groupby(['Country/Region']).sum().reset_index()

#     df = df.transpose().reset_index()
#     df.columns = df.iloc[0,:]
#     df.drop([0], axis = 0, inplace = True)
#     df.reset_index(drop = True, inplace = True)
#     df.rename(columns = {'Country/Region' : 'Date'}, inplace = True)
#     df.Date = pd.to_datetime(df.Date)

#     df.drop(list(df.columns[1:][df.iloc[:,1:].sum(axis = 0) == 0]), axis = 1, inplace=True) 
#     df.drop(['Iceland', 'Kazakhstan', 'Slovakia'], axis = 1, inplace = True)
#     df.columns = ["South Korea" if x == "Korea, South" else x for x in list(df.columns)]

#     dfR = pd.DataFrame(np.empty_like(df))
#     dfR.columns = df.columns
#     dfR['Date'] = df['Date']


#     for i in range(1, df.shape[1]):
#         country = df.columns[i]
#         j = np.where(df[country] > 0)[0][0]
#         dfR[country] = np.concatenate((np.full(j+5,np.nan), 
#                                                 pow(np.array(df[country][j+5:]) / np.array(df[country][j:df.shape[0]-5]), 1/5) - 1),
#                                                 axis = 0)  
#     for i in range(1, dfR.shape[1]):
#         s = [j for j in range(dfR.shape[0]) if not math.isnan(dfR.iloc[j,i])][0]
        
#         for j in range(s+1, dfR.shape[0]-1):
#             dfR.iloc[j, i] = np.mean([dfR.iloc[j-1, i],
#                                                   dfR.iloc[j, i],
#                                                   dfR.iloc[j+1, i]])
#     return(dfR)

def calculate_growth_rate_US(df):
    
    df = df.drop(['UID','iso2','iso3','code3','FIPS','Admin2','Country_Region', 'Lat', 'Long_','Combined_Key'], axis = 1)


    df =  df.groupby(['Province_State']).sum().reset_index()

    df = df.transpose().reset_index()
    df.columns = df.iloc[0,:]
    df.drop([0], axis = 0, inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.rename(columns = {'Province_State' : 'Date'}, inplace = True)
    df.Date = pd.to_datetime(df.Date)

    df.drop(list(df.columns[1:][df.iloc[:,1:].sum(axis = 0) == 0]), axis = 1, inplace=True) 
    df.drop(['Grand Princess'], axis = 1, inplace = True)


    dfR = pd.DataFrame(np.empty_like(df))
    dfR.columns = df.columns
    dfR['Date'] = df['Date']
    
    
    for i in range(1, df.shape[1]):
        state = df.columns[i]
        j = np.where(df[state] > 0)[0][0]
        
        for m in range(j, df.shape[0]):
            if df.iloc[m, i] == 0:
                df.iloc[m, i] = df.iloc[m-1, i]

        dfR[state] = np.concatenate((np.full(j+5,np.nan), 
                                                pow(np.array(df[state][j+5:]) / np.array(df[state][j:df.shape[0]-5]), 1/5) - 1),
                                                axis = 0)  
    for i in range(1, dfR.shape[1]):
        s = [j for j in range(dfR.shape[0]) if not math.isnan(dfR.iloc[j,i])][0]
            
        for j in range(s+1, dfR.shape[0]-1):
            dfR.iloc[j, i] = np.mean([dfR.iloc[j-1, i],
                                                      dfR.iloc[j, i],
                                                      dfR.iloc[j+1, i]])
    return(dfR)

### World Confirmed
world_confirmedR = pd.read_csv("calculate_growth_rate_WORLD.csv")
#world_confirmedR.replace('United Kingdom', 'UK', inplace = True)
world_confirmedR.rename(columns = {'United Kingdom': 'UK'}, inplace = True)
#world_confirmedR = calculate_growth_rate_WORLD(world_confirmed)

### World Death
world_deathR = pd.read_csv("calculate_death_rate_WORLD.csv")
#world_deathR.replace('United Kingdom', 'UK', inplace = True)
world_deathR.rename(columns = {'United Kingdom': 'UK'}, inplace = True)
#world_deathR = calculate_growth_rate_WORLD(world_death)
### World color
random.seed(125)

# colors = [f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)' for _ in range(world_confirmedR.shape[1]-1)]
# colors_World = pd.DataFrame({'country': world_confirmedR.columns[1:],
#                              'colors': colors})
# colors_World = colors_World.set_index('country').to_dict()['colors']
####
color_list = pd.read_csv("color_list.csv",)
color_list = color_list.append(color_list)
color_list.reset_index(drop = True, inplace = True)
colors = ['rgba(' + str(color_list['r'][x]) + ',' + str(color_list['g'][x]) + ',' + str(color_list['b'][x]) + ',' + str(0.9) + ')' for x in range(color_list.shape[0])]
colors_World = pd.DataFrame({'country': world_confirmedR.columns[1:],
                             'colors': colors[:len(world_confirmedR.columns[1:])]
                            })
colors_World = colors_World.set_index('country').to_dict()['colors']

### US Confirmed
us_confirmed = pd.read_csv("JHU/time_series_covid19_confirmed_US.csv")
us_confirmedR = calculate_growth_rate_US(us_confirmed)
us_confirmedR.drop('Diamond Princess', axis = 1, inplace = True)
us_confirmedR.drop('Guam', axis = 1, inplace = True)
### US Death
us_death = pd.read_csv("JHU/time_series_covid19_deaths_US.csv")
us_death.drop('Population', axis = 1, inplace = True)
us_deathR = calculate_growth_rate_US(us_death)
### US color
colors = [f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)' for _ in range(us_confirmedR.shape[1]-1)]
colors_US = pd.DataFrame({'state': us_confirmedR.columns[1:],
                             'colors': colors})
colors_US = colors_US.set_index('state').to_dict()['colors']


### Lockdown world
lockdown = pd.read_csv("covid19-lockdown-dates-by-country/countryLockdowndatesJHUMatch.csv")
lockdown = lockdown.drop(['Reference'], axis = 1)
lockdown = lockdown.groupby(['Country/Region']).min().reset_index()
lockdown['Date'] = pd.to_datetime(lockdown['Date'])
lockdown['Country/Region'].replace('Mainland China', 'China', inplace = True)
lockdown['Country/Region'].replace('The Bahamas', 'Bahamas', inplace = True)
#lockdown['Country/Region'].replace('UK', 'United Kingdom', inplace = True)
lockdown['Type'].replace("Full", "full", inplace = True)
lockdown['Type'].replace("Partial", "partial", inplace = True)
lockdown['Type'].replace(np.nan, "lockdown", inplace = True)


### Lockdown US
lockdown2 = pd.read_csv("lockdown_us.csv")
lockdown2 = lockdown2.drop(['Country','County'], axis = 1)
lockdown2 = lockdown2.groupby(['State']).min().reset_index()
lockdown2 = lockdown2.append(pd.Series(['Arkansas', np.nan, np.nan], index = lockdown2.columns), ignore_index=True)

####################################################################################
#######################   Page 1 - Plot2.   Map Lockdown      ###################
####################################################################################
df_lockdown = pd.read_csv('lockdown_new.csv')
df_lockdown = df_lockdown[(df_lockdown['code']!= 'DC') ]
df_lockdown['order'] = df_lockdown['type'].map({0: 'No lockdown order', 0.5: 'Partial lockdown', 
                                                1:'Statewide lockdown',0.75:'Essential business reopen',
                                                0.55: 'Partial reopen'})
for col in df_lockdown.columns: 
    df_lockdown[col] = df_lockdown[col].astype(str)

df_lockdown['text'] = df_lockdown['date'] +'\n' + df_lockdown['state'] + ': ' + df_lockdown['order'] 
lockdown_date = list(df_lockdown.date.unique())

color1 = [ "#ead6ee", "#aebaf8"]
color2 = ["#e8f5c8","#aebaf8"]

#######world
df_world = pd.read_csv('countryLockdown_date.csv')

df_world['area'] = df_world['type'].map({0: 'No lockdown', 0.5: 'Partial lockdown', 1: 'Full lockdown'})

for col in df_world.columns: 
    df_world[col] = df_world[col].astype(str)
df_world['type']=df_world['type'].astype(float)
df_world['text'] = df_world['date'] + df_world['region'] + ': ' + df_world['area'] 
world_date = list(df_world.date.unique())
color_lock = [ 'rgb(204,230,255)', 'rgb(133,122,173)', 'rgb(105,10,61)']


####################################################################################
#######################   Page 2 - Plot1.   Mobility      ##########################
####################################################################################
# df_google = pd.read_csv('https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/US_Corona.csv')
# df_apple = pd.read_csv('apple_mobility.csv')
# # category dropdown 
# # state and county dropdown
# state = df_google['State'].unique()
# Dict = {}
# for s in state:
#     df_1 = df_google[df_google['State'] == s]
#     df_2 = df_1[['State', 'County']]
#     Dict[s] = df_2['County'].unique()

# opt_state = options=[{'label': k, 'value': k} for k in Dict.keys()]
# # date slide bar
# df_google['Date'] = pd.to_datetime(df_google.Date)
# df_apple['Date'] = pd.to_datetime(df_apple.Date)
# dates = ['2020-02-29', '2020-03-07', '2020-03-14', '2020-03-21',
#          '2020-03-28', '2020-04-04', '2020-04-11']

####################################################################################
#######################   Page 3 - Plot1.   Survey      ##########################
####################################################################################
### original
concern = pd.read_csv('covid-19-polls-master/covid_concern_polls.csv')

concern.drop(['start_date','party','tracking','text','url'], axis = 1, inplace=True)
concern.replace(np.nan, 'Others', inplace=True)

concern_econ = concern[concern['subject'] == 'concern-economy']
concern_infec = concern[concern['subject'] == 'concern-infected']


### adjusted
concern_adj = pd.read_csv("covid-19-polls-master/covid_concern_polls_adjusted.csv")

concern_adj.drop(['modeldate','party','startdate','multiversions','tracking','timestamp','url'],
                axis = 1, inplace = True)
concern_adj.rename(columns = {'enddate': 'end_date'}, inplace = True)
concern_adj['end_date'] = pd.to_datetime(concern_adj['end_date'])

concern_adj['population'].replace('a', 'All Adults', inplace = True)
concern_adj['population'].replace('rv', 'Registered Voters', inplace = True)
concern_adj['population'].replace('lv', 'Likely Voters', inplace = True)

concern_adj_econ = concern_adj[concern_adj['subject'] == 'concern-economy']
concern_adj_infec = concern_adj[concern_adj['subject'] == 'concern-infected']

### topline
concern_topline = pd.read_csv('covid-19-polls-master/covid_concern_toplines.csv')

concern_topline.drop(['party', 'timestamp'], axis = 1, inplace = True)
concern_topline['modeldate'] = pd.to_datetime(concern_topline['modeldate'])

concern_topline_econ = concern_topline[concern_topline['subject'] == 'concern-economy']
concern_topline_infect = concern_topline[concern_topline['subject'] == 'concern-infected']

### Supportive accessories
symbols1 = pd.DataFrame({'pollster':concern_adj_econ.pollster.unique(),
                          'symbol': ['diamond','circle','cross', 
                                     'triangle-up','square','triangle-right',
                                     'diamond-tall','y-down',
                                     'x','hourglass',
                                     'star','hexagram'
                                    ]}).set_index('pollster').to_dict()['symbol']

sponsors = list(concern_econ.sponsor.unique())
sponsors = [sponsors[0]] + sponsors[2:len(sponsors)] + [sponsors[1]]
symbols2 = pd.DataFrame({'sponsor':sponsors,
                          'symbol': ['diamond','circle','cross', 
                                     'triangle-up','square','triangle-right',
                                     'diamond-tall','hourglass',
                                     'star','hexagram'
                                    ]}).set_index('sponsor').to_dict()['symbol']

symbols3 = pd.DataFrame({'population':['All Adults', 'Registered Voters', 'Likely Voters'],
                          'symbol': ['cross','hexagram','circle'
                                    ]}).set_index('population').to_dict()['symbol']


### original
approval = pd.read_csv('covid-19-polls-master/covid_approval_polls.csv')

approval.drop(['start_date','subject', 'tracking','text','url'], axis = 1, inplace=True)
approval.replace(np.nan, 'Others', inplace=True)

approval['party'].replace('all', 'All', inplace = True)
approval['party'].replace('R', 'Republicans', inplace = True)
approval['party'].replace('I', 'Independents', inplace = True)
approval['party'].replace('D', 'Democrats', inplace = True)

### adjusted
approval_adj = pd.read_csv("covid-19-polls-master/covid_approval_polls_adjusted.csv")

approval_adj.drop(['subject','startdate','multiversions','tracking','timestamp','url'],
                axis = 1, inplace = True)
approval_adj.rename(columns = {'enddate': 'end_date'}, inplace = True)
approval_adj['end_date'] = pd.to_datetime(approval_adj['end_date'])

approval_adj['population'].replace('a', 'All Adults', inplace = True)
approval_adj['population'].replace('rv', 'Registered Voters', inplace = True)
approval_adj['population'].replace('lv', 'Likely Voters', inplace = True)

approval_adj['party'].replace('all', 'All', inplace = True)
approval_adj['party'].replace('R', 'Republicans', inplace = True)
approval_adj['party'].replace('I', 'Independents', inplace = True)
approval_adj['party'].replace('D', 'Democrats', inplace = True)

### topline
approval_topline = pd.read_csv('covid-19-polls-master/covid_approval_toplines.csv')

approval_topline.drop(['subject', 'timestamp'], axis = 1, inplace = True)
approval_topline['modeldate'] = pd.to_datetime(approval_topline['modeldate'])

approval_topline['party'].replace('all', 'All', inplace = True)
approval_topline['party'].replace('R', 'Republicans', inplace = True)
approval_topline['party'].replace('I', 'Independents', inplace = True)
approval_topline['party'].replace('D', 'Democrats', inplace = True)

### Supportive accessories
symbols4 = pd.DataFrame({'pollster':approval_adj.pollster.unique(),
                          'symbol': ['diamond','circle','cross', 'x','hourglass', 'cross','triangle-up','square','cross','hexagram','diamond',
                                     'triangle-up','square','triangle-right',
                                     'diamond-tall','y-down','x',
                                     'x','hourglass', 'triangle-right','star', 'hexagram','x',
                                     'diamond','circle','cross', 'square','triangle-right','cross',
                                     'diamond-tall','y-down','star'
                                     'star','circle','hexagram','diamond','star'
                                    ]}).set_index('pollster').to_dict()['symbol']
symbols5 = pd.DataFrame({'sponsor':approval.sponsor.unique(),
                          'symbol': ['diamond','circle','cross', 
                                     'triangle-up','square','triangle-right',
                                     'diamond-tall','square','x','x','hourglass','star', 'hexagram',
                                     'diamond','circle','cross', 
                                     'square','triangle-right','cross','star',
                                     'star','hexagram'
                                    ]}).set_index('sponsor').to_dict()['symbol']

symbols6 = pd.DataFrame({'party': ['Democrats', 'Republicans', 'Independents'],
                          'symbol': ['triangle-up', 'star', 'square']}).set_index('party').to_dict()['symbol']


####################################################################################
#######################   Page 3 - Plot2.   Twiter      ##########################
####################################################################################

# daterange = pd.DataFrame(pd.date_range(start='3/22/2020',end='4/22/2020',freq='D'), columns = ['date'])
# daterange['date'] = [x.timestamp() for x in daterange['date']]

daterange = pd.date_range(start='3/22/2020',end='4/29/2020',freq='D')
daterange = [str(pd.to_datetime(x, unit='s').date()) for x in daterange]



####################################################################################
#######################   Page 4 - Plot1.   Unemployment      #####################
####################################################################################
df_unemployment_rate = pd.read_csv('unemployment_rate.csv')

df_claims = pd.read_csv('unemployment_claims.csv')

df_map = pd.read_csv('unemployment_rate.csv')
for col in df_map.columns:
    df_map[col] = df_map[col].astype(str)
df_map['text'] = df_map['State'] + ': ' + df_map['UEP Rate'] 

## dropdown
features = df_unemployment_rate.State.unique()
opts = [{'label' : i, 'value' : i} for i in features]
## Range Slider
un_dates = list(df_unemployment_rate.Month.unique())
## Slider
date_map = list(df_map.Month.unique())


####################################################################################
#######################   Page 5 - Plot1.   Legislation      ######################
####################################################################################
legal = pd.read_csv('covid-19-legislation.csv')
legal.drop('Internal Quorum Link', axis = 1, inplace = True)
legal.rename(columns= {'Status Text': 'Status'}, inplace = True)
legal = legal[legal['Region'] != "Puerto Rico"].reset_index(drop = True)
legal.replace(np.nan, '', inplace = True)

legal['search_area'] = legal[['COVID-19 Legislation', 'Official Description']].agg('.'.join, axis=1)
legal['search_area'] = legal['search_area'].str.lower()
legal['search_area'] = [re.sub('[^A-Za-z0-9]+', ' ', str(x)) for x in legal['search_area']]
legal['search_area'] = [re.sub(' ', '', str(x)) for x in legal['search_area']]

legal['link'] = ['<a href="'] * len(legal['Source Link']) + legal['Source Link'] + ['">click here</a>']
legal['title'] = ['<a href="'] * len(legal['Source Link']) + legal['Source Link'] + ['">'] + legal['COVID-19 Legislation'] + ['</a>']
legal['c'] = np.full(legal.shape[0], 1)
legal['code'] = [x.split(':')[0] for x in legal['COVID-19 Legislation']]


######################################################################################################################
######################################################################################################################
#################################         2.  APP Layout              ################################################
######################################################################################################################
######################################################################################################################


#########################################
###########  Initiate the app  ##########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
local_stylesheets = ['style.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title="COVID19-visual_app_title"

#########################################
###########  Navigation  ################
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("COVID-19 Visualization", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

#########################################
###########  Body Elements  #############

FLATTEN_THE_CURVE = [
    dbc.CardHeader(html.H5("Flatten The Curve - US")),
    dbc.CardBody([
        html.P("This page evaluates the lockdown and growth rates timeline on two levels: national-wise and global-wise. In the US, 42 states were on lockdown by Apr 7 (marked red), whereas most states in the central US were already partially open by Apr 21. Most states which are partially open claimed the stay-at-home order earlier, whereas states with main metropolitan areas and cities generally started the lockdown later since there were more effects and concerns to lockdown major cities.", className="card-text"),
        html.P("On the global level, the line chart demonstrates which government handled the pandemic effectively. For instance, South Korea started the lockdown right at the first outbreak and effectively stopped the spreading of the virus. Unfortunately, Italy missed the best time to lock down the country, as shown that the stay-at-home order was not issued until several outbreaks.", className="card-text"),
        html.P("The visualization shows that the stay-at-home order has helped flatten the curve, since the growth rates of both new cases and death have been steadily decreasing since the lockdowns on both national-wide and world-wide levels.", className="card-text"),
        html.P("Select multiple countries in the dropdown and control the slider to see the change of the lockdown policy on the maps and the fluctuation of growth rate in confirmed cases and death through time on the line charts.", style={'color': 'blue'}),
        #print(world_confirmedR.columns),
        dbc.Row([
            html.Label("Select countries to include in the line plot:", style={'marginLeft':'10px', 'color': 'blue'}),
            dcc.Dropdown(
                        id = "selected_countries",
                        options=[{'label': x, 'value': x} for x in list(world_confirmedR.columns[1:])],
                        value= ['US', 'Italy','South Korea', 'India', 'Austria'],
                        multi=True,
                        style={'width': '99%', 'margin': '0px 5px 0px 5px'}
                        )
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map_lockdown'),
                dcc.Slider(id = 'lockdown_slider',
                                    marks = {0:{'label':'3/19/20'}, 6:{'label':'3/25/20'},
                                    12:{'label':'3/31/20'}, 19:{'label':'4/7','style': {'color': '#f50'}},
                                    20:{'label':'','style': {'color': '#f50'}},
                                    27:{'label':'4/30/20'}, 31:{'label':'5/4/20'} 
                                    },
                                    min = 0,
                                    max = 31,
                                    value = 16,
                                    included = False,
                                    updatemode='drag'                                    
                                    ) 
                ], width = 5),
            dbc.Col([
                html.Div([
                    html.Img(src = "assets/legend2.jpeg",
                            style = {'height': '100px', 'marginTop': '60px', 'float': 'left'})
                    
                ], style={'vertical-align': 'middle'})
                

                ],width = 1),
            dbc.Col([
                html.Div([], style={'height': '20px'}),
                html.Label('Select Metrics'),
                dcc.Dropdown(
                        id = "selected_measure",
                        options = [{'label': 'Confirmed Growth Rate', 'value': 'confirmed'},
                                   {'label': 'Death Growth Rate', 'value': 'death'}],
                        value = 'confirmed'
                        ),
                dcc.Graph(id = "lineplot1")

                ], width = 6)
            

        ]),

        dbc.CardHeader(html.H5("Flatten The Curve - Global"), style = {'marginTop': '20px'}),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label('Select states to include in the line plot: ',  style={'marginLeft':'10px', 'color': 'blue'}),
                    dcc.Dropdown(
                                id = "selected_states",
                                options=[{'label': x, 'value': x} for x in list(us_confirmedR.columns[1:])],
                                value= ['New York', 'California', 'Georgia', 'Pennsylvania', 'Colorado', 'Florida', 'Delaware'],
                                multi=True
                                )
                    ], width = 12)

                ]),
            
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Label('No Lockdown ', style = {'color': '#cce6ff', 'margin-right': '20px'}),
                    html.Label(' Partial Lockdown ', style = {'color': '#857aad', 'margin-right': '20px'}),
                    html.Label(' Full Lockdown ', style = {'color': '#690a3d'}),
                    #html.P("Light Blue: No Lockdown, Purple: Partial Lockdown, Maroon: Full Lockdown "),
                    dcc.Graph(id='world_lockdown_map'),
                    dcc.Slider(id = 'world_lockdown_slider',
                                        marks = {0:{'label':'Jan 23'}, 1:{'label':''}, 2:{'label':''}, 3:{'label':'Feb 25'}, 
                                        4:{'label':''}, 5:{'label':''}, 6:{'label':'Mar 5'}, 7:{'label':''}, 
                                        8:{'label':''}, 9:{'label':''}, 10:{'label':'Mar 10'}, 11:{'label':''}, 
                                        12:{'label':''}, 13:{'label':''}, 14:{'label':''}, 15:{'label':'Mar 15'}, 
                                        16:{'label':''}, 17:{'label':''}, 18:{'label':''}, 19:{'label':''}, 
                                        20:{'label':'Mar 20'}, 21:{'label':''}, 22:{'label':''}, 23:{'label':''}, 
                                        24:{'label':''}, 25:{'label':'Mar 25'}, 26:{'label':''}, 27:{'label':''}, 
                                        28:{'label':''}, 29:{'label':''}, 30:{'label':'Mar 30'}, 31:{'label':''}
                                        },
                                        min = 0,
                                        max = 31,
                                        value = 16,
                                        included = False,
                                        updatemode='drag'                                    
                                        )   

                    ], width = 5),
                # dbc.Col([
                #     html.Div([
                #          html.Img(src = "assets/legend4.jpeg", style = {'height': '70%', 'marginTop': '60px', 'float': 'left'
                #                 ,'width':'70%'})
                #         ], style={'vertical-align': 'middle'})
                # ],width = 0.5),

                dbc.Col([
                    html.Div([], style={'height': '20px'}),
                    html.Label('Select Metrics'),
                    dcc.Dropdown(
                            id = "selected_measure2",
                            options = [{'label': 'Confirmed Growth Rate', 'value': 'confirmed'},
                                    {'label': 'Death Growth Rate', 'value': 'death'}],
                            value = 'confirmed'
                            ),
                    dcc.Graph(id = "lineplot2")

                    ], width = 7),
            
            
        ]),
        
        ])



        ])

]


#FLATTEN_THE_CURVE2 = [
    #dbc.CardHeader(html.H5("Flatten The Curve")),
    #dbc.CardBody([
        #dcc.Loading(),
        #dcc.Tabs([
            #dcc.Tab(label='World', children=[
                            # html.Div([
                            #     html.Label('Multi-Select Dropdown'),
                            #     dcc.Dropdown(
                            #         id = "selected_countries",
                            #         options=[{'label': x, 'value': x} for x in list(world_confirmedR.columns[1:])],
                            #         value= ['US','United Kingdom', 'Italy', 'Germany', 'Spain', 'South Korea', 'India', 'Austria'],
                            #         multi=True
                            #         ),
                            #     dcc.Dropdown(
                            #         id = "selected_measure",
                            #         options = [{'label': 'Confirmed Growth Rate', 'value': 'confirmed'},
                            #                    {'label': 'Death Growth Rate', 'value': 'death'}],
                            #         value = 'confirmed'
                            #         )

                            # ], style={'marginLeft': '0px', 'marginRight': '0px', 'padding-left': '0px', 'padding-right': '0px'}),

                            # html.Div([
                            #     html.Label("my plot here"),
                            #     dcc.Graph(id = "lineplot1")
                            # ], style={'marginLeft': '0px', 'marginRight': '0px', 'padding-left': '0px', 'padding-right': '0px',
                            # }),
                
            #]),

            #dcc.Tab(label='US', children=[
                            # html.Div([
                            #     html.Label('Multi-Select Dropdown'),
                            #     dcc.Dropdown(
                            #         id = "selected_states",
                            #         options=[{'label': x, 'value': x} for x in list(us_confirmedR.columns[1:])],
                            #         value= ['New York', 'California'],
                            #         multi=True
                            #         ),
                            #     dcc.Dropdown(
                            #         id = "selected_measure2",
                            #         options = [{'label': 'Confirmed Growth Rate', 'value': 'confirmed'},
                            #                    {'label': 'Death Growth Rate', 'value': 'death'}],
                            #         value = 'confirmed'
                            #         )

                            # ], style={'marginLeft': '0px', 'marginRight': '0px', 'padding-left': '0px', 'padding-right': '0px'}),

                            # html.Div([
                            #     html.Label("my plot here"),
                            #     dcc.Graph(id = "lineplot2")
                            # ], style={'marginLeft': '0px', 'marginRight': '0px', 'padding-left': '0px', 'padding-right': '0px'})
            #])

        #])

    #])


#]

MAP_LOCKDOWN = [

    #dbc.CardBody([
        html.Div([  
                dcc.Graph(id='map_lockdown'),
                # Add a slider
                html.P([
                    html.Label("Time"),
                    # dcc.Slider(id = 'lockdown_slider',
                    #                 marks = {0:{'label':'3/19/20'}, 6:{'label':'3/25/20'},
                    #                 12:{'label':'3/31/20'}, 19:{'label':'4/7','style': {'color': '#f50'}},
                    #                 20:{'label':'4/21','style': {'color': '#f50'}},
                    #                 27:{'label':'4/30/20'}, 31:{'label':'5/4/20'} 
                    #                 },
                    #                 min = 0,
                    #                 max = 31,
                    #                 value = 16,
                    #                 included = False,
                    #                 updatemode='drag'                                    
                    #                 )           
                        ],  style = {
                                    'width' : '87%',
                                    'fontSize' : '20px',
                                    'padding-left' : '60px',
                                    'padding-right' : '100px',
                                    'display': 'inline-block'
                                    }),
                html.Div([
                    #html.H1("This is my first dashboard"),
                    html.P("Notes: "),
                    html.P("1) Until Apr 7, 42 states have implemented stay-at-home orders."),
                    html.P("2) Started from Apr 21, governers have taken different stategies to reopen their states."),
                    html.P("Data Source: CNN, The New York Times, CNBC")
                         ],
                     style = {'padding' : '50px' }
                    )
                ])

        #])
]

# MOBILITY = [
#     dbc.CardHeader(html.H5('Mobility: Are people really following the stay-at-home rules?')),
#     dbc.CardBody([
#         dbc.Row([
#             dbc.Col([
#                 html.Label("Choose a state")
#                 ], width = 6),
#             dbc.Col([
#                 html.Label("Choose a county")
                    
#                 ], width = 6)
#             ])
    
#         ])
# ]

MOBILITY =[
    dbc.CardHeader(html.H5('Mobility: Are people really following the stay-at-home rules?')),
    dbc.CardBody([
        html.P("This page presents mobility data in the US and some main cities around the world. The mobility data in the US is derived from aggregated and anonymized data used to show popular times for places in Google Maps. These plots show how visits and length of stay at different places change compared to a baseline, which is the median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020. The x-axis represents the timeline, and the y-axis shows the percentage of mobility change compared to the baseline."),
        html.P("It shows that since March, people around the world have been staying at home more often and stopped traveling around as much. Moreover, in the line chart where the mobility is broken down into 6 categories, there are some interesting periodical patterns: "),
        html.Label('- Retail ', style = {'color': '#b39536', 'font-weight':'bold', 'margin-right': '10px'}), 
        html.Label('&'),
        html.Label(' Transit: ',  style = {'color': '#8c868f', 'font-weight':'bold', 'margin-left': '10px'}),
        html.Label('People stopped going to malls (retails) and taking public transportation since mid-March, when most states started the lockdown.'),
        html.Br(),
        html.Label('-  Work place ',  style = {'color': '#853bd4', 'font-weight':'bold', 'margin-right': '10px'}), 
        html.Label('&'),
        html.Label(' Residential Neighborhood: ',  style = {'color': '#cf30bc', 'font-weight':'bold', 'margin-left': '10px'}),
        html.Label(' These two show almost mirrored opposite trends, but the identical periodic pattern, which is very interesting! Also, since around March 16, an obvious weekly pattern started to emerge. People seemed to adjust their life and get used to working-at-home and yet still maintain a relatively regular weekly schedule. Funny thing is, people seemed to shortly stop by their office on weekends! '),    


        html.Br(),
        html.Label('-  Grocery ',  style = {'color': '#52bfbf', 'font-weight':'bold', 'margin-right': '10px'}), 
        html.Label('&'),
        html.Label(' Parks: ',  style = {'color': 'green', 'font-weight':'bold', 'margin-left': '10px'}),
        html.Label(' Similar trends but different details! Right before lockdown, these two places were hot! People rushed into stores to hoard goods and groceries, and hangout in the park more than usual. After lockdown, people have been going grocery shopping and hiking less often as they become more cautious about going outside. But unlike the pattern shown in the other four areas, trends in Grocery & Parks still go up to the axis once a while throughout the weeks, as people still need to go get groceries and take a walk from time to time.'),           
    
        html.Br(),
        html.Label('Periodic Pattern: ', style = {'background-color': 'lightgrey', 'margin-right': '20px'}),
        html.Label('The plots also show that people were not used to the quarantine life at the beginning of the lockdown, but most people quickly adapted and eventually developed their routines for activities such as grocery shopping, working from home, etc. Since around March 16, the plot started to show a clear weekly pattern.'),
            
        html.Br(),
        html.Label('Turning Point (from positive to negative): ', style = {'background-color': 'lightgrey', 'margin-right': '20px'}),
        html.Label('The point when the percentage of mobility change (compared to the historical baseline) switches from positive to negative (meaning from more than old days to less than old days, or the other direction for Residential) varies among places. Transit [Mar 9], Workplace [Mar 9], Residential [Mar 9] are the earliest, probably because most people started working from home after the first week of March. The other turning points are Retail [Mar 13], when most malls and shopping centers were closed since mid-March. Lastly, Parks [Mar 20] and Grocery [Mar 21] reached their turning points in late March, because at the beginning of the quarantine, people were panic buying groceries and they believed that hiking would still be safe. As the number of cases increased, people were more concerned about going outside.'),

        html.Br(),
        html.Label('Overall, the mobility page shows that people are generally following the stay-at-home order.'),

        html.Br(),
        html.Label('Use the dropdown to select states and counties and adjust the slider to view the change of mobility over time.', style={'color': 'blue'}),
    
    dbc.Row([
            dbc.Col([
                html.Iframe(src = " https://hack-cov19.herokuapp.com/", width="100%", height = '600px')
                #html.Iframe(src = "https://www.youtube.com/embed/zWfyxknakAs", width="100%", height = '600px')
                ], width = 12)
            ])

        ])
    ]


INTRO =[
    dbc.CardHeader(html.H5('Project Overview')),
    dbc.CardBody([
        html.H3("Impacts of COVID-19 and Government’s Responses "),
        html.Br(),
        html.H5("Group Members: Beixuan Jia, Luwei Lei, Miao Wang, Yuxin Zhang"),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Img(src = "https://media.npr.org/assets/img/2020/03/21/ap_20081027616567-3b72d64770e83cd39f74c16df178c55feef9b8d6-s800-c85.jpg", width = '100%')
                ], width = 6),
            dbc.Col([
                html.P("The pandemic of COVID-19 has become one of the major challenges of global public health. To help the public and decision-makers better understand the trend and the influence of COVID-19, this project not only creates visualizations to demonstrate the underlying patterns of COVID-19 and its impacts, but also added interactive features which allow users to focus on many of the relevant aspects and obtain interesting findings through the extensive information. The website contains six tabs, representing COVID-19’s overview and its impacts on Lockdown, Mobility, Public Opinion, Unemployment, and Legislation to answer if the curve has been flattened through various perspectives such as social media, mobility, unemployment, etc.", className="card-text"),
                html.Br()
                ], width = 6)
            ]),
        html.Br(),
        html.H6("Data Source:"),
        html.P(['   1. ', html.A("Johns Hopkins Coronavirus Dashboard Dataset", href='https://github.com/CSSEGISandData/COVID-19')]),
        html.P(['   2. ', html.A("1Point3Acres covid19 dataset", href='https://coronavirus.1point3acres.com/en')]),
        html.P(['   3. ', html.A("Worldwide Lockdown Dataset", href='https://www.kaggle.com/jcyzag/covid19-lockdown-dates-by-country#countryLockdowndates.csv')]),
        html.P(['   4. ', html.A("US Lockdown Dataset", href='https://www.kaggle.com/lin0li/us-lockdown-dates-dataset')]),
        html.P(['   5. ', html.A("Google Trends", href='https://trends.google.com/trends/?geo=US')]),
        html.P(['   6. ', html.A("Covid-19 Twitter dataset", href='https://github.com/thepanacealab/covid19_twitter/tree/master/dailies/2020-03-22')]),
        html.P(['   7. ', html.A("COVID-19 Legislation", href='https://www.quorum.us/spreadsheet/external/QCKYcPmSvYoAhnkIdcSS/')]),
        html.P(['   8. ', html.A("Google COVID-19 Community Mobility Reports", href='https://www.google.com/covid19/mobility/')]),
        html.P(['   9. ', html.A("Apple Mobility Data", href='https://www.apple.com/covid19/mobility')]),
        html.P(['   10. ', html.A("538 Survey Data on US Coronavirus Concern and Response Approval", href='https://projects.fivethirtyeight.com/coronavirus-polls/')]),
        html.P(['   11. ', html.A("U.S. Bureau of Labor Statistics", href='https://data.bls.gov/timeseries/LNS14000000')]),
        html.P(['   12. ', html.A("U.S. Department of Labor", href='https://oui.doleta.gov/unemploy/claims.asp')]),
        html.P('   13. Lockdown News from CNN'),
        html.P('   14. Lockdown News from The New York Times'),
        html.P('   15. Lockdown News from CNBC'),
        html.P(['   16. ', html.A("National Public Radio News", href='https://www.npr.org/2020/03/21/819511621/coronavirus-deaths-spike-abroad-as-new-york-city-becomes-u-s-virus-epicenter')]),
        html.Br(),
        html.H6("Tools & Packages:"),
        html.P('Python, Dash, Plotly, Flourish, Heroku')
        ])
    ]

SURVEY_MEDIA = [
    dbc.CardHeader(html.H5("Survey")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H5("Select Topics :")
                ], width = 2),
            dbc.Col([
                dcc.Dropdown(
                    id = 'selected_question',
                    options = [{'label': 'How concerned are Americans about Infection?', 'value': 'Q_concern_infec'},
                               {'label': 'How concerned are Americans about Economy?', 'value': 'Q_concern_econ'},
                               {'label': 'Do Americans approve of Trump’s response to the coronavirus crisis?', 'value': 'Q_approval'}],
                    value = 'Q_concern_econ'
                    )

                ], width = 10),

            ]),
        html.P("The Public Opinion page researched people’s opinions and concerns during the pandemic through surveys, social media posts and google search trends. This page was inspired by 538 survey website and gathered people’s opinion on three topics. Use the dropdown above to select a topic. Surveys show that after the first death in the US, people started to become more worried. Interestingly, registered voters and likely voters are generally less worried about COVID-19 than average Americans. Surveys sponsored by Fortune always show a less optimistic attitude towards the economy compared to average surveys, whereas surveys sponsored by CNBC generally receive more optimistic responses."),
        html.P("Use the dropdown to select topics. Use the radio button and select multiple sources of surveys in blank to see the comparison among participants’ opinions. ", style={'color': 'blue'}),
        dbc.Row([
            dbc.Col([
                html.H5("Choose Filter :"),
                html.Img(src = "https://media.istockphoto.com/vectors/survey-satisfaction-scale-meter-emoticon-talk-bubbles-icons-vector-id1186938974?k=6&m=1186938974&s=170667a&w=0&h=JtfZXrP90BGvdKktvqM8dZsLauT2uyjRW9JoCF1PCkQ=",
                style = {"width" : '135px'})
                ], width = 2),
            dbc.Col([
                dcc.RadioItems(
                        id = 'radio_display1',
                        options=[{'label': 'All   ', 'value': 'All'},
                                {'label': 'By Pollster   ', 'value': 'by_pollster'},
                                {'label': 'By Sponsor  ', 'value': 'by_sponsor'},
                                {'label': 'By Population', 'value': 'by_population'},
                                {'label': 'By Party', 'value': 'by_party'}
                                ],
                        value='All',
                        labelStyle={'display': 'block'}, style={'fontSize': 14, 'marginTop': '5px'}
                        )

                ], width = 2),
            dbc.Col([
                dcc.Dropdown(
                                id = "selected_pollsters",
                                # options = [{'label': 'All', 'value': 'All'}] +
                                #           [{'label': x, 'value': x} for x in list(concern_adj_econ.pollster.unique())],
                                multi=True,
                                style={'height': '100px', 'marginTop': '10px'}
                                )

                ], width = 8)
            ]),


        dcc.Graph(id = "survey_plot1")


        ])

]

markdict = {0: {'label': '3-22'},
            1: {'label': ''}, 2: {'label': ''}, 3: {'label': ''}, 4: {'label': ''},
            5: {'label': '3-27'}, 
            6: {'label': ''}, 7: {'label': ''}, 8: {'label': ''}, 9: {'label': ''},
            10: {'label': '4-01'},
            11: {'label': ''}, 12: {'label': ''}, 13: {'label': ''}, 14: {'label': ''},
            15: {'label': '4-06'},
            16: {'label': ''}, 17: {'label': ''}, 18: {'label': ''}, 19: {'label': ''},
            20: {'label': '4-11'},
            21: {'label': ''}, 22: {'label': ''}, 23: {'label': ''}, 24: {'label': ''},
            25: {'label': '4-16'}, 
            26: {'label': ''}, 27: {'label': ''}, 28: {'label': ''}, 29: {'label': ''},
            30: {'label': '4-21'},
            31: {'label': ''}, 32: {'label': ''}, 33: {'label': ''}, 
            34: {'label': '4-25'},
            35: {'label': ''}, 36: {'label': ''}, 37: {'label': '4-28'},
            38: {'label': ''}}

TWEETER = [
    dbc.CardHeader(html.H5('Twitter HoT Words ')),
    dbc.CardBody([
        html.P("The image on the left is a word cloud for hot debating topics on Twitter. The table on the right displays the top keywords with their popularities. The yellow text means the rank of popularity increased compared to the day before, green means the rank dropped and red means it is a new topic."),
        html.P("Control the slider to check Twitter trending words on a selected day. ", style={'color': 'blue'}),
        dbc.Row([
            dbc.Col([
                dcc.Slider(
                        id='year-slider',
                        updatemode = 'mouseup',
                        min=0,
                        max=38,
                        value=38,
                        marks=markdict,
                        step=1,
                        included=False)
                ], width = 12)
            ]),
        dbc.Row([
            dbc.Col([
                html.Div(id="image", style = {'width': '100%', 'margin-top': '100px'})
                ], width = 7),
            dbc.Col([
                dcc.Graph(id ='hot-table', style={'display': 'inline-block','width':'100%', 'margin-top': '30px'})
                ], width = 5)

            ])

        ])
]


GOOGLE =[
    dbc.CardHeader(html.H5('Google Search Trend')),
    dbc.CardBody([
        html.P("The google search keywords and Twitter hot words show the change of trending topics since the lockdown. Before the lockdown, people paid close attention to the information about COVID-19, whose main source had changed from the JHU to CDC website. Since the quarantine started, besides the virus, people started to spend more time searching for online-streaming services (Netflix) and online shopping websites (Amazon). Google Classroom shows a steadily high search trend. Meanwhile, people still care about news and trending topics such as the stock, oil trading, stimulus check, NFL, Tiger King, Kim Jong Un, etc. Discussions about political figures, especially the senators and presidential candidates, were also trending, since people paid close attention to how they handle the pandemic. More recently, people started searching more about reopening the state and protests. It proves that people’s concerns are mainly related to COVID-19’s impacts and the government’s response, and the concerns shift through time."),
        html.P("Use the slider on the bottom of the bar racing chart to see the change of trending topics in a certain time period.", style={'color': 'blue'}),

        dbc.Row([
            dbc.Col([
                html.Iframe(src = "https://public.flourish.studio/visualisation/2211837/", width="100%", height = '600px')
                ], width = 6),

            dbc.Col([
                #dbc.Jumbotron([
                html.Img(src = "assets/googleTrend5.png", height = '600px')
                #    ])
                
                ], width = 6)
            ])

        ])

    ]

UNEMPLOYMENT = [
    dbc.CardHeader(html.H5("Unemployment")),
    dbc.CardBody([
        html.P("This Page examines the unemployment rate by each US State since 2015. Before the pandemic, the unemployment rate was gradually going down, whereas the unemployment rate started rising again since the outbreak of COVID-19. Especially at the end of March 2020, when most states started the lockdown, the number of unemployment claims has grown significantly. This page reveals that the unemployment condition in each state is closely related to its economic structure. The most impacted states include those whose major economic sectors are tourism, such as Florida and Colorado. States which rely more on manufacturing would also expect growth in unemployment rates during the pandemic."),
        html.P("The unemployment rate decreased for the year but sharply increased in Mar 2020. Meanwhile,  the unemployment claims boosted as more states were locked down and people lost their jobs."),
        html.P("Use both pointers on the slider to control a certain period of time in the plot. The left pointer also controls the timestamp for the map, which compares the unemployment rate among states.", style={'color': 'blue'}),
        html.P("The US map on the left shows the unemployment rate by states. The line chart on the top right describes the changes in the unemployment rate by states. The line chart on the bottom right reveals the increasing unemployment claims by weeks."),
        html.P("Use the dropdown to select multiple states to include in the line chart and compare the unemployment rate and unemployment claims.", style={'color': 'blue'}),
        dbc.Row([
                dbc.Col([
                # html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'RangeSlider',
                                    marks = {0:{'label':'Jan 2015'}, 1:{'label':''}, 2:{'label':''}, 3:{'label':''}, 
                                    4:{'label':''}, 5:{'label':''}, 6:{'label':'July 2015'}, 7:{'label':''}, 
                                    8:{'label':''}, 9:{'label':''}, 10:{'label':''}, 11:{'label':''}, 
                                    12:{'label':'Jan 2016'}, 13:{'label':''}, 14:{'label':''}, 15:{'label':''}, 
                                    16:{'label':''}, 17:{'label':''}, 18:{'label':'July 2016'}, 19:{'label':''}, 
                                    20:{'label':''}, 21:{'label':''}, 22:{'label':''}, 23:{'label':''}, 
                                    24:{'label':'Jan 2017'}, 25:{'label':''}, 26:{'label':''}, 27:{'label':''}, 
                                    28:{'label':''}, 29:{'label':''}, 30:{'label':'July 2017'}, 31:{'label':''}, 
                                    32:{'label':''}, 33:{'label':''}, 34:{'label':''}, 35:{'label':''}, 
                                    36:{'label':'Jan 2018'}, 37:{'label':''}, 38:{'label':''}, 39:{'label':''}, 
                                    40:{'label':''}, 41:{'label':''}, 42:{'label':'July 2018'}, 43:{'label':''}, 
                                    44:{'label':''}, 45:{'label':''}, 46:{'label':''}, 47:{'label':''},
                                    48:{'label':'Jan 2019'}, 49:{'label':''}, 50:{'label':''}, 51:{'label':''}, 
                                    52:{'label':''}, 53:{'label':''}, 54:{'label':'July 2019'}, 55:{'label':''}, 
                                    56:{'label':''}, 57:{'label':''}, 58:{'label':''}, 59:{'label':''}, 
                                    60:{'label':'Jan 2020'}, 61:{'label':''}, 62:{'label':'Mar 2020'}},
                                    min = 0,
                                    max = 62,
                                    value = [25, 62],
                                    allowCross=True
                                    )           
                        # ],  style = {
                        #             'width' : '87%',
                        #             'fontSize' : '20px',
                        #             'padding-left' : '60px',
                        #             'padding-right' : '100px',
                        #             'display': 'inline-block'
                        #             })

                ], width = 12)

            ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map')
                ], width = 6),
            dbc.Col([
                dbc.CardBody([
                    dbc.Row([dcc.Graph(id = 'plot1')]),
                    dbc.Row([dcc.Graph(id = 'plot2')])

                    ])
                ], width = 6),
            dbc.Col([
                # html.P([
                    html.Label("Select any states"),
                    dcc.Dropdown(id = 'opt', 
                                 options = opts,
                                 placeholder="Select any states",
                                 value = [opts[5]['value'],opts[19]['value'],  opts[31]['value'],opts[45]['value']],
                                 searchable=True,                              
                                 multi=True)
                        # ], style = {'width': '400px',
                        #             'fontSize' : '20px',
                        #             'padding-left' : '100px',
                        #             'display': 'inline-block'})

                ], width = 12)

            ])

        ])

]

LEGAL_TABLE = [
    dbc.CardHeader(html.H5("Legislation Search Table")),
    dbc.CardBody([
        html.Label("This page demonstrates the COVID-19 related legislation in each state. "), 
        html.Label('Search certain legislations by keywords (separate each keyword by comma and press enter), states, or their status. On the right side, users can directly browse through the proposal code by zooming in the bar chart or sliding mouse over the stack like searching in a book shelf.' , style={'color': 'blue'}),
        html.Label("Detailed information about each legislation is displayed in the table on the left."),
        dbc.Row([
            dbc.Col([
                html.Label("Search By Keywords", style = {'fontSize': 15}),
                dcc.Input(id = "search_text",
                            type = 'search',
                            placeholder="Example: covid19, unemployment",
                            debounce = True,
                            style={'width': 330, 'height': 36})

                ], width = 4),

            dbc.Col([
                html.Label("Search By States", style = {'fontSize': 15}),
                dcc.Dropdown(
                    id = 'selected_state',
                    options = [{'label': x, 'value': x} for x in legal['Region'].unique()])
                ], width = 4),
            dbc.Col([
                html.Label("Search By Status", style = {'fontSize': 15}),
                dcc.Dropdown(
                    id = 'selected_status',
                    options = [{'label': x, 'value': x} for x in legal['Status'].unique()])
                ], width = 4)

            ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id = "legal_table")
                ], width = 6),
            dbc.Col([
                dcc.Graph(
                    figure = px.bar(legal, x="c", y="Region", color='Status', orientation='h', text = 'code',
                         height=580, 
                         color_discrete_sequence=["#DB5461", "#FAC9B8","#749BC1","#98A6D4",'#F4E409','#A6D3A0'],
                        ).update_traces(hovertemplate= '<b>%{text}</b>')
                         .update_layout(xaxis_showgrid=False, yaxis_showgrid=False, legend_orientation="h",
                                        font=dict(size=8),
                                        legend=dict(x=-.1, y=1.09),
                                        margin=dict(l=0, r=0, t=50, b=0, pad=0),
                                        plot_bgcolor='#f5f7fa')
                         .update_xaxes(title_text='').update_yaxes(title_text=''),
                    )

                ], width = 6, style = {'borderLeft': 'thin darkgrey solid', 'padding': '2px 15px 0px 0px',
                                       'margin': '10px 0px 0px 0px'})
            
            ])
            
        ])

]

######################################################
#################     Body    ########################
BODY = dbc.Container([

    dcc.Tabs(
        #parent_className='custom-tabs',
        #className='custom-tabs-container',
        children = [

        dcc.Tab(label='Overview', children=[
            dbc.Row([dbc.Col(dbc.Card(INTRO)),], style={"marginTop": 30})
            ], className='custom-tab'),

        dcc.Tab(label='Lockdown', children=[
            dbc.Row([dbc.Col(dbc.Card(FLATTEN_THE_CURVE)),], style={"marginTop": 30})
            #dbc.CardHeader(html.H5("Flatten The Curve")),
                # dbc.CardBody([
                #     dbc.Row([
                #         dbc.Col([
                #             dbc.Card(FLATTEN_THE_CURVE)
                #             ], width = 6),

                #         dbc.Col([
                #             dbc.Card(MAP_LOCKDOWN)
                #             ], width = 6)
                #         ])
                #     ])
            #dbc.Row([dbc.Col(dbc.Card(FLATTEN_THE_CURVE)),], style={"marginTop": 30})

            ], className='custom-tab'),

        dcc.Tab(label='Mobility', children=[
            dbc.Row([dbc.Col(dbc.Card(MOBILITY)),], style={"marginTop": 30})

            ], className='custom-tab'),

        dcc.Tab(label='Public Opinion', children=[
            dbc.Row([dbc.Col(dbc.Card(SURVEY_MEDIA)),], style={"marginTop": 30}),
            dbc.Row([
                dbc.Col([
                    dbc.Card(GOOGLE)
                    ], width = 12),
                dbc.Col([
                    dbc.Card(TWEETER)
                    ], width = 12)
                ], style={"marginTop": 20})

        


            # dcc.Tabs([
            #     dcc.Tab(label='Survey', children=[
            #         dbc.Row([dbc.Col(dbc.Card(SURVEY_MEDIA)),], style={"marginTop": 30})

            #         ], className='custom-tab'),
            #     dcc.Tab(label='Tweeter', children=[
            #         ])


            #     ], vertical = True, parent_className='custom-tabs', className='custom-tabs-container')

            ]),

        dcc.Tab(label='Unemployment', children=[
            dbc.Row([dbc.Col(dbc.Card(UNEMPLOYMENT)),], style={"marginTop": 30})

            ]),

        dcc.Tab(label='Legislation', children=[
            dbc.Row([dbc.Col([dbc.Card(LEGAL_TABLE)])], style={"marginTop": 50})

            ]),

        ], colors={"border": "white", "primary": "gold", "background": "cornsilk"
    })
        
    ]
    #,className="no_margin_container",
    ,className="mt-12",
)



app.layout = html.Div(children=[NAVBAR, BODY])


######################################################################################################################
######################################################################################################################
#################################         3.  CALLLBACKS             ################################################
######################################################################################################################
######################################################################################################################


####################################################################################
#######################   Page 1 - Plot1.   Flatten the Curve      ################
####################################################################################

@app.callback(dash.dependencies.Output("lineplot1", "figure"),
    [dash.dependencies.Input("selected_countries", "value"),
     dash.dependencies.Input("selected_measure", "value")])

def update_fig(selected_countries, selected_measure):

    data = []
    US = []
    IT = []
    SK = []


    if selected_measure == "confirmed":
        df = world_confirmedR
    elif selected_measure == "death":
        df = world_deathR

    if "US" in selected_countries:
        US = [go.Scatter(x = df.Date,
                             y = df['US'],
                             name = 'US',
                             mode = 'lines',
                             line = dict(color = 'rgba(53,92,125, 0.8)', width = 3, shape = 'spline'),
                             #text = ["United States" if i == 38 else "" for i in range(df.shape[0])],
                             #textposition = "top center",
                             #textfont = dict(color = "rgba(53,92,125, 1)")
                            ),
              go.Scatter(x = df.Date,
                          y = [df['US'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          name = 'US (partial lockdown)',
                          mode = 'markers',
                          marker = dict(color = 'rgba(53,92,125, 0.8)', size = 10),
                          text = ["Partial lockdown" if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else "" for i in range(df.shape[0])],
                          textposition="top right",
                          textfont = dict(color = "rgba(53,92,125, 1)")
                            )]
        selected_countries.remove('US')
    
    if "Italy"  in selected_countries:
        IT = [go.Scatter(x = df.Date,
                             y = df['Italy'],
                             name = 'Italy',
                             mode = 'lines',
                             line = dict(color = 'rgba(153,184,152, 0.9)', width = 3, shape = 'spline'),
                            ),
              go.Scatter(x = df.Date,
                          y = [df['Italy'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'Italy'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          mode = 'markers',
                          name = 'Italy (full lockdown)',
                          marker = dict(color = 'rgba(153,184,152, 0.9)', size = 10),
                            )]
        selected_countries.remove('Italy')

    # if "Spain" in selected_countries:
    #     SP = [go.Scatter(x = df.Date,
    #                          y = df['Spain'],
    #                          name = 'Spain',
    #                          mode = 'lines',
    #                          line = dict(color = 'rgba(237, 177, 131, 0.9)', width = 3, shape = 'spline'),
    #                         ),
    #           go.Scatter(x = df.Date,
    #                       y = [df['Spain'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'Spain'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
    #                       mode = 'markers',
    #                       marker = dict(color = 'rgba(237, 177, 131, 0.9)', size = 10),
    #                       #text = ["Full" if lockdown.Date[lockdown['Country/Region'] == 'Spain'].values == df.Date[i] else "" for i in range(df.shape[0])],
    #                       #textposition="top right"
    #                         )]
    if "South Korea" in selected_countries:
        SK = [go.Scatter(x = df.Date,
                             y = df['South Korea'],
                             name = 'South Korea',
                             mode = 'lines',
                             line = dict(color = 'rgba(246,114,128, 0.9)', width = 3, shape = 'spline'),
                            ),
              go.Scatter(x = df.Date,
                          y = [df['South Korea'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'South Korea'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          mode = 'markers',
                          name = 'South Korea (full)',
                          marker = dict(color = 'rgba(246,114,128, 0.9)', size = 10),
                          #text = ["Full" if lockdown.Date[lockdown['Country/Region'] == 'South Korea'].values == df.Date[i] else "" for i in range(df.shape[0])],
                          #textposition="top right"
                            )]
        selected_countries.remove('South Korea')


    others1 = [go.Scatter(x = df.Date, 
                        y = df[selected_countries[i]],
                        name = selected_countries[i],
                        mode = 'lines',
                        line = dict(color = colors_World[selected_countries[i]], 
                            width = 2, shape = 'spline')) for i in range(len(selected_countries))]
    others2 = [go.Scatter(x = df.Date,
                          y = [df[selected_countries[i]][j] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == selected_countries[i]].values) == pd.Timestamp(df.Date.iloc[j]) else np.nan for j in range(df.shape[0])],
                          name = selected_countries[i] + ' (' + str(lockdown.Type[lockdown['Country/Region'] == selected_countries[i]].values[0]) + ')',
                          mode = 'markers',
                          marker = dict(color = colors_World[selected_countries[i]],  size = 5),
                          #text = [lockdown['Type'][lockdown['Country/Region'] == selected_countries[i]].values[0] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == selected_countries[i]].values) == pd.Timestamp(df.Date.iloc[j]) else "unknown type" for j in range(df.shape[0])],
                          #textposition="top right"
                            ) for i in range(len(selected_countries))]

    

    data = data + US + IT + SK + others1 + others2 

    if selected_measure == "confirmed":
        layout = {"title": "Confirmed Case Growth Rate ", "height": 450, "plot_bgcolor": '#f5f7fa',
                    "margin": "l=0, r=0, t=50, b=0, pad=0", 'hovermode': 'closest'}
    elif selected_measure == "death":
        layout = {"title": "Death Case Growth Rate", "height": 450, "plot_bgcolor": '#f5f7fa',
                     "margin": "l=0, r=0, t=50, b=0, pad=0", 'hovermode': 'closest'}


    return dict(data = data,
                layout = layout)



@app.callback(dash.dependencies.Output("lineplot2", "figure"),
    [dash.dependencies.Input("selected_states", "value"),
     dash.dependencies.Input("selected_measure2", "value")])

def update_fig2(selected_states, selected_measure2):
    data = []
    NY = []
    CA = []


    if selected_measure2 == "confirmed":
        df = us_confirmedR
    elif selected_measure2 == "death":
        df = us_deathR

    if "New York" in selected_states:
        NY = [go.Scatter(x = df.Date,
                             y = df['New York'],
                             name = 'New York',
                             mode = 'lines+text',
                             line = dict(color = 'rgba(53,92,125, 0.9)', width = 3, shape = 'spline'),
                             text = ["New York" if i == 45 else "" for i in range(df.shape[0])],
                             textposition = "top center",
                             textfont = dict(color = "rgba(53,92,125, 1)")
                            ),
              go.Scatter(x = df.Date,
                          y = [df['New York'][i] if pd.to_datetime(lockdown2.Date[lockdown2['State'] == 'New York'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          name = 'New York (lockdown)',
                          mode = 'markers',
                          marker = dict(color=[f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)'],
                       size=10),
                          #marker = dict(color = 'rgba(53,92,125, 1)', size = 10),
                          #text = ["Partial" if pd.to_datetime(lockdown2.Date[lockdown2['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else "" for i in range(df.shape[0])],
                          #textposition="top right",
                          #textfont = dict(color = "rgba(53,92,125, 1)")
                            )]
        selected_states.remove('New York')

    if "California" in selected_states:
        CA = [go.Scatter(x = df.Date,
                             y = df['California'],
                             name = 'California',
                             mode = 'lines+text',
                             line = dict(color = 'rgba(245, 133, 29, 0.9)', width = 3, shape = 'spline'),
                             text = ["California" if i == 38 else "" for i in range(df.shape[0])],
                             textposition = "top center",
                             textfont = dict(color = "rgba(245, 133, 29, 1)")
                            ),
              go.Scatter(x = df.Date,
                          y = [df['California'][i] if pd.to_datetime(lockdown2.Date[lockdown2['State'] == 'California'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          name = 'California',
                          mode = 'markers',
                          marker = dict(color = 'rgba(245, 133, 29, 1)', size = 10),
                          #text = ["Partial" if pd.to_datetime(lockdown2.Date[lockdown2['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else "" for i in range(df.shape[0])],
                          #textposition="top right",
                          #textfont = dict(color = "rgba(53,92,125, 1)")
                            )]
        selected_states.remove('California')

    others1 = [go.Scatter(x = df.Date, 
                        y = df[selected_states[i]],
                        name = selected_states[i],
                        mode = 'lines',
                        line = dict(color= f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)', 
                            width = 0.8, shape = 'spline')) for i in range(len(selected_states))]
    others2 = [go.Scatter(x = df.Date,
                          y = [df[selected_states[i]][j] if pd.to_datetime(lockdown2.Date[lockdown2['State'] == selected_states[i]].values) == pd.Timestamp(df.Date.iloc[j]) else np.nan for j in range(df.shape[0])],
                          name = selected_states[i] + ' (' + str(lockdown2.Type[lockdown2['State'] == selected_states[i]].values[0]) + ')',
                          mode = 'markers',
                          marker = dict(color = f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)', size = 5),
                          textposition="top right"
                            ) for i in range(len(selected_states))]

    data = data  + NY + CA + others1 + others2
    
    if selected_measure2 == "confirmed":
        layout = {"title": "Confirmed Case Growth Rate ", "height": 450,  "plot_bgcolor": '#f5f7fa','hovermode': 'closest'}
    elif selected_measure2 == "death":
        layout = {"title": "Death Case Growth Rate", "height": 450, "plot_bgcolor": '#f5f7fa','hovermode': 'closest'}

    return dict(data = data,
                layout = layout)

####################################################################################
#######################   Page 1 - Plot2.   Map Lockdown      ###################
####################################################################################
@app.callback(Output('map_lockdown', 'figure'),
            [Input('lockdown_slider', 'value')])

def update_figure(time_lockdown):

    lockdown_new = df_lockdown[df_lockdown['date'] == lockdown_date[time_lockdown]]

    if time_lockdown <= 19:
        fig = go.Figure(data=go.Choropleth(
                locations=lockdown_new['code'],
                z=lockdown_new['type'],
                autocolorscale = False,
                colorscale= color1,            
                locationmode = 'USA-states',
                showscale = False,
                
                text= lockdown_new['text'],  # hover text
                colorbar={'dtick':0.5,
                        'tickmode':'array',
                        'ticktext':['No lockdown order','Partial lockdown','Statewide lockdown'],
                        'tickvals':[0,0.5,1],
                        'tickangle': 90
                        }               
            ))
    else:
        fig = go.Figure(data=go.Choropleth(
                locations=lockdown_new['code'],
                z=lockdown_new['type'],
                autocolorscale = False,
                colorscale= color2,            
                locationmode = 'USA-states',
                text= lockdown_new['text'],  # hover text
                #colorbar_title = "Percent",
                showscale = False,
                
                colorbar={'dtick':0.25,
                        'tickmode':'array',
                        'ticktext':['Partial reopen','Essential business reopen','Statewide lockdown'],
                        'tickvals':[0.55,0.75,1],
                        'tickangle': 90
                        }               
            ))
       
    fig.update_layout(
    title_text = 'Lockdown Timeline by States',
    geo_scope='usa',
    font=dict(size=13),
    width = 510, #height = 500,
    margin=dict(l=0, r=0, t=80, b=0, pad = 0),
    )

    return fig

##### world
@app.callback(Output('world_lockdown_map', 'figure'),
            [Input('world_lockdown_slider', 'value')])

def update_figure(world_time):

    lockdown_new = df_world[df_world['date'] == world_date[world_time]]

    fig = px.choropleth(lockdown_new, locations="iso_alpha",
                    color="type",
                    hover_name="region", # column to add to hover information
                    color_continuous_scale=color_lock
                    #text= lockdown_new['text']
                    )
    fig.update_geos(lataxis_showgrid=False, lonaxis_showgrid=False, 
                    projection_type="natural earth",showcountries=True)             
    fig.update_layout(
    title_text = 'Worldwide Lockdown Timeline',
    margin=dict(l=0, r=0, t=80, b=0, pad = 0),
    coloraxis_showscale = False
    )

    return fig

####################################################################################
#######################   Page 2 - Plot1.   Mobility      ##########################
####################################################################################

# df_google = pd.read_csv('https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/US_Corona.csv')
# df_apple = pd.read_csv('apple_mobility.csv')
# # category dropdown 
# # state and county dropdown
# state = df_google['State'].unique()
# Dict = {}
# for s in state:
#     df_1 = df_google[df_google['State'] == s]
#     df_2 = df_1[['State', 'County']]
#     Dict[s] = df_2['County'].unique()

# opt_state = options=[{'label': k, 'value': k} for k in Dict.keys()]
# # date slide bar
# df_google['Date'] = pd.to_datetime(df_google.Date)
# df_apple['Date'] = pd.to_datetime(df_apple.Date)
# dates = ['2020-02-29', '2020-03-07', '2020-03-14', '2020-03-21',
#          '2020-03-28', '2020-04-04', '2020-04-11']

# Step 3. Create a plotly figure
##############################################################################
# ### Google Mobility
# fig = make_subplots(
#     rows=2, cols=3,
#     subplot_titles=("Retail", "Grocery", "Parks", 
#                     "Transit", "Work", "Residential"))

# df0 = df_google[(df_google['State'] == "The Whole Country")]

# fig.add_trace(go.Scatter(x = df0.Date, y = df0.Retail,
#                     name = 'Retail',
#                     line = dict(width = 2,
#                                 color = 'rgb(229, 151, 50)')),
#                     row=1, col=1)

# fig.add_trace(go.Scatter(x = df0.Date, y = df0.Grocery,
#                     name = 'Grocery',
#                     line = dict(width = 2,
#                                 color = 'rgb(51, 218, 230)')),
#                     row=1, col=2)

# fig.add_trace(go.Scatter(x = df0.Date, y = df0.Parks,
#                     name = 'Parks',
#                     line = dict(width = 2,
#                                 color = 'rgb(61, 202, 169)')),
#                     row=1, col=3)

# fig.add_trace(go.Scatter(x = df0.Date, y = df0.Transit,
#                     name = 'Transit',
#                     line = dict(width = 2,
#                                 color = 'rgb(148, 147, 159)')),
#                     row=2, col=1)

# fig.add_trace(go.Scatter(x = df0.Date, y = df0.Work,
#                     name = 'Work',
#                     line = dict(width = 2,
#                                 color = 'rgb(143, 132, 242)')),
#                     row=2, col=2)

# fig.add_trace(go.Scatter(x = df0.Date, y = df0.Residential,
#                     name = 'Residential',
#                     line = dict(width = 2,
#                                 color = 'rgb(242, 132, 227)')),
#                     row=2, col=3)

# fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))

# fig.update_layout(height=500, width=700, 
#                     title = 'Time Series Plot for Mobility in' + str(df0['County'][0]),
#                     hovermode = 'closest', 
#                     shapes = [{'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':'2020-03-07', 'x1':'2020-04-04', 
#                                'xref':'x1','yref':'y1',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                               {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':'2020-03-07', 'x1':'2020-04-04',
#                                'xref':'x2','yref':'y2',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                               {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':'2020-03-07', 'x1':'2020-04-04',
#                                        'xref':'x3','yref':'y3',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':'2020-03-07', 'x1':'2020-04-04',
#                                        'xref':'x4','yref':'y4',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':'2020-03-07', 'x1':'2020-04-04',
#                                        'xref':'x5','yref':'y5',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':'2020-03-07', 'x1':'2020-04-04',
#                                        'xref':'x6','yref':'y6',
#                                'line': {'color': 'black', 'width': 0.5}
#                                }
#                       ])

# ##############################################################################
# ### Apple Mobility
# # Define cities
# city = ['New York City', 'Rome', 'London', 'Berlin', 'Toronto', 'Tokyo']
# fig_app = make_subplots(
#     rows=2, cols=3,
#     subplot_titles=('New York City', 'Rome', 'London', 'Berlin', 'Toronto', 'Tokyo'))

# df_US = df_apple[(df_apple['Region'] == city[0])]
# ####### NYC
# traceapp1 = go.Scatter(x = df_US.Date, y = df_US.driving,
#                     name = 'Driving',
#                     mode='lines',
#                     line = dict(width = 1,
#                                 color = 'rgb(131, 90, 241)'),
#                     stackgroup='one')
                                

# traceapp2 = go.Scatter(x = df_US.Date, y = df_US.transit,
#                     name = 'Transit',
#                     mode='lines',
#                     line = dict(width = 1,
#                                 color = 'rgb(111, 231, 219)'),
#                     stackgroup='one')

# traceapp3 = go.Scatter(x = df_US.Date, y = df_US.walking,
#                     name = 'Walking',
#                     mode='lines',
#                     line=dict(width = 1, 
#                               color='rgb(102, 255, 102)'),
#                     stackgroup='one')

# fig_app.add_trace(traceapp3,
#               row=1, col=1)
# fig_app.add_trace(traceapp2,
#               row=1, col=1)
# fig_app.add_trace(traceapp1,
#               row=1, col=1)

# for c in range(1, len(city)): 
# #    print(c, city[c])
#     df_apple_city = df_apple[(df_apple['Region'] == city[c])]
    
#     traceapp1 = go.Scatter(x = df_apple_city.Date, y = df_apple_city.driving,
#                     name = 'Driving',
#                     mode='lines',
#                     line = dict(width = 1,
#                                 color = 'rgb(131, 90, 241)'),
#                     stackgroup='one', showlegend= False)
                                

#     traceapp2 = go.Scatter(x = df_apple_city.Date, y = df_apple_city.transit,
#                         name = 'Transit',
#                         mode='lines',
#                         line = dict(width = 1,
#                                     color = 'rgb(111, 231, 219)'),
#                         stackgroup='one', showlegend= False)
    
#     traceapp3 = go.Scatter(x = df_apple_city.Date, y = df_apple_city.walking,
#                         name = 'Walking',
#                         mode='lines',
#                         line=dict(width = 1, 
#                                   color='rgb(102, 255, 102)'),
#                         stackgroup='one', showlegend= False)
#     if(c < 3): 
#         fig_app.add_trace(traceapp3,
#               row=1, col=c+1)
#         fig_app.add_trace(traceapp2,
#                       row=1, col=c+1)
#         fig_app.add_trace(traceapp1,
#                       row=1, col=c+1)
    
#     else: 
#         fig_app.add_trace(traceapp3,
#               row=2, col=c-2)
#         fig_app.add_trace(traceapp2,
#                       row=2, col=c-2)
#         fig_app.add_trace(traceapp1,
#                       row=2, col=c-2)
        
# fig_app.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))

# fig_app.update_layout(height=500, width=700, 
#                     title = 'Time Series Plot for Mobility',
#                     hovermode = 'x unified')
             
# ## Step 5. Add callback functions
# @app.callback(
#     Output('opt_c', 'options'),
#     [Input('opt_s', 'value')])
# def set_state_options(selected_state):
#     return [{'label': i, 'value': i} for i in Dict[selected_state]]

# @app.callback(
#     Output('opt_c', 'value'),
#     [Input('opt_c', 'options')])
# def set_county_value(available_options):
#     return available_options[0]['value']

# @app.callback(Output('google_fig', 'figure'),
#               [Input('slider', 'value'), 
#                Input('opt_s', 'value'), Input('opt_c', 'value')])

# def update_figure(input2, selected_state, selected_county):
#     df_3 = df_google[(df_google['State'] == selected_state) & (df_google['County'] == selected_county)]
#     df_3 = df_3.sort_values(['Date']).reset_index(drop=True)
#     df_4 = df_3[(df_3['Date'] >= dates[input2[0]]) & (df_3['Date'] < dates[input2[1]])]
#     df_4 = df_4.sort_values(['Date']).reset_index(drop=True)
    
# ###############################################################################
# #### Google Mobility
#     fig = make_subplots(
#     rows=2, cols=3,
#     subplot_titles=("Retail", "Grocery", "Parks", 
#                     "Transit", "Work", "Residential"))
    
#     fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Retail,
#                         name = 'Retail',
#                         fill = 'tozeroy',
#                         line = dict(width = 2,
#                                     color = 'rgb(229, 151, 50)')),
#                         row=1, col=1)
    
#     fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Grocery,
#                         name = 'Grocery',
#                         fill = 'tozeroy',
#                         line = dict(width = 2,
#                                     color = 'rgb(51, 218, 230)')),
#                         row=1, col=2)
    
#     fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Parks,
#                         name = 'Parks',
#                         fill = 'tozeroy',
#                         line = dict(width = 2,
#                                     color = 'rgb(61, 202, 169)')),
#                         row=1, col=3)
    
#     fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Transit,
#                         name = 'Transit',
#                         fill = 'tozeroy',
#                         line = dict(width = 2,
#                                     color = 'rgb(148, 147, 159)')),
#                         row=2, col=1)
    
#     fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Work,
#                         name = 'Work',
#                         fill = 'tozeroy',
#                         line = dict(width = 2,
#                                     color = 'rgb(143, 132, 242)')),
#                         row=2, col=2)
    
#     fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Residential,
#                         name = 'Residential',
#                         fill = 'tozeroy',
#                         line = dict(width = 2,
#                                     color = 'rgb(242, 132, 227)')),
#                         row=2, col=3)
    
#     fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))
    
#     if (df_3['State'][0] == "The Whole Country"):
#         fig.update_layout(height=500, width=700, 
#                     title = 'Time Series Plot for Mobility in ' + str(df_4['County'][0]),
#                     hovermode = 'closest')
        
#         fig['layout'].update(shapes = [{'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x1', 'yref':'y1',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x2', 'yref':'y2',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x3','yref':'y3',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x4','yref':'y4',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x5','yref':'y5',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x6','yref':'y6',
#                                'line': {'color': 'black', 'width': 0.5}
#                                }
#                               ])
                
#     else: 
#         fig.update_layout(height=500, width=700, 
#                         title = 'Time Series Plot for Mobility in ' + str(df_4['County'][0]) + ', ' + str(df_3['State'][0]),
#                         hovermode = 'closest')
        
#         fig['layout'].update(shapes = [{'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x1','yref':'y1',
#                                'line': {'color': 'black', 'width': 0.5}
#                                }, 
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x2','yref':'y2',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x3','yref':'y3',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x4','yref':'y4',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x5','yref':'y5',
#                                'line': {'color': 'black', 'width': 0.5}
#                                },
#                                {'type': 'line', 'y0':0, 'y1': 0, 
#                                        'x0':min(df_4.Date), 'x1':max(df_4.Date),
#                                        'xref':'x6','yref':'y6',
#                                'line': {'color': 'black', 'width': 0.5}
#                                }                          
#                               ])
    
    
#     return fig

# ##############################################################################
# ### Apple Mobility
# @app.callback(Output('all_fig', 'figure'), 
#               [Input('slider', 'value')])

# def update_fig(input2):
# #    df_apple_US = df_apple[(df_apple['Region'] == "Tokyo")]
#     fig_app = make_subplots(
#     rows=2, cols=3,
#     subplot_titles=('New York City', 'Rome', 'London', 'Berlin', 'Toronto', 'Tokyo'))
    
#     df_US = df_apple[(df_apple['Region'] == city[0])]
#     df_apple_US = df_US[(df_US['Date'] >= dates[input2[0]]) & (df_US['Date'] < dates[input2[1]])]
    
#     traceapp1 = go.Scatter(x = df_apple_US.Date, y = df_apple_US.driving,
#                         name = 'Driving',
#                         mode='lines',
#                         line = dict(width = 1,
#                                     color = 'rgb(131, 90, 241)'),
#                         stackgroup='one')
                                    
    
#     traceapp2 = go.Scatter(x = df_apple_US.Date, y = df_apple_US.transit,
#                         name = 'Transit',
#                         mode='lines',
#                         line = dict(width = 1,
#                                     color = 'rgb(111, 231, 219)'),
#                         stackgroup='one')
    
#     traceapp3 = go.Scatter(x = df_apple_US.Date, y = df_apple_US.walking,
#                         name = 'Walking',
#                         mode='lines',
#                         line=dict(width = 1, 
#                                   color='rgb(102, 255, 102)'),
#                         stackgroup='one')
    
#     fig_app.add_trace(traceapp3,
#               row=1, col=1)
#     fig_app.add_trace(traceapp2,
#                   row=1, col=1)
#     fig_app.add_trace(traceapp1,
#                   row=1, col=1)

#     for c in range(1, len(city)): 
#     #    print(c, city[c])
#         df_apple_city = df_apple[(df_apple['Region'] == city[c])]
#         df_apple_new = df_apple_city[(df_apple_city['Date'] >= dates[input2[0]]) & (df_apple_city['Date'] < dates[input2[1]])]
        
#         traceapp1 = go.Scatter(x = df_apple_new.Date, y = df_apple_new.driving,
#                         name = 'Driving',
#                         mode='lines',
#                         line = dict(width = 1,
#                                     color = 'rgb(131, 90, 241)'),
#                         stackgroup='one', showlegend= False)
                                    
    
#         traceapp2 = go.Scatter(x = df_apple_new.Date, y = df_apple_new.transit,
#                             name = 'Transit',
#                             mode='lines',
#                             line = dict(width = 1,
#                                         color = 'rgb(111, 231, 219)'),
#                             stackgroup='one', showlegend= False)
        
#         traceapp3 = go.Scatter(x = df_apple_new.Date, y = df_apple_new.walking,
#                             name = 'Walking',
#                             mode='lines',
#                             line=dict(width = 1, 
#                                       color='rgb(102, 255, 102)'),
#                             stackgroup='one', showlegend= False)
#         if(c < 3): 
#             fig_app.add_trace(traceapp3,
#                   row=1, col=c+1)
#             fig_app.add_trace(traceapp2,
#                           row=1, col=c+1)
#             fig_app.add_trace(traceapp1,
#                           row=1, col=c+1)
        
#         else: 
#             fig_app.add_trace(traceapp3,
#                   row=2, col=c-2)
#             fig_app.add_trace(traceapp2,
#                           row=2, col=c-2)
#             fig_app.add_trace(traceapp1,
#                           row=2, col=c-2)
            
#     fig_app.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))
    
#     fig_app.update_layout(height=500, width=700, 
#                         title = 'Time Series Plot for Mobility',
#                         hovermode = 'x unified')

#     return fig_app



####################################################################################
#######################   Page 3 - Plot1.   Survey      ###########################
####################################################################################
################ Survey Plot
### buttons

@app.callback(
    [Output('selected_pollsters', 'options'),
     Output('selected_pollsters', 'value')],
    [Input('selected_question', 'value'),
     Input('radio_display1', 'value')])

def set_survey_options(which_question, which_radio):
    #print('which_question', which_question)

    if which_question == 'Q_concern_econ':
      if which_radio == 'by_party':
          return [[{'label': 'All', 'value': 'all'}], ['all']]
      if which_radio == "All":
          return [[{'label': 'All', 'value': 'all'}], ['all']]
      elif which_radio == "by_pollster":
          return [[{'label': x, 'value': x} for x in list(concern_adj_econ.pollster.unique())], ['Morning Consult']]
      elif which_radio == "by_sponsor":
          return [[{'label': x, 'value': x} for x in list(concern_econ.sponsor.unique())], ['New York Times', 'CNBC', 'Fortune']]
      elif which_radio == 'by_population':
          return [[{'label': x, 'value': x} for x in list(concern_adj_econ.population.unique())], ['All Adults', 'Registered Voters']]
    
    elif which_question == 'Q_concern_infec':
      if which_radio == 'by_party':
          return [[{'label': 'All', 'value': 'all'}], ['all']]
      if which_radio == "All":
          return [[{'label': 'All', 'value': 'all'}], ['all']]
      elif which_radio == "by_pollster":
          return [[{'label': x, 'value': x} for x in list(concern_adj_infec.pollster.unique())], ['YouGov', 'SurveyUSA', 'Optimus','Quinnipiac University','Harris Insights & Analytics']]
      elif which_radio == "by_sponsor":
          return [[{'label': x, 'value': x} for x in list(concern_infec.sponsor.unique())], ['ABC News', 'CBS News', 'CNBC', 'Economist', 'Fortune', 'USA Today']]
      elif which_radio == 'by_population':
          return [[{'label': x, 'value': x} for x in list(concern_adj_infec.population.unique())], ['All Adults', 'Registered Voters']]
    
    elif which_question == 'Q_approval':
      if which_radio == "All":
          return [[{'label': 'All', 'value': 'all'}], ['all']]
      elif which_radio == "by_pollster":
          return [[{'label': x, 'value': x} for x in list(approval_adj.pollster.unique())], ['YouGov','Morning Consult','SurveyMonkey']]
      elif which_radio == "by_sponsor":
          return [[{'label': x, 'value': x} for x in list(approval.sponsor.unique())], ['ABC News', 'CBS News', 'CNBC', 'CNN', 'USA Today', 'Economist','Politico']]
      elif which_radio == 'by_population':
          return [[{'label': x, 'value': x} for x in list(approval_adj.population.unique())], ['All Adults', 'Registered Voters']]
      elif which_radio == 'by_party':
          return [[{'label': x, 'value': x} for x in ['Democrats', 'Republicans', 'Independents']], ['Democrats', 'Republicans', 'Independents']]
    
    
    



@app.callback(
    Output('radio_display1', 'value'),
    [Input('radio_display1', 'options')])
def set_survey_value(available_options):
    return available_options[0]['value']


@app.callback(Output("survey_plot1", "figure"),
            [Input("selected_question", "value"),
             Input("selected_pollsters", "value"),
             Input("radio_display1", "value")])

def update_fig_s1(selected_question, selected_pollsters, radio_display1):
    data = []
    topline = []
    topline1 = []
    All = []
    others1 = []
    others2 = []
    others3 = []
    others4 = []
    events = []

    if selected_question == 'Q_approval':

      df_topline = approval_topline
      df_adj = approval_adj
      df_original = approval

      topline1 = [go.Scatter(x = df_topline[df_topline['party'] == 'All'].modeldate,
                             y = df_topline[df_topline['party'] == 'All'].approve_estimate,
                             name = 'approve',
                             mode = 'lines',
                             line = dict(color = "Green")
                            ),
                 go.Scatter(x = df_topline[df_topline['party'] == 'All'].modeldate,
                             y = df_topline[df_topline['party'] == 'All'].disapprove_estimate,
                             name = 'disapprove',
                             mode = 'lines',
                             line = dict(color = "Red")
                            ),
                 go.Scatter(x=['2020-02-23','2020-02-23','2020-03-03','2020-03-03', '2020-03-13','2020-03-13','2020-03-27', '2020-03-27'],
                              y=[89, 84,105, 100, 94, 90, 100, 94],
                              text=['1st case of suspected', 'local transmission in the US',
                                  "Trump donated salary",
                                  "to fight the virus",
                                  'Trump declares', 'national emergency',
                                  "Trump signs",
                                  "Stimulus bill"],
                              mode="text",
                              showlegend=False
                          ),
                  go.Scatter(x = ['2020-02-26', '2020-02-26'],
                           y = [0,85],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-03', '2020-03-03'],
                           y = [0,98],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-13', '2020-03-13'],
                           y = [0,90],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-27', '2020-03-27'],
                           y = [0,85], 
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          )]

      if radio_display1 == 'All':
        All = [go.Scatter(x = df_adj.end_date,
                              y = df_adj.approve_adjusted,
                              name = "approve",
                              mode = 'markers',
                              marker = dict(size = 8,
                                            color = "green",
                                            opacity = df_adj.weight / max(df_adj.weight)
                                           )),
               go.Scatter(x = df_adj.end_date,
                              y = df_adj.disapprove_adjusted,
                              name = "disapprove",
                              mode = 'markers',
                              marker = dict(size = 8,
                                           color = "red",
                                           opacity = df_adj.weight / max(df_adj.weight)
                                           ))
                ]

      elif radio_display1 == 'by_pollster':
          others1 = [go.Scatter(x = df_adj[df_adj['pollster'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['pollster'] == selected_pollsters[i]].approve_adjusted,
                                  name = 'approve ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "green",
                                              opacity = [x+0.1 if x<0.5 else x for x in df_adj.weight / max(df_adj.weight)],
                                              symbol = symbols4[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_adj[df_adj['pollster'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['pollster'] == selected_pollsters[i]].disapprove_adjusted,
                                  name = 'disapprove ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "red",
                                              opacity = [x+0.1 if x<0.5 else x for x in df_adj.weight / max(df_adj.weight)],
                                              symbol = symbols4[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]

      elif radio_display1 == 'by_sponsor':
          others1 = [go.Scatter(x = df_original[df_original['sponsor'] == selected_pollsters[i]].end_date, 
                                y = df_original[df_original['sponsor'] == selected_pollsters[i]].approve,
                                  name = 'approve ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "green",
                                              opacity = 0.3,
                                              symbol = symbols5[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_original[df_original['sponsor'] == selected_pollsters[i]].end_date, 
                                y = df_original[df_original['sponsor'] == selected_pollsters[i]].disapprove,
                                  name = 'disapprove ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "red",
                                              opacity = 0.3,
                                              symbol = symbols5[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]

      elif radio_display1 == 'by_population':
          others1 = [go.Scatter(x = df_adj[df_adj['population'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['population'] == selected_pollsters[i]].approve_adjusted,
                                  name = 'approve ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "green",
                                              opacity = 0.3,
                                              symbol = symbols3[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_adj[df_adj['population'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['population'] == selected_pollsters[i]].disapprove_adjusted,
                                  name = 'disapprove ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "red",
                                              opacity = 0.3,
                                              symbol = symbols3[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]

      elif radio_display1 == 'by_party':
          others1 = [go.Scatter(x = df_adj[df_adj['party'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['party'] == selected_pollsters[i]].approve_adjusted,
                                  name = 'approve ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "green",
                                              opacity = 0.3,
                                              symbol = symbols6[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_adj[df_adj['party'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['party'] == selected_pollsters[i]].disapprove_adjusted,
                                  name = 'disapprove ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "red",
                                              opacity = 0.3,
                                              symbol = symbols6[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]


    else: 
      if selected_question == 'Q_concern_econ':
        df_topline = concern_topline_econ
        df_adj = concern_adj_econ
        df_original = concern_econ

        events = [go.Scatter(x=['2020-02-29','2020-02-29', '2020-03-09', '2020-03-12','2020-03-27', '2020-03-27', '2020-04-19'],
                              y=[76, 73, -3, 71, 74, 71, 71],
                              text=["1st death reported",
                                  "in the US",
                                  "First Trading Curb",
                                  'Second Trading Curb',
                                  "Trump signs",
                                  "Stimulus bill",
                                  "U.S Oil Price Hits $15"],
                              mode="text",
                              showlegend=False
                          ),
                  go.Scatter(x = ['2020-02-29', '2020-02-29'],
                           y = [0,70],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-09', '2020-03-09'],
                           y = [0,70],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-12', '2020-03-12'],
                           y = [0,70],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-27', '2020-03-27'],
                           y = [0,70],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-04-19', '2020-04-19'],
                           y = [0,70],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          )]

      elif selected_question == 'Q_concern_infec':
        df_topline = concern_topline_infect
        df_adj = concern_adj_infec
        df_original = concern_infec

        events = [go.Scatter(x=['2020-02-24','2020-02-27', '2020-03-03', '2020-03-03','2020-03-15', '2020-03-15', '2020-03-26','2020-03-26', '2020-04-05',
                                '2020-04-24', '2020-04-24'],
                              y=[45, 41, 58, 54, 49, 45, 62, 58, 52, 50, 46],
                              text=["1st death reported", "in the US",
                                  "CDC lifts restrictions", "for virus testing",
                                  'CDC warns against','large gatherings',
                                  "US leads the world", "in COVID-19 cases",
                                  "Global cases hit 1 million",
                                  'More than 1 million', 'confirmed in the US'],
                              mode="text",
                              showlegend=False
                          ),
                  go.Scatter(x = ['2020-02-29', '2020-02-29'],
                           y = [0,39],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-03', '2020-03-03'],
                           y = [0,52],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-15', '2020-03-15'],
                           y = [0,44],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-03-26', '2020-03-26'],
                           y = [0,55],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-04-02', '2020-04-02'],
                           y = [0,50],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          ),
                  go.Scatter(x = ['2020-04-27', '2020-04-27'],
                           y = [0,45],
                           mode = 'lines',
                           line = dict(color = "grey",width=1, dash="dashdot"),
                           showlegend=False
                          )]


      topline = [go.Scatter(x = df_topline.modeldate,
                               y = df_topline.very_estimate,
                               name = 'very (AVERAGE)',
                               mode = 'lines',
                               line = dict(color = "Red")
                              ),
                 go.Scatter(x = df_topline.modeldate,
                               y = df_topline.somewhat_estimate,
                               name = 'somewhat (AVERAGE)',
                               mode = 'lines',
                               line = dict(color = "Pink")
                              ),
                 go.Scatter(x = df_topline.modeldate,
                               y = df_topline.not_very_estimate,
                               name = 'not very (AVERAGE)',
                               mode = 'lines',
                               line = dict(color = "#B6D7B9")
                              ),
                 go.Scatter(x = df_topline.modeldate,
                               y = df_topline.not_at_all_estimate,
                               name = 'not at all (AVERAGE)',
                               mode = 'lines',
                               line = dict(color = "Green")
                              ), 
                  ]

      if radio_display1 == 'by_party':
          radio_display1 = 'All'


      if radio_display1 == 'All':
          All = [go.Scatter(x = df_adj.end_date,
                                y = df_adj.very_adjusted,
                                name = "very",
                                mode = 'markers',
                                marker = dict(size = df_adj.samplesize*0.005,
                                              color = "red",
                                              opacity = df_adj.weight / max(df_adj.weight)
                                             )),
                 go.Scatter(x = df_adj.end_date,
                                y = df_adj.somewhat_adjusted,
                                name = "somewhat",
                                mode = 'markers',
                                marker = dict(size = df_adj.samplesize*0.005,
                                             color = "pink",
                                             opacity = df_adj.weight / max(df_adj.weight)
                                             )),
                 go.Scatter(x = df_adj.end_date,
                                y = df_adj.not_very_adjusted,
                                name = "not_very",
                                mode = 'markers',
                                marker = dict(size = df_adj.samplesize*0.005,
                                             color = "#B6D7B9",
                                             opacity = df_adj.weight / max(df_adj.weight)
                                             )),
                 go.Scatter(x = df_adj.end_date,
                                y = df_adj.not_at_all_adjusted,
                                name = "not_at_all",
                                mode = 'markers',
                                marker = dict(size = df_adj.samplesize*0.005,
                                             color = "Green",
                                             opacity = df_adj.weight / max(df_adj.weight)
                                             ))
                  ]

      elif radio_display1 == 'by_pollster':
          # print(df_adj.pollster)
          # print(selected_pollsters)
          # print(selected_pollsters[0])
          # print(selected_pollsters[0] == 'YouGov')
          # print(df_adj[df_adj['pollster'] == selected_pollsters[0]])
          others1 = [go.Scatter(x = df_adj[df_adj['pollster'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['pollster'] == selected_pollsters[i]].very_adjusted,
                                  name = 'very ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = [x+5 if x<3 else x for x in df_adj.samplesize*0.006],
                                              color = "red",
                                              opacity = [x+0.1 if x<0.5 else x for x in df_adj.weight / max(df_adj.weight)],
                                              symbol = symbols1[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_adj[df_adj['pollster'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['pollster'] == selected_pollsters[i]].somewhat_adjusted,
                                  name = 'somewhat ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = [x+5 if x<3 else x for x in df_adj.samplesize*0.006],
                                              color = "pink",
                                              opacity = [x+0.1 if x<0.5 else x for x in df_adj.weight / max(df_adj.weight)],
                                              symbol = symbols1[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others3 = [go.Scatter(x = df_adj[df_adj['pollster'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['pollster'] == selected_pollsters[i]].not_very_adjusted,
                                  name = 'not very ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = [x+5 if x<3 else x for x in df_adj.samplesize*0.006],
                                              color = "#B6D7B9",
                                              opacity = [x+0.1 if x<0.5 else x for x in df_adj.weight / max(df_adj.weight)],
                                              symbol = symbols1[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others4 = [go.Scatter(x = df_adj[df_adj['pollster'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['pollster'] == selected_pollsters[i]].not_at_all_adjusted,
                                  name = 'not at all ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = [x+5 if x<3 else x for x in df_adj.samplesize*0.006],
                                              color = "green",
                                              opacity = [x+0.1 if x<0.5 else x for x in df_adj.weight / max(df_adj.weight)],
                                              symbol = symbols1[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]

      elif radio_display1 == 'by_sponsor':
          others1 = [go.Scatter(x = df_original[df_original['sponsor'] == selected_pollsters[i]].end_date, 
                                y = df_original[df_original['sponsor'] == selected_pollsters[i]].very,
                                  #name = 'very ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "red",
                                              opacity = 0.8
                                              #symbol = symbols2[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_original[df_original['sponsor'] == selected_pollsters[i]].end_date, 
                                y = df_original[df_original['sponsor'] == selected_pollsters[i]].somewhat,
                                  name = 'somewhat ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "pink",
                                              opacity = 0.8,
                                              symbol = symbols2[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others3 = [go.Scatter(x = df_original[df_original['sponsor'] == selected_pollsters[i]].end_date, 
                                y = df_original[df_original['sponsor'] == selected_pollsters[i]].not_very,
                                  name = 'not very ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "#B6D7B9",
                                              opacity = 0.8,
                                              symbol = symbols2[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others4 = [go.Scatter(x = df_original[df_original['sponsor'] == selected_pollsters[i]].end_date, 
                                y = df_original[df_original['sponsor'] == selected_pollsters[i]].not_at_all,
                                  name = 'not at all ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 8,
                                              color = "green",
                                              opacity = 0.8,
                                              symbol = symbols2[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]

      elif radio_display1 == 'by_population':
          others1 = [go.Scatter(x = df_adj[df_adj['population'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['population'] == selected_pollsters[i]].very_adjusted,
                                  name = 'very ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "red",
                                              opacity = 0.8,
                                              symbol = symbols3[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others2 = [go.Scatter(x = df_adj[df_adj['population'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['population'] == selected_pollsters[i]].somewhat_adjusted,
                                  name = 'somewhat ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "pink",
                                              opacity = 0.8,
                                              symbol = symbols3[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others3 = [go.Scatter(x = df_adj[df_adj['population'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['population'] == selected_pollsters[i]].not_very_adjusted,
                                  name = 'not very ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "#B6D7B9",
                                              opacity = 0.8,
                                              symbol = symbols3[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]
          others4 = [go.Scatter(x = df_adj[df_adj['population'] == selected_pollsters[i]].end_date, 
                                y = df_adj[df_adj['population'] == selected_pollsters[i]].not_at_all_adjusted,
                                  name = 'not at all ' + '(' + selected_pollsters[i] + ')',
                                  mode = 'markers',
                                  marker = dict(size = 6,
                                              color = "green",
                                              opacity = 0.8,
                                              symbol = symbols3[selected_pollsters[i]]
                                             )
                                  ) for i in range(len(selected_pollsters))]

    data = topline + topline1 + All + others1 + others2 + others3 + others4 + events

    if selected_question == "Q_concern_infec":
        layout = dict(title = {
                    'text': "<b>How concerned are Americans about infection?</b>",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                   plot_bgcolor='rgb(247,245,245)',
                   height = 500,
                   hovermode='closest',
                   xaxis_showgrid=False, yaxis_showgrid=False,
                   )
    elif selected_question == "Q_concern_econ":
        layout = dict(title = {
                    'text': "<b>How concerned are Americans about economy?</b>",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                   plot_bgcolor='rgb(247,245,245)',
                   height = 500,
                   hovermode='closest',
                   xaxis_showgrid=False, yaxis_showgrid=False,
                   )
    elif selected_question == "Q_approval":
        layout = dict(title = {
                    'text': "<b>Do Americans approve of Trump’s response to the coronavirus crisis?</b>",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                   plot_bgcolor='rgb(247,245,245)',
                   height = 500,
                   hovermode='closest',
                   xaxis_showgrid=False, yaxis_showgrid=False,
                   )

    return dict(data = data,
                layout = layout)



##################################################################################
#######################   Page 3 - Plot2.   Tweeter      ###########################
####################################################################################
@app.callback(
    dash.dependencies.Output('image', 'children'),
    [Input('year-slider', 'value')])


def update_output(value):
    src1 = "https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/twitterViz/images/" + daterange[value] + '.png'
    img = html.Img(src=src1,  style={'width':'100%', 'display': 'inline-block'})
    return img

@app.callback(
    dash.dependencies.Output('hot-table', 'figure'),
    [Input('year-slider', 'value')])

def table_output(value):
    filename = "https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/twitterViz/newcsv/" + daterange[value] + '.csv'
    df = pd.read_csv(filename)
    #temp = temp.iloc[1:-1,:].reset_index(drop = True)
    #df['rank'] = df.index + 1

    if daterange[value] != "2020-03-22":
        #red : New , yello: 上涨， green: 下降
        font_color=['black']
        temp = []
        df['change'] = pd.to_numeric(df['change'], errors='coerce')
        for i in df['change']:
            if np.isnan(i):
                temp.append('rgb(248, 112, 96)')
            else:
                if i >= 0:
                    temp.append('rgb(246, 189, 96)')
                else:
                    temp.append('rgb(132, 236, 157)')
        font_color.append(temp)
        data=[go.Table(
            columnwidth = [80,40,40],
            header=dict(values=['Keywords', 'Hottness'],
                        line_color= 'gainsboro',
                        fill_color='rgb(16, 37, 66)',
                        font=dict(color='rgb(238, 240, 242)'),
                        align='left'),
            cells=dict(values=[df['word'], df['count']],
                    line_color= 'gainsboro',
                    fill=dict(color=['rgb(247, 237, 226)', 'white']),
                    font_color=font_color,
                    align= ['left']*3))]
    else:
        data=[go.Table(
            columnwidth = [80,40,40],
            header=dict(values=list(df.columns),
                        line_color= 'gainsboro',
                        fill_color='rgb(16, 37, 66)',
                        font=dict(color='rgb(238, 240, 242)'),
                        align='left'),
            cells=dict(values=[df['word'], df['count']],
                    line_color= 'gainsboro',
                    fill=dict(color=['rgb(247, 237, 226)', 'white']),
                    align='left'))]

    return dict(data = data)


####################################################################################
#######################   Page 4 - Plot1.   Unemployment      ######################
####################################################################################

df_unemployment_rate_0 = df_unemployment_rate[df_unemployment_rate['code']=='AL']
df_claims_0 = df_claims[df_claims['code']=='AL']

layout1 = go.Layout(title = 'Time Series for Unemployment Rate',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       linewidth=0.5,
                       mirror=True),
                   plot_bgcolor = 'white',
                   font=dict(size=10),
                    height = 200, width = 500, margin=dict(l=80,r=0,b=0,t=30,pad=0))

layout2 = go.Layout(title = 'Time Series for the Emerging Unemployment Claims',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       linewidth=0.5,
                       mirror=True),
                   plot_bgcolor = 'white',
                   font=dict(size=9),
                   height = 200, width = 500, margin=dict(l=80,r=0,b=0,t=60,pad=0))

trace_1 = go.Scatter(x = df_unemployment_rate_0['Month'], y = df_unemployment_rate_0['UEP Rate'],
                    name = 'Alabama',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
# layout1 = go.Layout(title = 'Time Series for Unemployment Rate',
#                    hovermode = 'x',
#                    spikedistance =  -1,
#                    xaxis=dict(
#                        #showline=True, 
#                        #showgrid=True, 
#                        showticklabels=True,
#                        spikemode  = 'across+toaxis',
#                        #linecolor='rgb(204, 204, 204)',
#                        linewidth=0.5,
#                        mirror=True)                       
#                        )

trace_2 = go.Scatter(x = df_claims_0['date'], y = df_claims_0['claims'],
                    name = 'Alabama',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
# layout2 = go.Layout(title = 'Time Series for Emerging Unemployment Claims',
#                    hovermode = 'x',
#                    spikedistance =  -1,
#                    xaxis=dict(
#                        #showline=True, 
#                        #showgrid=True, 
#                        showticklabels=True,
#                        spikemode  = 'across+toaxis',
#                        #linecolor='rgb(204, 204, 204)',
#                        linewidth=0.5,
#                        mirror=True))

linetrace = go.Scatter(
                x=[df_claims_0['date'][357],df_claims_0['date'][357]], # , '2020-03-09', '2020-03-12','2020-03-27', '2020-03-27', '2020-04-19'],
                y=[0, -3], # -3, 71, 74, 71, 71],
                text=["1st death reported",
                    "in the US"],
                    # "First Trading Curb",
                    # 'Second Trading Curb',
                    # "Trump signs",
                    # "Stimulus bill",
                    # "U.S Oil Price Hits $15"],
                mode="text",
                showlegend=False
            )

linetrace2 = go.Scatter(x = [df_claims_0['date'][357], df_claims_0['date'][357]],
                         y = [0,140000],
                         mode = 'lines',
                         line = dict(color = "black",width=1, dash="dashdot"),
                         showlegend=False
                        )           


fig1 = go.Figure(data = [trace_1], layout = layout1)
fig2 = go.Figure(data = [trace_2, linetrace, linetrace2], layout = layout2)


@app.callback([Output('plot1', 'figure'),Output('plot2', 'figure'),Output('map', 'figure')],
             [Input('opt', 'value'),Input('RangeSlider','value'),])


def update_figure(un_state,un_time):
    
    # filtering the data
    df_unemployment_rate_2 = df_unemployment_rate[(df_unemployment_rate.Month >= un_dates[un_time[0]]) & (df_unemployment_rate.Month <= un_dates[un_time[1]])]
    df_new_un = df_map[df_map['Month']== date_map[un_time[0]]]

    traces_1 = []
    traces_2 = []
    highesty = 0

    for val in un_state:
        df_unemployment_rate_1 = df_unemployment_rate_2[(df_unemployment_rate_2.State == val)]
        df_claims_1 = df_claims[df_claims['State'] == val]

        traces_1.append(go.Scatter(
            x = df_unemployment_rate_1['Month'],
            y = df_unemployment_rate_1['UEP Rate'],
            text= val,
            name = val,
            mode = 'lines+markers',
            marker = {'symbol':'triangle-right','size':5},
            line = {'width':1},
            showlegend=True
            
        ))

        traces_2.append(go.Scatter(
            x = df_claims_1['date'],
            y = df_claims_1['claims'],
            text= val,
            name = val,
            mode = 'lines+markers',
            marker = {'symbol':'triangle-right','size':5}, #star-dot
            line = {'width':1},
            showlegend=False
        ))

        if df_claims_1['claims'].max() > highesty:
            highesty = df_claims_1['claims'].max()
    
    linetrace = go.Scatter(
                x=[df_claims_0['date'][357], df_claims_0['date'][459],  df_claims_0['date'][561]],
                y=[highesty+4000, -10000, highesty+4000],
                text=["1st death reported",
                    "Week of Trading Curbs",
                    "Stimulus bill signed"
                    ],
                    # "Trump signs",
                    # "Stimulus bill",
                    # "U.S Oil Price Hits $15"],
                mode="text",
                showlegend=False
            )
    linetrace2 = go.Scatter(x = [df_claims_0['date'][357], df_claims_0['date'][357]],
                            y = [0,highesty],
                            mode = 'lines',
                            line = dict(color = "black",width=1, dash="dashdot"),
                            showlegend=False
                            )  
    linetrace3 = go.Scatter(x = [df_claims_0['date'][459], df_claims_0['date'][459]],
                            y = [0,highesty],
                            mode = 'lines',
                            line = dict(color = "black",width=1, dash="dashdot"),
                            showlegend=False
                            )   
    linetrace4 = go.Scatter(x = [df_claims_0['date'][561], df_claims_0['date'][561]],
                            y = [0,highesty],
                            mode = 'lines',
                            line = dict(color = "black",width=1, dash="dashdot"),
                            showlegend=False
                            )   

    traces_2.append(linetrace)
    traces_2.append(linetrace2)   
    traces_2.append(linetrace3)  
    traces_2.append(linetrace4) 

    fig1 = go.Figure(data = traces_1, layout = layout1)

    fig2 = go.Figure(data = traces_2, layout = layout2)

    fig3 = go.Figure(data=go.Choropleth(
            locations=df_new_un['code'],
            z=df_new_un['UEP Rate'].astype(float),
            colorscale='Reds',
            locationmode = 'USA-states',
            text=df_new_un['text'], # hover text
            colorbar_title = "Percent"
            
        ))

    fig3.update_layout(
            title_text = 'Unemployment Rate by State',
            geo_scope='usa',
            font=dict(size=10),
            width = 500,
            margin=dict(l=0,r=0,b=0,t=0,pad=0)) # limite map scope to USA)
    
    return fig1, fig2, fig3



####################################################################################
#######################   Page 5 - Plot1.   Legislation      ######################
####################################################################################

##### Legal Table 
@app.callback(Output("legal_table", "figure"),
    [Input("search_text", "value"),
     Input("selected_state", "value"),
     Input("selected_status", "value")])

def update_table(search_text, selected_state, selected_status):
    df = legal

    if search_text != None:
        keywords = re.split(',', search_text)
        keywords = [x.lower() for x in keywords]
        keywords = [re.sub('[^A-Za-z0-9]+', ' ', str(x)) for x in keywords]
        keywords = [re.sub(' ', '', str(x)) for x in keywords]

        for keyword in keywords:
            df = df[df['search_area'].str.contains(keyword)==True]

    if selected_state != None:
        df = df[(df['Region'] == selected_state)] 
    if selected_status != None:
        df = df[(df['Status'] == selected_status)]

    data = [go.Table(
                columnwidth = [400,200,200,200,150],
                header=dict(values=['<b>COVID-19 Legislation</b>', '<b>State</b>',
                                    '<b>Status</b>', '<b>Last Timeline Action</b>', '<b>Last Action Date</b>'],
                            fill_color='#91ADC2',
                            #fill_color='#87BBA2',
                            #fill_color='#4D5382',
                            font_color='white',
                            align='left'),
                cells=dict(values=[df['title'], df['Region'],
                                   df['Status'], df['Last Timeline Action'], df['Last Timeline Action Date']
                                   ],
                           fill_color='#f5f7fa',
                           align=['left','left','left','left','center']))
            ]
    layout = dict(height = 580,
                  margin=dict(t=25, b=20, l=0, r=10, pad=0))

    return dict(data = data, layout = layout)


if __name__ == '__main__':
    app.run_server(debug=False)