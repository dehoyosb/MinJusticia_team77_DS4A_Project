import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

tab2_content = dbc.Card(
    dbc.CardBody(
        [

        	dbc.Row([
        		dbc.Col([
        			dcc.Graph(id='map',style={"height" : "700px", "width" : "auto"}),
        			]),
        		dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                     html.H3(html.Div(id='number_ofenders'), style = {'color': 'rgb(255,255,255,1)', 'font-weight': 'bold', 'text-align':'center'}),
                     html.H5("Number of Reoffenders", className="card-title", style = {'color': 'rgb(255,255,255,1)', 'font-weight': 'bold',  'text-align':'center'}),
                    ], className="w-100 mb-3",style = {'background-color': 'rgb(51,102,204,1)', 'font-weight': 'bold', 'color':'#fff'}),
                    html.Hr(),]),
                        dbc.Col([

                        dbc.Card([
                     html.H3(html.Div(id='number_inmates'), style = {'color': 'rgb(255,255,255,1)', 'font-weight': 'bold', 'text-align':'center'}),
                     html.H5("Number of Bookings", className="card-title", style = {'color': 'rgb(255,255,255,1)', 'font-weight': 'bold', 'text-align':'center'}),
                     
                    ], className="w-100 mb-3",style = {'background-color': 'rgb(51,102,204,1)', 'font-weight': 'bold', 'color':'#fff'}),
                    html.Hr(),

                    ]),
                ]),
        			dcc.Graph(id='piramid',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0,'border-color':'rgb(51,102,204,1)' }),
                    html.Hr(),
                    dcc.Graph(id='education_level',style={"height" : "300px", "width" : "auto",'margin':5,'border':'1px solid', 'border-radius': 0,'border-color':'rgb(51,102,204,1)'}),
            		]),
                ]),
        ] ,  #style={"height" : "400px", "width" : "600px"}
            #style={'background-color': '#9DBEFF'},
    ),
    className="mt-3",
)





