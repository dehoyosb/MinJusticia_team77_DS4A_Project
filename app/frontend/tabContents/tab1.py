import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

tab1_content = dbc.Card(
    dbc.CardBody(
        [
        dbc.Col([
        	dbc.Row([
        		dbc.Col([dcc.Graph(id='context_minj_graph',style={"height" : "400px", "width" : "auto"}),]),
        		dbc.Col([dcc.Graph(id='top_crimes',style={"height" : "400px", "width" : "auto"}),]),
        		]),
        	dcc.Graph(id='parallel_graph',style={"height" : "500px", "width" : "auto"})
        ])
        
        ]
    ),
    className="mt-3",
)