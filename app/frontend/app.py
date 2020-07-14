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
from ..backend.utils import DbEngine

#sys.path.insert(1, '/tabContents')


#Create the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Import the tabs content for the individual file

from .tabContents.tab1 import tab1_content
from .tabContents.tab2 import tab2_content
from .tabContents.tab3 import tab3_content
from .tabContents.tab4 import tab4_content
from .tabContents.tab5 import tab5_content

#import filters

from .tabContents.filters import filter_reclusion_dep
from .tabContents.filters import filter_prison_date_range
from .tabContents.filters import filter_crime
from .tabContents.filters import filter_sentence_type
from .tabContents.filters import filter_gender
from .tabContents.filters import filter_range_age
from .tabContents.filters import filter_excep_cond
from .tabContents.filters import filter_reclusion_entity


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


        #dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Col([
            dbc.Row([
                dbc.DropdownMenu(
                    children=[
                         dbc.DropdownMenuItem("Development Team", header=True),
                         dbc.DropdownMenuItem("Page 2", href="#"),
                         dbc.DropdownMenuItem("Page 3", href="#"),
                     ],
                    right=False,
                    nav=True,
                    in_navbar=True,
                    label="Team",
                    color= '#fff',
                    toggle_style={"color": "white"}
        ),

        html.A("ESP", href="http://www.minjusticia.gov.co", style={'color':'#fff'}),
        ]),],
        width={"size": 3, "order": "last", "offset": 5},)
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
         # first group of filters
html.Div(
    [
     dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "+ Reclusion Ubication",
                        color="light",
                        id=f"group-1-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody([html.Div(filter_reclusion_dep),
                    html.Div(filter_reclusion_entity)]),
                id="collapse-1",
            ),
        ]
    ),


    dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "+ Sociodemographic",
                        color="light",
                        id=f"group-2-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody([html.Div(filter_gender),
                    html.Div(filter_range_age),
                    html.Div(filter_excep_cond)]),
                id="collapse-2",
            ),
        ]
    ),


      dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "+ Prison feature",
                        color="light",
                        id=f"group-3-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody([
                    html.Div(filter_prison_date_range),
                    html.Div(filter_crime),
                    html.Div(filter_sentence_type)]),
                id="collapse-3",
            ),
        ]
    ),

], className="accordion"
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
        dbc.Tab(tab3_content, label="Reoffenders Classification"),
        dbc.Tab(tab4_content, label="Trends"),
        #dbc.Tab(tab5_content, label="Predictive"),
    ]
)])

])])



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
                        ip = '172.17.0.3', 
                        port = '5432', 
                        db = 'minjusticia')
    engine = db_engine.connect()
    queries = Queries(engine)
    app.run_server(debug=True,host='0.0.0.0', port=5000)