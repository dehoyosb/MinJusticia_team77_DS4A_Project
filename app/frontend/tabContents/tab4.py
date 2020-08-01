import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


tab4_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
        		dbc.Col([
        			dcc.Graph(id='surv_study',style={"height" : "400px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0,'border-color':'rgb(51,102,204,1)'}),
        			html.Hr(),
        			dcc.Graph(id='surv_work',style={"height" : "400px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0,'border-color':'rgb(51,102,204,1)'}),
        			]),
                dbc.Col([
                    dcc.Graph(id='hazard_severity',style={"height" : "400px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0,'border-color':'rgb(51,102,204,1)'}),
                    html.Hr(),
                    dcc.Graph(id='hazard_shdi',style={"height" : "400px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0,'border-color':'rgb(51,102,204,1)'}),
                    ]),
        		]),
        ]
    ),
    className="mt-3",
)