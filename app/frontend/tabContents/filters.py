import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt

filter_reclusion_dep= html.Div([html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Reclusion Department", className="lead"
        ),
        dcc.Dropdown(
        id='reclusion_dep',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),])


filter_reclusion_entity= html.Div([html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Reclusion Entity", className="lead"
        ),
        dcc.Dropdown(
        id='reclusion_entity',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),])



filter_prison_date_range = html.Div([
	html.P(
            "Prision income date range", className="lead"
        ),
		dcc.DatePickerRange(
							id='prison_date_range',
							min_date_allowed=dt(2010, 1, 1),
							max_date_allowed=dt(2021, 1, 1),
							initial_visible_month=dt(2020, 7, 1)#,
							#end_date=dt(2020, 7, 15).date()
		),])





filter_crime=html.Div([html.P(
					            "                 ", className="lead"
					        ),
							html.P(
					            "Crime", className="lead"
					        ),
							dcc.Dropdown(
					        id='crime',
					        options=[
					            {'label': 'New York City', 'value': 'NYC'},
					            {'label': 'Montreal', 'value': 'MTL'},
					            {'label': 'San Francisco', 'value': 'SF'}
					        ],
					        value='NYC'
					    ),])


filter_sentence_type = html.Div([	html.P(
						            "                 ", className="lead"
						        ),
								html.P(
						            "Sentence Type", className="lead"
						        ),
								dcc.Dropdown(
						        id='sentence_type',
						        options=[
						            {'label': 'New York City', 'value': 'NYC'},
						            {'label': 'Montreal', 'value': 'MTL'},
						            {'label': 'San Francisco', 'value': 'SF'}
						        ],
						        value='NYC'
						    ),])



filter_gender = html.Div([	html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Gender", className="lead"
        ),
	
	dcc.Checklist(
		id='gender',
		options=[
			{'label': 'Male', 'value': '2'},
			{'label': 'Female', 'value': '1'},
		],
		value=['1', '2'],
		labelStyle={'display': 'inline-block', 'align': 'center', 'padding-left' : '30px'}
),])



filter_range_age = html.Div([	html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Range Age", className="lead"
        ),
	dcc.RangeSlider(
					id='range_age',
					count=1,
					min=15,
					max=100,
					step=1,
					value=[15, 100],
					marks={15:'15', 20: '20', 30:'30', 40:'40',50:'50',60:'60',70:'70',80:'80',90:'90',100:'100'},
					tooltip={'always_visible': True}

), ])



filter_excep_cond = html.Div([html.P(
            "                 ", className="lead"
        ),
		html.P(
            "Exceptional Conditions", className="lead"
        ),
	
	dcc.Checklist(
		id='excep_cond',
		options=[
			{'label': 'Yes', 'value': '2'},
		],
		#value=['1', '2'],
		labelStyle={'display': 'inline-block', 'align': 'center', 'padding-left' : '30px'}
), ])


