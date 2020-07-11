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
        
        etnic_recognition = self.queries.run("""select * from reconocimiento_etnico""")
        data_people['reconocimiento_etnico'] = 'NINGUNO'
        for i in etnic_recognition.index:
            data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains(etnic_recognition['nombre'].values[i])),
                            'reconocimiento_etnico'] =  etnic_recognition['nombre'].values[i]
            
        ############## foreign
        data_people['extranjero'] = 'N'
        data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains('EXTRANJEROS')),'extranjero'] =  'S'
        
        ############## sexual diversity
        sexual_dive = self.queries.run("""select * from diversidad_sexual""")
        data_people['diversidad_sexual'] = 'N'
        for i in sexual_dive.index:
            data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains(sexual_dive['nombre'].values[i])),
                            'diversidad_sexual'] =  'S'
    
        personas_genero = self.queries.run("""select * from persona where diversidad_sexual = 2""")
        for i in personas_genero.index:
            for j in sexual_dive.index:
                if sexual_dive['nombre'].values[j] in personas_genero['condicion_exepcional'].values[i]:
                    query = str(personas_genero['id_persona'].values[i]) + ', ' \
                                + str(sexual_dive['id_diversidad_sexual'].values[j])
                    self.queries.insert('INSERT INTO public.persona_diversidad_sexual (id_persona, id_diversidad_sexual) VALUES('+query+');')
        
        ############## people
        data_people.to_sql('personas_tmp', con=self.queries.engine)
        self.queries.run('select * from personas_tmp limit 5')
        self.queries.run('SELECT public.tcompararpersonas();')
        
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
        
        ############## registro
        data_reg.to_sql('registros_tmp', con=self.queries.engine)
        self.queries.run('select * from registros_tmp limit 5')
        self.queries.run('SELECT public.tcompararreg();')