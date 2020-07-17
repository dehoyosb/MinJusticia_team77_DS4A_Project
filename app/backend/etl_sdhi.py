#Packages:
import pandas as pd
import string
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

class ETL_SDHI():
    def __init__(self, query_obj):
        self.queries = query_obj
        
    def inmate_static_info(self, df):
        # set dictionary for SDHI table 
        DEPTO_ESTABLECIMIENTO_key = {
             'ANTIOQUIA':1,
             'CAUCA':8,
             'CALDAS':6,
             'QUINDIO':19,
             'RISARALDA':20,
             'ATLANTICO':2,
             'HUILA':13,
             'VALLE DEL CAUCA':24,
             'NARIÑO':17,
             'ARAUCA':25,
             'BOYACA':5,
             'SUCRE':22,
             'CUNDINAMARCA':11,
             'AMAZONAS':29,
             'META':16,
             'CORDOBA':10,
             'SANTANDER':21,
             'BOGOTA D.C.':3,
             'CESAR':9,
             'BOLIVAR':4,
             'LA GUAJIRA':14,
             'CAQUETA':7,
             'NORTE DE SANTANDER':18,
             'PUTUMAYO':27,
             'TOLIMA':23,
             'SAN ANDRES Y PROVIDENCIA':28,
             'MAGDALENA':15,
             'CASANARE':26,
             'CHOCO':12
        }
        inmate = self.queries.run('etl_select_7')             
        inmate['shdi_id']= inmate.nombre.apply(lambda x: DEPTO_ESTABLECIMIENTO_key[x] if x != 'tbd' else 0)
        df['region_norm'] = df['region'].apply(lambda x: x.split('(')[0].strip().upper())
        df = pd.merge(df, inmate, left_on = 'region_norm', right_on = 'nombre')
        df.to_sql('sdhi_index', con=self.queries.engine)
                







