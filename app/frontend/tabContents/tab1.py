import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

tab1_content = dbc.Card(
    dbc.CardBody(
        [
        dbc.Col([
        	dbc.Row([
        		dbc.Col([dcc.Graph(id='context_minj_graph',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0, 'border-color':'rgb(51,102,204,1)'}),]),
        		dbc.Col([dcc.Graph(id='top_crimes',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0, 'border-color':'rgb(51,102,204,1)'}),]),
        		]),
        	dcc.Graph(id='parallel_graph',style={"height" : "400px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0, 'border-color':'rgb(51,102,204,1)' })
        ])
        
        ]
    ),
    className="mt-3",
)