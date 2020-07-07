import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import sys
#sys.path.insert(1, '/tabContents')


#Create the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Import the tabs content for the individual file

from tabContents.tab1 import tab1_content
from tabContents.tab2 import tab2_content
from tabContents.tab3 import tab3_content
from tabContents.tab4 import tab4_content
from tabContents.tab5 import tab5_content



#Create Layout
app.layout = html.Div([
    # create the navbar, the first bar
    dbc.Navbar(
    [
        html.A(
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

        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Development Team", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            right=True,
            nav=True,
            in_navbar=True,
            label="Team",
            color= '#fff',
            style={'color':'#fff','text-align':'left'}
        ),

        html.A("ESP", href="http://www.minjusticia.gov.co", style={'color':'#fff','text-align':'right'})
    ],
    color='#345bc6',
    dark=True,
),

dbc.Row(
    [
    ###  create sidebar 
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
    # create the app content, simply add every tab created in the folder
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