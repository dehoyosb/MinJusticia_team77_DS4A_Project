# Libraries
#----------------------------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import json
from urllib.request import urlopen

%matplotlib inline
plt.style.use('seaborn')


# Basics
#----------------------------------------------------------------------------------------------#
# Connect DB
from app.backend.utils import DbEngine, Queries
from app.backend.etl import ETL

# Enconding
from app.encoding_module import encoder

# Connect DB
db_engine = DbEngine(user     = 'team77', 
                     password = 'mintic2020.', 
                     ip       = 'localhost', 
                     port     = '5432', 
                     db       = 'minjusticia2') 

engine    = db_engine.connect()
queries   = Queries(engine)

# Get data
encoding = Encoding(queries)
inmate_df = encoding.get_data('etl_select_8')


# Map
#----------------------------------------------------------------------------------------------#
# Get json file for Departamentos in Colombia
jsonCOL = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'

with urlopen(jsonCOL) as response:
    counties = json.load(response)

# ID as Departamento name for mapping
for loc in counties['features']:
    loc['id'] = loc['properties']['NOMBRE_DPT']
    
# Calculate # of inmates by Departamento of origin in Colombia
temp = inmate.groupby(['persona_id_persona','nombre']).count().id_registro.reset_index() \
             .rename(columns = {'id_registro':'count'}).nombre.value_counts().to_frame().reset_index() \
             .rename(columns = {'index':'DEPTO', 'nombre':'ncount'}) 

# Departamentos names in json file
jsonDPTOname = [depto['properties']['NOMBRE_DPT'] for depto in counties['features']]

# Change departamentos names
temp.DEPTO = temp.DEPTO.replace({'BOGOTA D.C.':'SANTAFE DE BOGOTA D.C',
                                 'SAN ANDRES Y PROVIDENCIA':'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'})

# Map
fig = go.Figure(go.Choroplethmapbox(geojson    = counties, 
                                    locations  = temp.DEPTO, 
                                    z          = temp.ncount, 
                                    colorscale = 'Reds', 
                                    marker_line_width = 0.3))

fig.update_layout(mapbox_style  = "carto-positron", 
                  mapbox_zoom   = 4.5,
                  mapbox_center = {"lat": 4.570868, "lon": -74.2973328}, 
                  margin        = {"r":0, "t":0, "l":0, "b":0})

fig.show()

