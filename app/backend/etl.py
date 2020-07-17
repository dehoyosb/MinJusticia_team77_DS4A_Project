#Packages:
import pandas as pd
import string
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

class ETL():
    def __init__(self, query_obj):
        self.queries = query_obj
        
    def inmate_static_info(self, data):
        ############## etnic recognition
        data_people = data[['INTERNOEN', 'GENERO', 'PAIS_INTERNO', 'REINCIDENTE', 
                            'ANO_NACIMIENTO', 'ESTADO_CIVIL','NIVEL_EDUCATIVO', 'CONDIC_EXPECIONAL']] \
                      .drop_duplicates(subset = ["INTERNOEN"])
        data_people = data_people.reset_index(drop=True)
        data_people['CONDIC_EXPECIONAL'] = data_people['CONDIC_EXPECIONAL'].fillna('NINGUNO')
        
        etnic_recognition = self.queries.run('etl_select_1')
        data_people['reconocimiento_etnico'] = 'NINGUNO'
        for i in etnic_recognition.index:
            data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains(etnic_recognition['nombre'].values[i])),
                            'reconocimiento_etnico'] =  etnic_recognition['nombre'].values[i]
            
        ############## foreign
        data_people['extranjero'] = 'N'
        data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains('EXTRANJEROS')),'extranjero'] =  'S'
        
        ############## sexual diversity
        sexual_dive = self.queries.run('etl_select_2')
        data_people['diversidad_sexual'] = 'N'
        for i in sexual_dive.index:
            data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains(sexual_dive['nombre'].values[i])),
                            'diversidad_sexual'] =  'S'
    
        personas_genero = self.queries.run('etl_select_3')
        for i in personas_genero.index:
            for j in sexual_dive.index:
                if sexual_dive['nombre'].values[j] in personas_genero['condicion_exepcional'].values[i]:
                    query = str(personas_genero['id_persona'].values[i]) + ', ' \
                                + str(sexual_dive['id_diversidad_sexual'].values[j])
                    self.queries.insert('INSERT INTO public.persona_diversidad_sexual (id_persona, id_diversidad_sexual) VALUES('+query+');')
        
        ############## people
        data_people.to_sql('personas_tmp', con=self.queries.engine)
        self.queries.run('etl_select_4')
        self.queries.run('etl_select_5')
        
    def inmate_variable_info(self, data):
        data_reg= data[['INTERNOEN', 'GENERO','DELITO','ESTADO_INGRESO','FECHA_CAPTURA',
                        'FECHA_INGRESO','ESTABLECIMIENTO','TENTATIVA','SUBTITULO_DELITO',
                        'AGRAVADO', 'CALIFICADO','FECHA_SALIDA','EDAD','DEPARTAMENTO', 'CIUDAD',
                        'ACTIVIDADES_TRABAJO', 'ACTIVIDADES_ESTUDIO', 'ACTIVIDADES_ENSEÑANZA',
                        'HIJOS_MENORES', 'CONDIC_EXPECIONAL','ESTADO','SITUACION_JURIDICA']]
        
        ############## No exceptional condition
        data_reg['CONDIC_EXPECIONAL'] = data_reg['CONDIC_EXPECIONAL'].fillna('NINGUNO')

        ############## Madre Gestantes
        data_reg['madre_gestante'] = 'NA'
        data_reg.loc[(data_reg['GENERO'].str.contains('FEMENINO')),'madre_gestante'] = 'N'
        data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('MADRE GESTANTE')),'madre_gestante'] =  'S'

        data_reg['madre_lactante'] = 'NA'
        data_reg.loc[(data_reg['GENERO'].str.contains('FEMENINO')),'madre_lactante'] = 'N'
        data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('MADRE LACTANTE')),'madre_lactante'] =  'S'

        ############## Discapacitad
        data_reg['discapacidad'] = 'N'
        data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('CON DISCAPACIDAD')),'discapacidad'] =  'S'

        ############## Adulto Mayor
        data_reg['adulto_mayor'] = 'N'
        data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('ADULTO MAYOR')),'adulto_mayor'] =  'S'
        
        #severity index

        # Count number of observations by crime type and category
        top10 = list(data_reg['DELITO'].value_counts().to_frame() \
                     .reset_index().rename(columns = {'index':'DELITONAME'}).head(10)['DELITONAME'])
        #https://leyes.co/codigo_penal.htm
        #values as [min_month,max_month,decree]
        dict_pena ={'HURTO': [16,108,239],
                    'TRAFICO FABRICACION O PORTE DE ESTUPEFACIENTES': [128,360,376],
                    'FABRICACION TRAFICO Y PORTE DE ARMAS DE FUEGO O MUNICIONES':[132,180,366],
                    'CONCIERTO PARA DELINQUIR':[48,108,340],
                    'HOMICIDIO':[208,450,103],
                    'EXTORSION':[192,288,244],
                    'FABRICACIÓN, TRÁFICO, PORTE O TENENCIA DE ARMAS DE FUEGO, ACCESORIOS, PARTES O MUNICIONES':[108,144,365],
                    'VIOLENCIA INTRAFAMILIAR':[48,720,229],
                    'LESIONES PERSONALES':[16,360,[111,112,113,114,115,116,117,118,119,120,121]],
                    'FABRICACION  TRAFICO Y PORTE DE ARMAS Y MUNICIONES DE USO PRIVATIVO DE LAS FUERZAS ARMADAS':[132,180,366]
                    }
        df_severity = pd.DataFrame(dict_pena)
        df_severity_t = df_severity.transpose().reset_index()
        col_names=['crime','min_month','max_month','decree']
        df_severity_t.columns = col_names
        crime_score = {'HURTO':1,
                       'TRAFICO FABRICACION O PORTE DE ESTUPEFACIENTES':7,
                       'FABRICACION TRAFICO Y PORTE DE ARMAS DE FUEGO O MUNICIONES':4,
                       'CONCIERTO PARA DELINQUIR':2,
                       'HOMICIDIO':9, 
                       'EXTORSION':6,
                       'FABRICACIÓN, TRÁFICO, PORTE O TENENCIA DE ARMAS DE FUEGO, ACCESORIOS, PARTES O MUNICIONES':3,
                       'VIOLENCIA INTRAFAMILIAR':10,
                       'LESIONES PERSONALES':8,
                       'FABRICACION  TRAFICO Y PORTE DE ARMAS Y MUNICIONES DE USO PRIVATIVO DE LAS FUERZAS ARMADAS':5
                      }
        data_reg['crime_score'] = data_reg['DELITO'].apply(lambda x: crime_score[x] if x in top10 else 0)
        display(df_severity_t,data_reg.head(1))
        #Calificado,Agravado,tentativa
        CAT_cases = data_reg[['TENTATIVA','AGRAVADO', 'CALIFICADO']].drop_duplicates().reset_index(drop=True)
        CAT_cases['multiplier']= 'TBD'
        CAT_cases.loc[5,'multiplier'] = 1  # TENTATIVA
        CAT_cases.loc[0,'multiplier'] = 2    # CONSUMADO
        CAT_cases.loc[4,'multiplier'] = 3 # TENTATIVA-AGRAVADO
        CAT_cases.loc[7,'multiplier'] = 4  # TENTATIVA-CALIFICADO
        CAT_cases.loc[6,'multiplier'] = 5 # TENTATIVA-CALIFICADO-AGRAVADO
        CAT_cases.loc[3,'multiplier'] = 6    # CONSUMADO-AGRAVADO
        CAT_cases.loc[2,'multiplier'] = 7    # CONSUMADO-CALIFICADO
        CAT_cases.loc[1,'multiplier'] = 8    # CONSUMADO-CALIFICADO-AGRAVADO
        display(CAT_cases)
        # Feature engineering
        # Generate score
        data_reg['CONSUMADO_b']  = data_reg.TENTATIVA.apply(lambda x: 4 if x=="N" else 0)
        data_reg['TENTATIVA_b'] = data_reg.TENTATIVA.apply(lambda x: 3 if x=="S" else 0)
        data_reg['CALIFICADO_b'] = data_reg.CALIFICADO.apply(lambda x: 2 if x=="S" else 0)
        data_reg['AGRAVADO_b']  = data_reg['AGRAVADO'].apply(lambda x: 1 if x=="S" else 0)
        # Multiplier score
        data_reg['crime_multiplier'] = (data_reg['CONSUMADO_b'] + data_reg['TENTATIVA_b'] + data_reg['CALIFICADO_b'] + data_reg['AGRAVADO_b'])/7
        # Severity 
        data_reg['severity'] = data_reg['crime_score']*data_reg['crime_multiplier']

        ############## registro
        data_reg.to_sql('registros_tmp', con=self.queries.engine)
        #self.queries.run('select * from registros_tmp limit 5')
        self.queries.run('etl_select_6')








