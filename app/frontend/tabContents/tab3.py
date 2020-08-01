import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_table import DataTable

tab3_content = dbc.Card(
    dbc.CardBody(
        [
        	dbc.Row([
        		dbc.Col([dcc.Graph(id='map_risk',style={"height" : "600px", "width" : "auto"}),]),
        		dbc.Col([
        			dcc.Graph(id='recividism_risk',style={"height" : "500px", "width" : "auto"}),
        			dcc.Graph(id='radar_plot',style={"height" : "500px", "width" : "auto"}),
        			
        			DataTable(id='risk_table'),

        			]),



        	])
            
        ]
    ),
    className="mt-3",
)