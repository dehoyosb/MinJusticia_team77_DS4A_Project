import re
import unidecode
import pandas as pd
import numpy as np

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from ..utils.metrics import binprob, accuracy_t, precision_t, recall_t, f1_t
from .preprocessing import reduce_cats, dummy_helper, binarize, missing_ind


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
    
    def supervised(self, inmate):
        # Feature changes
        # Dates
        inmate.fecha_ingreso = pd.to_datetime(inmate.fecha_ingreso)
        inmate.fecha_salida  = pd.to_datetime(inmate.fecha_salida)
        inmate.fecha_captura = pd.to_datetime(inmate.fecha_captura)

        # Crime types
        inmate.tentativa  = inmate.tentativa .apply(lambda x: 'TENT_' if x == 2 else '')
        inmate.agravado   = inmate.agravado  .apply(lambda x: 'AGRA_' if x == 2 else '')
        inmate.calificado = inmate.calificado.apply(lambda x: 'CALF_' if x == 2 else '')

        # Activities
        inmate.actividades_trabajo   = inmate.actividades_trabajo  .apply(lambda x: 1 if x == 2 else 0)
        inmate.actividades_estudio   = inmate.actividades_estudio  .apply(lambda x: 1 if x == 2 else 0)
        inmate.actividades_enseñanza = inmate.actividades_enseñanza.apply(lambda x: 1 if x == 2 else 0)

        # Children: Y/N
        inmate.hijos_menores = inmate.hijos_menores.apply(lambda x: 1 if x == 2 else 0)

        # Genero
        inmate.genero = inmate.genero.apply(lambda x: 1 if x == 2 else 0) # Masculino baseline

        # Condición excepcional
        inmate.madre_gestante = inmate.madre_gestante.apply(lambda x: 1 if x == 2 else 0)
        inmate.madre_lactante = inmate.madre_lactante.apply(lambda x: 1 if x == 2 else 0)
        inmate.discapacidad   = inmate.discapacidad  .apply(lambda x: 1 if x == 2 else 0)
        inmate.adulto_mayor   = inmate.adulto_mayor  .apply(lambda x: 1 if x == 2 else 0)

        # Crime + crime type
        inmate['delito_comp'] = inmate.tentativa + inmate.agravado + inmate.calificado + inmate.crimenme_en
        
        # Reduce categories
        inmate.delito_comp = reduce_cats(inmate.delito_comp, 20)
        inmate.country     = reduce_cats(inmate.country, 2)
        
        # Column names upper case
        inmate.columns = [colname.upper() for colname in inmate.columns.tolist()]
        
        # Select features of interest
        inmate = inmate[['INTERNOEN',
                         'DELITO_COMP',
                         'FECHA_INGRESO','FECHA_SALIDA','FECHA_CAPTURA',
                         'ANIO_NACIMIENTO','GENERO','MARITALSTATUS','EDUC_LEVEL','HIJOS_MENORES',
                         'COUNTRY',
                         'ACTIVIDADES_TRABAJO','ACTIVIDADES_ESTUDIO','ACTIVIDADES_ENSEÑANZA',
                         'MADRE_GESTANTE','MADRE_LACTANTE','DISCAPACIDAD','ADULTO_MAYOR',
                         'SEVERITY', 
                         'SHDI','HEALTHINDEX','INCINDEX','EDINDEX','LIFEXP','GNIC','ESCH','MSCH','POP',
                         'JAILNAME','REGIONALNME']]
        
        # Intermediate table
        iscat  = [nme for nme in inmate.columns[inmate.dtypes == 'object'] if nme != 'INTERNOEN' and nme != 'FECHA_SALIDA']
        inmate = binarize(inmate, iscat)[0]
        inmate = inmate.drop(iscat, axis = 1)
        inmate = inmate.drop(['FECHA_CAPTURA'], axis = 1)
        
        # Time in jail 
        inmate['timejail_day'] = (inmate.FECHA_SALIDA - inmate.FECHA_INGRESO)
        inmate.timejail_day    = inmate.timejail_day.dt.days
        
        # Key: inmate + booking date
        inmate_booking = inmate.copy().sort_values(by = ['INTERNOEN','FECHA_INGRESO'])\
                                      .groupby(['INTERNOEN','FECHA_INGRESO'])\
                                      .max()\
                                      .reset_index()
        
        # Recidivism in days and booking data t-1
        inmate_booking['FECHA_SALIDA_t_1'] = inmate_booking.groupby('INTERNOEN').FECHA_SALIDA.shift(1)
        inmate_booking['recidivism_day']   = (inmate_booking.FECHA_INGRESO - inmate_booking.FECHA_SALIDA_t_1).dt.days
        
        # Year booking date 
        inmate_booking['year'] = inmate_booking.FECHA_INGRESO.dt.year
        
        # Impute recidivism and time in jail 
        # Methodology: conditional imputation with 10 iterations (default)
        imp_omit   = ['FECHA_INGRESO','FECHA_SALIDA','FECHA_SALIDA_t_1','INTERNOEN']
        df_imp     = inmate_booking.drop(columns = imp_omit)
        imp_mean   = IterativeImputer(random_state = 0, max_iter = 10, add_indicator = True, n_nearest_features = 5)
        inmate_imp = imp_mean.fit_transform(df_imp)
        
        # Imputation labels
        imp_lab = list(set(inmate_booking.columns[inmate_booking.isna().any()] \
                  .tolist()).difference(set(['FECHA_INGRESO','FECHA_SALIDA','FECHA_SALIDA_t_1','INTERNOEN'])))
        # Imputed values
        inmate_imp = pd.DataFrame(inmate_imp, columns = df_imp.columns.tolist() + ['imp_' + nme for nme in imp_lab])
        
        # Replace imputed values
        inmate_booking.recidivism_day    = inmate_imp.recidivism_day
        inmate_booking.timejail_day      = inmate_imp.timejail_day
        inmate_booking.MSCH              = inmate_imp.MSCH
        inmate_booking.EDINDEX           = inmate_imp.EDINDEX
        inmate_booking.LIFEXP            = inmate_imp.LIFEXP
        inmate_booking.SHDI              = inmate_imp.SHDI
        inmate_booking.GNIC              = inmate_imp.GNIC
        inmate_booking.ESCH              = inmate_imp.ESCH
        inmate_booking.POP               = inmate_imp.POP
        inmate_booking.HEALTHINDEX       = inmate_imp.HEALTHINDEX
        inmate_booking.INCINDEX          = inmate_imp.INCINDEX

        # Missing values
        for nme in imp_lab:
            inmate_booking[nme] = inmate_imp[nme]
            
        # Delete negative values from time in jail and recidivism 
        inmate_booking = inmate_booking[inmate_booking.timejail_day   >= 0] # omit 3041
        inmate_booking = inmate_booking[inmate_booking.recidivism_day >= 0] # omit 841
        
        return inmate_booking