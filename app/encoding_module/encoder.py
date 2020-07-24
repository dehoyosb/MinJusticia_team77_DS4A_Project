import pandas as pd
import numpy as np
import re
import unidecode


class Encoding():
    def __init__(self, query_obj):
        self.queries = query_obj
        
    def get_data(self, sql):
        return self.queries.run(sql)
    
    def one_hot(self, df):
        
        df = df.rename(columns={'nombre': 'delito'})
        counts = df['delito'].value_counts().to_frame()
        df.loc[df[~df['delito'].isin(counts.index[:10].values)].index, 'delito'] = 'OTRO'
            
        one_hot = pd.concat([df[['internoen','fecha_ingreso']],
                     pd.get_dummies(df.delito, prefix='delito'),
                     pd.get_dummies(df.tentativa, prefix='tentativa', drop_first = True),
                     pd.get_dummies(df.agravado, prefix='agravado', drop_first = True),
                     pd.get_dummies(df.calificado, prefix='calificado', drop_first = True),
                     df.groupby(['internoen','fecha_ingreso'])['severity'].max().reset_index(drop=True).to_frame() \
                    .rename(columns = {'severity':'max_severity'}),
                     df.groupby(['internoen','fecha_ingreso'])['severity'].mean().reset_index(drop=True).to_frame() \
                    .rename(columns = {'severity':'mean_severity'})],
                     axis = 1)
        one_hot = one_hot.groupby(['internoen','fecha_ingreso']).max().reset_index()
        
        col = df.columns.tolist()
        for c in ['delito_id_delito', 'id_delito', 'name_eng', 'delito', 'id_registro','id_persona',
                  'persona_id_persona','condicion_exepcional','tentativa','agravado','calificado',
                  'fecha_captura','anio_nacimiento', 'situacion_juridica','reincidente','municipio_id_municipio',
                  'id_subtitulo_delito','severity']:
            col.remove(c)
        
        return df[col].drop_duplicates().merge(one_hot, on = ['internoen','fecha_ingreso'])