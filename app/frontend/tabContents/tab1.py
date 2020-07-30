import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

tab1_content = dbc.Card(
    dbc.CardBody(
        [
        dbc.Col([
        	dbc.Row([html.H3('Primera fila')]),
        	dbc.Row([dcc.Graph(id='context_minj_graph',style={"height" : "400px", "width" : "auto"})]),
        	dcc.Graph(id='parallel_graph',style={"height" : "500px", "width" : "80%"})
        ])
        
        ]
    ),
    className="mt-3",
)