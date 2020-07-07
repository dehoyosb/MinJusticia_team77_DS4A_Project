import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import sys
from datetime import datetime as dt

#sys.path.insert(1, '/tabContents')


#Create the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Import the tabs content for the individual file

from tabContents.tab1 import tab1_content
from tabContents.tab2 import tab2_content
from tabContents.tab3 import tab3_content
from tabContents.tab4 import tab4_content
from tabContents.tab5 import tab5_content



#Create Layout
app.layout = html.Div([
    # create the navbar, the first bar
    dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url("minjusticia_logo.jpg"), height="40px")),
                    dbc.Col(dbc.NavbarBrand("Recividism in Colombia", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="http://www.minjusticia.gov.co",
        ),
        dbc.NavbarToggler(id="navbar-toggler")#,
    ],
    color='#345bc6',
    dark=True,
),

dbc.Row(
    [
    ###  create sidebar 
    #dbc.Col([html.P('  '),]),
	
	dbc.Col(
    [
        html.H4("Filters"),
        html.Hr(),
        html.P(
            "Prision income date range", className="lead"
        ),
		dcc.DatePickerRange(
							id='my-date-picker-range',
							min_date_allowed=dt(2010, 1, 1),
							max_date_allowed=dt(2021, 1, 1),
							initial_visible_month=dt(2020, 7, 1)#,
							#end_date=dt(2020, 7, 15).date()
		),
		html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Reclusion Department", className="lead"
        ),
		dcc.Dropdown(
        id='reclusion_dep',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
	
	html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Crime", className="lead"
        ),
		dcc.Dropdown(
        id='crime',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
	
	html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Sentence Type", className="lead"
        ),
		dcc.Dropdown(
        id='sentence_type',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
	
	html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Gender", className="lead"
        ),
	
	dcc.Checklist(
		id='gender',
		options=[
			{'label': 'Male', 'value': '2'},
			{'label': 'Female', 'value': '1'},
		],
		value=['1', '2'],
		labelStyle={'display': 'inline-block', 'align': 'center', 'padding-left' : '30px'}
),
	html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Range Age", className="lead"
        ),
	dcc.RangeSlider(
					id='range_age',
					count=1,
					min=15,
					max=100,
					step=1,
					value=[15, 100],
					marks={15:'15', 20: '20', 30:'30', 40:'40',50:'50',60:'60',70:'70',80:'80',90:'90',100:'100'},
					tooltip={'always_visible': True}

), 

html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Exceptional Conditions", className="lead"
        ),
	
	dcc.Checklist(
		id='excep_cond',
		options=[
			{'label': 'Yes', 'value': '2'},
		],
		#value=['1', '2'],
		labelStyle={'display': 'inline-block', 'align': 'center', 'padding-left' : '30px'}
), 
	
    ],
    width={"size": 'auto'#,
		   #"offset": 1
		   },
	style={'margin-left': '20px'},
	#align="center"
),
    # create the app content, simply add every tab created in the folder
dbc.Col([
    dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Overview"),
        dbc.Tab(tab2_content, label="Socio Demographic"),
        dbc.Tab(tab3_content, label="Clustering"),
        dbc.Tab(tab4_content, label="Trends"),
        dbc.Tab(tab5_content, label="Predictive"),
    ]
)])

])])


#@app.callback(
#    Output('main-figure','figure'),
#    [Input('fig-slider','value')])
#def slider_interaction(slider_val):
#    if slider_val==0:
#        fig=Map_Fig
#    else:
#        fig=Scatter_Fig
#
#    return fig 



#Initiate the server where the app will work
if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0', port=5000)