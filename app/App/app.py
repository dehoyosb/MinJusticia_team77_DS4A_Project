import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

#Create the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Create the tabs and content

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tab5_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

#########
###  create sidebar 

#Create Layout
app.layout = html.Div([
    dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
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
        dbc.NavbarToggler(id="navbar-toggler")#,
        #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color='#345bc6',
    dark=True,
),
dbc.Row(
    [
dbc.Col(
    [
        html.H2("Filters", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
    ],
    width=2
),
dbc.Col([
    dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Overview"),
        dbc.Tab(tab2_content, label="Socio Demographic"),
        dbc.Tab(tab3_content, label="Clustering"),
        dbc.Tab(tab4_content, label="Trends"),
        dbc.Tab(tab5_content, label="Predictive"),
    ]
)])

])])


#@app.callback(
#    Output('main-figure','figure'),
#    [Input('fig-slider','value')])
#def slider_interaction(slider_val):
#    if slider_val==0:
#        fig=Map_Fig
#    else:
#        fig=Scatter_Fig
#
#    return fig 



#Initiate the server where the app will work
if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0', port=5000)