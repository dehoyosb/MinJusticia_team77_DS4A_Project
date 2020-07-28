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
from utils.encoder import Encoding
import re
import numpy as np
import chart_studio.plotly as py
import plotly.graph_objs as go
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

import plotly.tools as tls 
import nltk
from nltk.corpus import stopwords



plt.style.use('seaborn')



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


#set function for actualice dataset people when update filters
def data_people_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	if(dept is None):
		data_people = data_people_0
	else:
		data_people = data_people_0[data_people_0['departamento']==dept]

	if(entity is None):
		data_people = data_people
	else:
		data_people = data_people[data_people['establecimiento']==entity]

#	if(pris_start_date is None) and (pris_end_date is None):
#		data_people = data_people
#	else:
#		if pris_end_date is None :
#			start_date = dt.strptime(re.split('T| ', pris_start_date)[0], '%Y-%m-%d').date()
#			data_people = data_people[pd.to_datetime(data_people['fecha_ingreso']) > start_date]
#		if pris_start_date is None :
#			end_date = dt.strptime(re.split('T| ', pris_end_date)[0], '%Y-%m-%d').date()
#			data_people = data_people[pd.to_datetime(data_people['fecha_ingreso']) < end_date]
#		else:
#			end_date = dt.strptime(re.split('T| ', pris_end_date)[0], '%Y-%m-%d').date()
#			start_date = dt.strptime(re.split('T| ', pris_start_date)[0], '%Y-%m-%d').date()
#			data_people = data_people[(data_people['fecha_ingreso'] < end_date)&(data_people['fecha_ingreso'] > start_date)]


	if(crime is None):
		data_people = data_people
	else:
		data_people = data_people[data_people['delito_id_delito']==crime]

	if(gender is None):
		data_people = data_people
	else:
		data_people = data_people[data_people['genero'].isin(gender)]

	data_people = data_people[data_people['actual age'].isin(range(range_age[0],range_age[1]))]

	if(excep_cond ==[]):
		data_people = data_people
	else:
		data_people = data_people[data_people['condicion_excepcional']==2]
	return data_people

#set function for actualice dataset registry when update filters
def inmate_df_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	if(dept is None):
		inmate_df_filt = inmate_df
	else:
		inmate_df_filt = inmate_df[inmate_df['departamento']==dept]

	if(entity is None):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['id_establecimiento']==entity]

#	if(pris_start_date is None) and (pris_end_date is None):
#		inmate_df_filt = inmate_df_filt
#	else:
#		if pris_end_date is None :
#			start_date = dt.strptime(re.split('T| ', pris_start_date)[0], '%Y-%m-%d').date()
#			inmate_df_filt = inmate_df_filt[pd.to_datetime(inmate_df_filt['fecha_ingreso']) > start_date]
#		if pris_start_date is None :
#			end_date = dt.strptime(re.split('T| ', pris_end_date)[0], '%Y-%m-%d').date()
#			inmate_df_filt = inmate_df_filt[pd.to_datetime(inmate_df_filt['fecha_ingreso']) < end_date]
#		else:
#			end_date = dt.strptime(re.split('T| ', pris_end_date)[0], '%Y-%m-%d').date()
#			start_date = dt.strptime(re.split('T| ', pris_start_date)[0], '%Y-%m-%d').date()
#			inmate_df_filt = inmate_df_filt[(inmate_df_filt['fecha_ingreso'] < end_date)&(inmate_df_filt['fecha_ingreso'] > start_date)]


	if(crime is None):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['delito_id_delito']==crime]

	if(gender is None):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['genero'].isin(gender)]

	inmate_df_filt = inmate_df_filt[inmate_df_filt['actual age'].isin(range(range_age[0],range_age[1]))]

	if(excep_cond ==[]):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['condicion_excepcional']==2]
	return inmate_df_filt



def parallel_df_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	if(dept is None):
		inmate_df_filt = parallel_df
	else:
		inmate_df_filt = inmate_df[inmate_df['departamento']==dept]

	if(entity is None):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['id_establecimiento']==entity]

	if(crime is None):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['delito_id_delito']==crime]

	if(gender is None):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['genero'].isin(gender)]

	inmate_df_filt = inmate_df_filt[inmate_df_filt['actual age'].isin(range(range_age[0],range_age[1]))]

	if(excep_cond ==[]):
		inmate_df_filt = inmate_df_filt
	else:
		inmate_df_filt = inmate_df_filt[inmate_df_filt['condicion_excepcional']==2]
	return inmate_df_filt



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
	options2 = [{'label': options[options['id_departamento']==i]['nombre'].values[0].capitalize(), 'value': i} for i in options['id_departamento'].values ]
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
	options2 = [{'label': options[options['id_establecimiento']==i]['nombre'].values[0].capitalize(), 'value': i} for i in options['id_establecimiento'].values ]
	return  options2


@app.callback(
	Output('crime', 'options'),
	[Input("group-3-toggle", "n_clicks")],
)
def update_crime_dropdown(n):
	options = queries.run('crime_filter')
	options2 = [{'label': options[options['id_delito']==i]['name_eng'].values[0].capitalize(), 'value': i} for i in options['id_delito'].values ]
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
	[Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
	 Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")],
)
def figure_education_level(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	data_people = data_people_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	education_level_count = data_people[['education level', 'gender','people']].groupby(['education level', 'gender']).sum().reset_index()
	education_level_count = education_level_count.sort_values('people')
	fig = px.bar(education_level_count, x='people', y='education level', color='gender', barmode='group', orientation='h')
	fig.update_traces(marker_line_color='rgb(8,48,107)',
    	              marker_line_width=1.5, opacity=0.6)
	fig.update_layout(title_text='Education level', legend_title_text='')
	fig.update_layout(margin= {"r":0, "t":50, "l":0, "b":0})
	fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1))
	return fig
	

@app.callback(
	Output('piramid', 'figure'),
	[Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
	 Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")],
)
def figure_education_level(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	data_people = data_people_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)

	piramide_male = data_people[data_people['gender']=='MALE'][['range_age', 'people']].groupby(['range_age']).sum().reset_index()
	piramide_female = data_people[data_people['gender']=='FEMALE'][['range_age', 'people']].groupby(['range_age']).sum().reset_index()
	if len(piramide_male.index) == 0:
		piramide = piramide_female
		piramide.columns = ['range_age','female']
		piramide['male'] = 0
	else:
		if len(piramide_female.index) == 0:
			piramide = piramide_male
			piramide.columns = ['range_age','male']
			piramide['female'] = 0
		else:
			piramide = pd.merge(piramide_male, piramide_female, on = 'range_age')
			piramide.columns = ['range_age', 'male','female']

	
	women_bins = np.array(-1 * piramide['female'])
	men_bins = np.array(piramide['male'])

	y = list(range(10, 100, 10))

	fig = go.Figure(
	layout = go.Layout(yaxis=go.layout.YAxis(title='Age'),
	                   xaxis=go.layout.XAxis(
	                       range=[-1 * (np.array(piramide['male']).max()*(1.2)), (np.array(piramide['male']).max()*(1.2))],
	                       #tickvals=[-50000, -20000, 0, 20000, 50000],
	                       #ticktext=[50000, 20000, 0, 20000, 50000],
	                       title='Number'),
	                   barmode='overlay',
	                   bargap=0.1),

	data = [go.Bar(y=y,
	               x=men_bins,
	               orientation='h',
	               name='MALE',
	               hoverinfo='x',
	               marker=dict(color = 'Royal Blue')
	               ),
	        go.Bar(y=y,
	               x=women_bins,
	               orientation='h',
	               name='FEMALE',
	               text=-1 * women_bins.astype('int'),
	               hoverinfo='text',
	               marker=dict(color = 'Orange')
	               )])
	fig.update_layout(title_text='population pyramid')
	fig.update_layout(margin= {"r":0, "t":50, "l":0, "b":0}, legend_title_text='')
	fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1))
	return fig


@app.callback(
	Output('map', 'figure'),
	[Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
	 Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")],
)
def figure_map(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	# Get data
	inmate_df_1 = inmate_df_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	# Map
	#----------------------------------------------------------------------------------------------#
	# Get json file for Departamentos in Colombia
	jsonCOL = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'

	with urlopen(jsonCOL) as response:
	    counties = json.load(response)

	# ID as Departamento name for mapping
	for loc in counties['features']:
	    loc['id'] = loc['properties']['NOMBRE_DPT']
	    
	# Calculate # of inmates by Departamento of origin in Colombia
	temp = inmate_df_1.groupby(['persona_id_persona','nombre']).count().id_registro.reset_index() \
	             .rename(columns = {'id_registro':'count'}).nombre.value_counts().to_frame().reset_index() \
	             .rename(columns = {'index':'DEPTO', 'nombre':'ncount'}) 

	# Departamentos names in json file
	jsonDPTOname = [depto['properties']['NOMBRE_DPT'] for depto in counties['features']]

	# Change departamentos names
	temp.DEPTO = temp.DEPTO.replace({'BOGOTA D.C.':'SANTAFE DE BOGOTA D.C',
	                                 'SAN ANDRES Y PROVIDENCIA':'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'})

	# Map
	fig = go.Figure(go.Choroplethmapbox(geojson    = counties, 
	                                    locations  = temp.DEPTO, 
	                                    z          = temp.ncount, 
	                                    colorscale = 'Reds', 
	                                    marker_line_width = 0.3),
					layout = dict(
						            title='boh',
						            autosize=True,
						        ))

	fig.update_layout(mapbox_style  = "carto-positron", 
	                  mapbox_zoom   = 4.5,
	                  mapbox_center = {"lat": 4.570868, "lon": -74.2973328}, 
	                  margin        = {"r":0, "t":50, "l":0, "b":0})
	return fig





@app.callback(
    [Output('number_ofenders', 'children')],
    [Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
     Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")])
def update_number_ofenders(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	data_people = data_people_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	x = data_people.people.count()
	return ["{}".format(x)]





@app.callback(
    Output('surv_study', 'figure'),
    [Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
     Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")])
def update_surv_study(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	inmate_df_1 = inmate_df_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	#data_people_receiv = inmate_df_1[~inmate_df_1['fecha_salida_anterior'].isna()]
	data_people_receiv = inmate_df_1[inmate_df_1['tiempo_nuevo_delito']>0]
	data_people_receiv = data_people_receiv.reset_index()
	
	fig = go.Figure()
	kmf.fit(data_people_receiv[data_people_receiv['actividades_estudio']==2]['tiempo_nuevo_delito'], 
	        event_observed=data_people_receiv[data_people_receiv['actividades_estudio']==2]['event'],
	        label='data')
	df = kmf.survival_function_
	df = df.reset_index()
	fig.add_trace(go.Scatter(x=df["timeline"], y=df["data"],mode='lines', name="With study activities"))

	kmf.fit(data_people_receiv[data_people_receiv['actividades_estudio']==1]['tiempo_nuevo_delito'], 
	        event_observed=data_people_receiv[data_people_receiv['actividades_estudio']==1]['event'],
	        label='data')
	df = kmf.survival_function_
	df = df.reset_index()
	fig.add_trace(go.Scatter(x=df["timeline"], y=df["data"],mode='lines', name="Without study activities"))
	fig.update_layout(title='Recividism survival curve by study activities',
	                   xaxis_title='Time in months until recidivism',
	                   yaxis_title='Survival for recidivism')
	fig.update_layout(margin= {"r":0, "t":50, "l":0, "b":0}, legend_title_text='')
	fig.update_layout(legend=dict(
    yanchor="top",
    y=1.02,
    xanchor="right",
    x=1))
	return fig


@app.callback(
    Output('surv_work', 'figure'),
    [Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
     Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")])
def update_surv_work(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	inmate_df_1 = inmate_df_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	#data_people_receiv = inmate_df_1[~inmate_df_1['fecha_salida_anterior'].isna()]
	data_people_receiv = inmate_df_1[inmate_df_1['tiempo_nuevo_delito']>0]
	data_people_receiv = data_people_receiv.reset_index()
	
	fig = go.Figure()
	kmf.fit(data_people_receiv[data_people_receiv['actividades_trabajo']==2]['tiempo_nuevo_delito'], 
	        event_observed=data_people_receiv[data_people_receiv['actividades_trabajo']==2]['event'],
	        label='data')
	df = kmf.survival_function_
	df = df.reset_index()
	fig.add_trace(go.Scatter(x=df["timeline"], y=df["data"],mode='lines', name="With work activities"))

	kmf.fit(data_people_receiv[data_people_receiv['actividades_trabajo']==1]['tiempo_nuevo_delito'], 
	        event_observed=data_people_receiv[data_people_receiv['actividades_trabajo']==1]['event'],
	        label='data')
	df = kmf.survival_function_
	df = df.reset_index()
	fig.add_trace(go.Scatter(x=df["timeline"], y=df["data"],mode='lines', name="Without work activities"))
	fig.update_layout(title='Recividism survival curve by work activities',
	                   xaxis_title='Time in months until recidivism',
	                   yaxis_title='Survival for recidivism')
	fig.update_layout(margin= {"r":0, "t":50, "l":0, "b":0}, legend_title_text='')
	fig.update_layout(legend=dict(
    yanchor="top",
    y=1.02,
    xanchor="right",
    x=1))
	return fig



@app.callback(
    Output('education_level_age', 'figure'),
    [Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
     Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")])
def update_education_level_age(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	data_people = data_people_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	education_level_count = data_people[['actual age','education level','people']].groupby(['actual age','education level']).sum().reset_index()
	#education_level_count = education_level_count.sort_values('people')
	#fig.add_trace(go.Scatter(x=education_level_count["actual age"], y=education_level_count["people"],mode='lines', name="Education level by actual age"))
	fig = px.line(education_level_count, x='actual age', y='people', color='education level', title='Education level by actual age')
	fig.update_layout(margin= {"r":0, "t":50, "l":0, "b":0})
	fig.update_layout(title_text='Age by educational level', legend_title_text='')
	fig.update_layout(legend=dict(
    yanchor="top",
    y=1.02,
    xanchor="right",
    x=1))
	return fig



@app.callback(
    Output('parallel_graph', 'figure'),
    [Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
     Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")])
def update_parallel_graph(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	df=parallel_df_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	fig = px.parallel_categories(
                             df, 
                             dimensions=['titulo', 'subtitulo', 'delito'],
                             labels={'titulo':'Titulo', 
                                     'subtitulo':'Subtitulo', 
                                     'delito':'Delito'}#,
                             #width=1000, 
                             #height=800
                             )
	return fig



@app.callback(
    Output('context_minj_graph', 'figure'),
    [Input("reclusion_dep", "value"),Input("reclusion_entity", "value"),Input("prison_date_range", "start_date"),Input("prison_date_range", "end_date"),
     Input("crime", "value"),Input("gender", "value"),Input("range_age", "value"),Input("excep_cond", "value")])
def update_context_minj_graph(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond):
	people = data_people_funct(dept, entity, pris_start_date, pris_end_date, crime, gender, range_age, excep_cond)
	people.fecha_ingreso = pd.to_datetime(people.fecha_ingreso)
	people['year'] = people.fecha_ingreso.dt.year
	people = people[['year','people']].groupby('year').count()
	people = people.reset_index()
	people.columns = ['year','reoffenders']
	df_merge = pd.merge(context_minjusticia_df,people, how='left',on ='year')
	df_merge.set_index('year',inplace=True)
	df_merge['reoffenders'] = df_merge['reoffenders']/1000
	df_merge = df_merge.reset_index()
	temp = df_merge.melt(id_vars='year', value_vars= ['population', 'capacity', 'reoffenders'])
	labels = ['population', 'capacity', 'reoffenders']
	x_data_temp =[]
	y_data_temp = []
	for i,var in enumerate(labels):
	    x_data_temp.append(temp[temp.variable==var]['year'].values)
	    y_data_temp.append(temp[temp.variable==var]['value'].values)

	title = 'Jail Population in Colombia'
	labels = ['Population', 'Capacity', 'Reoffenders']
	colors = ['rgb(67,67,67)', 'rgb(168, 50, 50)', 'rgb(49,130,189)']
	percentages = ['149','100','11']
	mode_size = [10, 10, 10]
	line_size = [3, 3, 5]
	x_data = x_data_temp
	y_data = y_data_temp
	fig = go.Figure()

	for i in range(0, 3):
	    fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
	        name=labels[i],
	        line=dict(color=colors[i], width=line_size[i]),
	        connectgaps=True,
	    ))
	    # endpoints
	    fig.add_trace(go.Scatter(
	        x=[x_data[i][0], x_data[i][-1]],
	        y=[y_data[i][0], y_data[i][-1]],
	        mode='markers',
	        marker=dict(color=colors[i], size=mode_size[i])
	    ))
	fig.update_layout(
	    xaxis=dict(
	        showline=True,
	        showgrid=False,
	        showticklabels=True,
	        linecolor='rgb(204, 204, 204)',
	        linewidth=2,
	        ticks='outside',
	        tickfont=dict(
	            family='Arial',
	            size=11,
	            color='rgb(82, 82, 82)',
	        ),
	    ),
	    yaxis=dict(
	        showgrid=False,
	        zeroline=False,
	        showline=False,
	        showticklabels=True,
	    ),
	    autosize=True,
	    margin=dict(
	        autoexpand=True,
	        l=100,
	        r=20,
	        t=110,
	    ),
	    showlegend=False,
	    plot_bgcolor='white'
	)
	annotations = []
	# Adding labels
	for y_trace, label, color, percentage in zip(y_data, labels, colors, percentages):
	    annotations.append(dict(xref='paper', x=0.75, y=y_trace[-1],
	                                  xanchor='left', yanchor='bottom',
	                                  text=label+': {}k, ({}%)'.format(int(y_trace[-1]),percentage),
	                                  font=dict(family='Work Sans',
	                                            size=14.5),
	                                  showarrow=False))
	# Title
	annotations.append(dict(xref='paper', yref='paper', x=0.3, y=1,
	                              xanchor='left', yanchor='bottom',
	                              text=title,
	                              font=dict(family='Work Sans',
	                                        size=25,
	                                        color='rgb(37,37,37)'),
	                              showarrow=False))
	# Source
	annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
	                              xanchor='center', yanchor='top',
	                              text='Source: INPEC & datos.gov.co',
	                              font=dict(family='Work Sans',
	                                        size=12,
	                                        color='rgb(150,150,150)'),
	                              showarrow=False))
	fig.update_layout(annotations=annotations)

	return fig




#Initiate the server where the app will work
if __name__ == "__main__":
#    db_engine = DbEngine(user = 'postgres', 
#                        password = 'YyjnDpcVRtpHDOHHzr58',
#                        ip = 'database-1.cjppulxuzu8c.us-east-2.rds.amazonaws.com', 
#                        port = '5432', 
#                        db = 'minjusticia')
    db_engine = DbEngine(user = 'team77', 
                        password = 'mintic2020.',
                        ip = 'localhost', 
                        port = '5432', 
                        db = 'minjusticia')
    nltk.download('stopwords')
    stopwords_list = stopwords.words('english')
    kmf = KaplanMeierFitter()
    engine = db_engine.connect()
    queries = Queries(engine)
    data_people_0 = queries.run('people_query')
    encoding = Encoding(queries)
    inmate_df_0 = encoding.get_data('etl_select_8')
    inmate_df = encoding.surv_encode (inmate_df_0)
    parallel_df = encoding.parallel_encode(inmate_df_0, stopwords_list)
    context_minjusticia_df = queries.run('context_minjusticia')
    app.run_server(debug=True,host='0.0.0.0', port=5000)