import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from datetime import datetime as dt
from utils.utils import DbEngine, Queries





#Create the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Import the tabs content for the individual file

from tabContents.tab1 import tab1_content
from tabContents.tab2 import tab2_content
from tabContents.tab3 import tab3_content
from tabContents.tab4 import tab4_content
from tabContents.tab5 import tab5_content

#import filters

from tabContents.filters import filter_reclusion_dep
from tabContents.filters import filter_prison_date_range
from tabContents.filters import filter_crime
from tabContents.filters import filter_sentence_type
from tabContents.filters import filter_gender
from tabContents.filters import filter_range_age
from tabContents.filters import filter_excep_cond
from tabContents.filters import filter_reclusion_entity


#Create Layout
app.layout = html.Div([
        html.Link(
            rel='stylesheet',
            href='/assets/css/styles.css'
        ),
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


        #dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Col([
            dbc.Row([
#                dbc.DropdownMenu(
#                    children=[
#                         dbc.DropdownMenuItem("Development Team", header=True),
#                         dbc.DropdownMenuItem("Page 2", href="#"),
#                         dbc.DropdownMenuItem("Page 3", href="#"),
#                     ],
#                    right=False,
#                    nav=True,
#                    in_navbar=True,
#                    label="Team",
#                    color= '#fff',
#                    toggle_style={"color": "white"}
 #       ),
 		dbc.Col([html.A("Development Team", href="http://localhost:5001", style={'color':'#fff'})]),

        dbc.Col([html.A("ESP", href="http://www.minjusticia.gov.co", style={'color':'#fff'})]),
        ]),],
        width={"size": 3, "order": "last", "offset": 5},)
    ],
    color='rgb(51,102,204,1)',
    dark=True,
),

dbc.Row(
    [
    ###  create sidebar 
    #dbc.Col([html.P('  '),]),
	
	dbc.Col(
    [
        #html.H4("Filters"),
        html.Hr(),
         # first group of filters
html.Div(
    [
     dbc.Card(
        [
            dbc.Button(
                        "+ Reclusion Ubication",
                        style={"background-color": "rgb(51,102,204,1)","text-align" : "left",  "border" : "0px"},
                        id=f"group-1-toggle",
            ),
            dbc.Collapse(
                dbc.CardBody([html.Div(filter_reclusion_dep),
                    html.Div(filter_reclusion_entity)]),
                id="collapse-1",
                style = {"height" : "400px"},
            ),
        ],
        style={"background-color": "#4573D0",
        	   "border" : "none", 
        	   #"color": "rgb(255,255,255,1)",
        	   "size": "100%"}
    ),


    dbc.Card(
        [
                    dbc.Button(
                        "+ Sociodemographic",
                        style={"background-color": "rgb(51,102,204,1)","text-align" : "left",  "border" : "0px"},
                        id=f"group-2-toggle",
            ),
            dbc.Collapse(
                dbc.CardBody([html.Div(filter_gender),
                    html.Div(filter_range_age),
                    html.Div(filter_excep_cond)]),
                id="collapse-2",
            ),
        ],
        style={"background-color": "#4573D0",
        	   "border" : "none", 
        	   #"color": "rgb(255,255,255,1)",
        	   "size": "100%"}
    ),


      dbc.Card(
        [
                    dbc.Button(
                        "+ Prison feature",
                        id=f"group-3-toggle",
                        style={"background-color": "rgb(51,102,204,1)","text-align" : "left", "border" : "0px"}

            ),
            dbc.Collapse(
                dbc.CardBody([
                    html.Div(filter_prison_date_range),
                    html.Div(filter_crime),
                    html.Div(filter_sentence_type)]),
                id="collapse-3",
            ),
        ],
        style={"background-color": "#4573D0",
        	   "border" : "none", 
        	   #"color": "rgb(255,255,255,1)",
        	   "size": "100%"}
    ),

], className="accordion"
),
    ],
    width={"size": 'auto'#,
		   #"offset": 1
		   },
	style={'margin-left': '10px', "background-color": "rgb(51,102,204,1)"},
	#align="center"
),
    # create the app content, simply add every tab created in the folder
dbc.Col([
	dbc.CardHeader(
    dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Overview", label_style={"width": "300px","font-size":"large"}),
        dbc.Tab(tab2_content, label="Socio Demographic", label_style={"width": "300px"}),
        dbc.Tab(tab3_content, label="Reoffenders Classification", label_style={"width": "300px"}),
        dbc.Tab(tab4_content, label="Trends", label_style={"width": "300px"}),
        #dbc.Tab(tab5_content, label="Predictive"),
    ],
    #style={"background-color": "rgb(255,171,0,0.5)"}
),
    #style={"background-color": "rgb(255,171,0,0.5)"},
    )], 
    #style={"background-color": "rgb(255,171,0,0.5)"}
    )

])])


####  callback for acordion frame for filters options
@app.callback(
    [Output("collapse-1", "is_open"),Output("collapse-2", "is_open"),Output("collapse-3", "is_open")],
    [Input("group-1-toggle", "n_clicks"), Input("group-2-toggle", "n_clicks"), Input("group-3-toggle", "n_clicks")],
    [State("collapse-1", "is_open"), State("collapse-2", "is_open"), State("collapse-3", "is_open")],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3 ):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


# update filters options 
@app.callback(
	Output('reclusion_dep', 'options'),
	[Input("group-1-toggle", "n_clicks")],
)
def update_reclusion_dep_dropdown(n):
	options = queries.run('reclusion_dept')
	options2 = [{'label': options[options['id_departamento']==i]['nombre'].values[0], 'value': i} for i in options['id_departamento'].values ]
	return  options2


@app.callback(
	Output('reclusion_entity', 'options'),
	[Input("reclusion_dep", "value")],
)
def update_reclusion_entity_dropdown(dept):
	options = queries.run('reclusion_entity')
	if dept is None:
		options = options
	else:
		options = options[options['departamento']==dept]
	options2 = [{'label': options[options['id_establecimiento']==i]['nombre'].values[0], 'value': i} for i in options['id_establecimiento'].values ]
	return  options2


@app.callback(
	Output('crime', 'options'),
	[Input("group-3-toggle", "n_clicks")],
)
def update_crime_dropdown(n):
	options = queries.run('crime_filter')
	options2 = [{'label': options[options['id_delito']==i]['name_eng'].values[0], 'value': i} for i in options['id_delito'].values ]
	return  options2




#@app.callback(
#	Output('sentence_type', 'options'),
#	[Input("group-3-toggle", "n_clicks")],
#)
#def update_sentence_type_dropdown(n):
#	options = queries.run('sentence_type')
#	options2 = [{'label': options[options['id_delito']==i]['name_eng'].values[0], 'value': i} for i in options['id_delito'].values ]
#	return  options2


######   figures callback 

@app.callback(
	Output('education_level', 'figure'),
	[Input("reclusion_dep", "value"),Input("reclusion_entity", "value")],
)
def figure_education_level(dept, entity):
	data_people_0 = queries.run('people_query')
	if(dept is None):
		data_people = data_people_0
	else:
		data_people = data_people_0[data_people_0['departamento']==dept]

	if(entity is None):
		data_people = data_people
	else:
		data_people = data_people[data_people['establecimiento']==entity]

	education_level_count = data_people[['education level', 'gender','people']].groupby(['education level', 'gender']).sum().reset_index()
	education_level_count = education_level_count.sort_values('people')
	fig = px.bar(education_level_count, x='people', y='education level', color='gender', barmode='group', orientation='h')
	fig.update_traces(marker_line_color='rgb(8,48,107)',
    	              marker_line_width=1.5, opacity=0.6)
	fig.update_layout(title_text='Education level')
	return fig
	







@app.callback(
    [Output('result', 'children'),
    Output('result2', 'children')],
    [Input('reclusion_dep','value')])
def update_result(x):
    return ["The value is; {}".format(x), "The value 2 is; {}".format(x)]




#Initiate the server where the app will work
if __name__ == "__main__":
    db_engine = DbEngine(user = 'team77', 
                        password = 'mintic2020.',
                        ip = 'localhost', 
                        port = '5432', 
                        db = 'minjusticia')
    engine = db_engine.connect()
    queries = Queries(engine)
    app.run_server(debug=True,host='0.0.0.0', port=5000)