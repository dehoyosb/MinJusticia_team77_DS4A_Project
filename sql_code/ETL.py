# import packages to read and transfer data
import pandas as pd
import string
import os

from sqlalchemy import create_engine, text

# create engine to conect database in docker 
pd.options.display.max_rows = 20
engine = create_engine('postgresql://team77:mintic2020.@postgres/minjusticia', max_overflow=20)
def runQuery(sql):
    result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())


# create the required table only for people
data_people = data[['INTERNOEN', 'GENERO', 'PAIS_INTERNO', 'REINCIDENTE', 'ANO_NACIMIENTO', 
                        'ESTADO_CIVIL','NIVEL_EDUCATIVO']].drop_duplicates(subset = ["INTERNOEN"])
data_people = data_people.reset_index(drop=True)
data_people.to_sql('personas_tmp', con=engine)

# insert data on temp table for the procedure
runQuery('select * from personas_tmp')

# run procedure to normalize the data and insert in the columns
runQuery('SELECT public.tcompararpersonas();')




# create the required table for the reg table

data_reg= data[['INTERNOEN', 'DELITO','ESTADO_INGRESO','FECHA_CAPTURA',
                'FECHA_INGRESO','ESTABLECIMIENTO','TENTATIVA',
       'AGRAVADO', 'CALIFICADO','FECHA_SALIDA','EDAD','DEPARTAMENTO', 'CIUDAD','ACTIVIDADES_TRABAJO',
       'ACTIVIDADES_ESTUDIO', 'ACTIVIDADES_ENSEÑANZA','HIJOS_MENORES', 'CONDIC_EXPECIONAL','ESTADO','SITUACION_JURIDICA']]
data_reg


# insert data on temp table for the procedure
data_reg.to_sql('registros_tmp', con=engine)

# run procedure to normalize the data and insert in the columns
runQuery('SELECT public.tcompararreg();')




# check all ok
print('Count of data in the people table' )
print(runQuery('select count(*) from persona')

print('Count of data in the registry table' )
print(runQuery('select count(*) from registro')