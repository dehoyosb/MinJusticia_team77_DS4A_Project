import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_table import DataTable

tab3_content = dbc.Card(
    dbc.CardBody(
        [
        	dbc.Row([
        		dbc.Col([dcc.Graph(id='map_risk',style={"height" : "700px", "width" : "auto"}),
        			    ]),
        		
        		dbc.Col([
        			dcc.Graph(id='recividism_risk',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0, 'border-color':'rgb(51,102,204,1)'}),
        			dcc.Graph(id='radar_plot',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0, 'border-color':'rgb(51,102,204,1)'}),
        			]),



        	])
            
        ]
    ),
    className="mt-3",
)