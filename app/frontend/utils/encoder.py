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
                     pd.get_dummies(df.tentativa, prefix='tentativa'),
                     pd.get_dummies(df.agravado, prefix='agravado'),
                     pd.get_dummies(df.calificado, prefix='calificado'),
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

    def surv_encode(self, df):
        df['fecha_salida_anterior'] = df['fecha_salida2'].shift(1)
        df.loc[df['numero'] == 1,'fecha_salida_anterior'] = np.nan
        df['tiempo_nuevo_delito'] = (df['fecha_ingreso']-df['fecha_salida_anterior'])/ np.timedelta64(1, 'M')
        df['event'] = 1
        df['event'] = df.apply(lambda x: 0 if (x.numero_evento==1)&(x.estado_id_estado==2) else 1, axis=1)
        one_hot = pd.concat([df[['id_persona','fecha_ingreso']],
                     pd.get_dummies(df.actividades_estudio, prefix='estudio'),
                     pd.get_dummies(df.actividades_trabajo, prefix='trabajo'),
                     pd.get_dummies(df.actividades_enseñanza, prefix='enseñanza'),
                     pd.get_dummies(df.madre_gestante, prefix='madre_gestante'),
                     pd.get_dummies(df.madre_lactante, prefix='madre_lactante'),
                     pd.get_dummies(df.discapacidad, prefix='discapacidad'),
                     pd.get_dummies(df.adulto_mayor, prefix='adulto_mayor'),
                     df.groupby(['id_persona','fecha_ingreso'])['severity'].max().reset_index(drop=True).to_frame() \
                    .rename(columns = {'severity':'max_severity'}),
                     df.groupby(['id_persona','fecha_ingreso'])['severity'].mean().reset_index(drop=True).to_frame() \
                    .rename(columns = {'severity':'mean_severity'})],
                     axis = 1)
        df = df.merge(one_hot, on = ['id_persona','fecha_ingreso'], how = 'left')
        return df

    def parallel_encode(self, df, stopwords_list):
        counts = df['delito'].value_counts().to_frame()
        counts['%'] = 100*(counts['delito'].cumsum() / counts['delito'].sum())
        counts = counts[:10]
        test = df[df['delito'].isin(counts.index.values)]
        test['titulo'] = test['titulo'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in stopwords_list]))
        test['subtitulo'] = test['subtitulo'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in stopwords_list]))
        test['delito'] = test['delito'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in stopwords_list]))
        return test