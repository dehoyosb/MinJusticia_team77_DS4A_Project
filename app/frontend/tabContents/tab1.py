import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

tab1_content = dbc.Card(
    dbc.CardBody(
        [
        dbc.Col([
        	dbc.Row([html.H3('Primera fila')]),
        	dbc.Row([html.H3('Segunda fila')]),
        	dbc.Row([dcc.Graph(id='parallel_graph',style={"height" : "600px", "width" : "auto"})]),
        ])
        
        ]
    ),
    className="mt-3",
)