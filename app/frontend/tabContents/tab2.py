import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

tab2_content = dbc.Card(
    dbc.CardBody(
        [

        	dbc.Row([
        		dbc.Col([
        			dcc.Graph(id='map',style={"height" : "600px", "width" : "auto"}),
        			]),
        		dbc.Col([
                    dbc.Card([
                     html.H2("Number of Offenders", className="card-title", style = {'color': 'rgb(255,255,255,1)', 'font-weight': 'bold'}),
                     html.H3(html.Div(id='number_ofenders')),
                    ], className="w-75 mb-3",style = {'background-color': 'rgb(51,102,204,1)', 'font-weight': 'bold', 'color':'#fff'}),
                    html.Hr(),
        			dcc.Graph(id='piramid',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0}),
                    html.Hr(),
                    dcc.Graph(id='education_level',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0}),
            		]),
                dbc.Col([
                    dbc.Card([
                     html.H2("Number of Inmates", className="card-title", style = {'color': 'rgb(255,255,255,1)', 'font-weight': 'bold'}),
                     html.H3(html.Div(id='number_inmates')),
                    ], className="w-75 mb-3",style = {'background-color': 'rgb(51,102,204,1)', 'font-weight': 'bold', 'color':'#fff'}),
                    html.Hr(),
                    dcc.Graph(id='education_level_age',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0}),
                    ]),

                ]),
        ] ,  #style={"height" : "400px", "width" : "600px"}
            #style={'background-color': '#9DBEFF'},
    ),
    className="mt-3",
)





