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
             'ANTIOQUIA':'COLr101',
             'CAUCA':'COLr108',
             'CALDAS':'COLr106',
             'QUINDIO':'COLr119',
             'RISARALDA':'COLr120',
             'ATLANTICO':'COLr102',
             'HUILA':'COLr112',
             'VALLE DEL CAUCA':'COLr124',
             'NARIÑO':'COLr117',
             'ARAUCA':'COLr125',
             'BOYACA':'COLr105',
             'SUCRE':'COLr122',
             'CUNDINAMARCA':'COLr111',
             'AMAZONAS':'COLr129',
             'META':'COLr116',
             'CORDOBA':'COLr110',
             'SANTANDER':'COLr121',
             'BOGOTA D.C.':'COLr103',
             'CESAR':'COLr109',
             'BOLIVAR':'COLr104',
             'LA GUAJIRA':'COLr114',
             'CAQUETA':'COLr107',
             'NORTE DE SANTANDER':'COLr118',
             'PUTUMAYO':'COLr127',
             'TOLIMA':'COLr123',
             'SAN ANDRES Y PROVIDENCIA':'COLr128',
             'MAGDALENA':'COLr115',
             'CASANARE':'COLr126',
             'CHOCO':'COLr112'
        }
        inmate = self.queries.run('etl_select_7')             
        inmate['GDLCODE']= inmate.nombre.apply(lambda x: DEPTO_ESTABLECIMIENTO_key[x] if x != 'tbd' else 0)
        #inmate.FECHA_CAPTURA = pd.to_datetime(inmate.FECHA_CAPTURA)
        #inmate['year'] = inmate.FECHA_CAPTURA.dt.year
        df = pd.merge(df, inmate, on='GDLCODE')
        #df = pd.merge(inmate,df,how='left',on= ['year','GDLCODE'])
        #df.to_sql('sdhi_index', con=self.queries.engine)
        df.to_sql('GDLCODE', con=self.queries.engine) 
        self.queries.run('etl_select_9')       







