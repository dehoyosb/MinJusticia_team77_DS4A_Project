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

def insertQuery(sql):
    result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return 1

# data reading from excel
data = pd.read_excel('data/ReincidenciaPospenadosNal201011Junio2020Rev.xlsx', skiprows = 6)





# create the required table only for people
data_people = data[['INTERNOEN', 'GENERO', 'PAIS_INTERNO', 'REINCIDENTE', 'ANO_NACIMIENTO', 
                        'ESTADO_CIVIL','NIVEL_EDUCATIVO', 'CONDIC_EXPECIONAL']].drop_duplicates(subset = ["INTERNOEN"])
data_people = data_people.reset_index(drop=True)

# create variables from execptional conditions

############## etnic reconnition
data_people['CONDIC_EXPECIONAL'] = data_people['CONDIC_EXPECIONAL'].fillna('NINGUNO')
etnic_recognition = runQuery("""select * from reconocimiento_etnico""")
data_people['reconocimiento_etnico'] = 'NINGUNO'
for i in etnic_recognition.index:
    data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains(etnic_recognition['nombre'].values[i])),'reconocimiento_etnico'] =  etnic_recognition['nombre'].values[i]
#data_people[~(data_people['reconocimiento_etnico'] == 'NINGUNO')]['reconocimiento_etnico']

############## foreign

data_people['extranjero'] = 'N'
data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains('EXTRANJEROS')),'extranjero'] =  'S'
data_people['CONDIC_EXPECIONAL']
#data_people[~(data_people['extranjero'] == 'N')]['extranjero']

############## sexual diversity
sexual_dive = runQuery("""select * from diversidad_sexual""")
sexual_dive
data_people['diversidad_sexual'] = 'N'
for i in sexual_dive.index:
    data_people.loc[(data_people['CONDIC_EXPECIONAL'].str.contains(sexual_dive['nombre'].values[i])),'diversidad_sexual'] =  'S'

data_people[~(data_people['diversidad_sexual'] == 'N')]['diversidad_sexual']


# insert data on temp table for the procedure
data_people.to_sql('personas_tmp', con=engine)
runQuery('select * from personas_tmp')

# run procedure to normalize the data and insert in the columns
runQuery('SELECT public.tcompararpersonas();')


################################################################################
#############

# insert sexual diversity variables in the adecuate table
############## sexual diversity
personas_genero = runQuery("""select * from persona where diversidad_sexual = 2""")
personas_genero
for i in personas_genero.index:
    for j in sexual_dive.index:
        if sexual_dive['nombre'].values[j] in personas_genero['condicion_exepcional'].values[i]:
            query = str(personas_genero['id_persona'].values[i])+', '+str(sexual_dive['id_diversidad_sexual'].values[j])
            insertQuery('INSERT INTO public.persona_diversidad_sexual (id_persona, id_diversidad_sexual) VALUES('+query+');')



 #####################################################################################################
 #####################################################################################################
 #####################################################################################################



# create the required table for the reg table

data_reg= data[['INTERNOEN', 'GENERO','DELITO','ESTADO_INGRESO','FECHA_CAPTURA',
                'FECHA_INGRESO','ESTABLECIMIENTO','TENTATIVA',
       'AGRAVADO', 'CALIFICADO','FECHA_SALIDA','EDAD','DEPARTAMENTO', 'CIUDAD','ACTIVIDADES_TRABAJO',
       'ACTIVIDADES_ESTUDIO', 'ACTIVIDADES_ENSEÑANZA','HIJOS_MENORES', 'CONDIC_EXPECIONAL','ESTADO','SITUACION_JURIDICA']]
data_reg

# create variables for exceptional conditions

data_reg['CONDIC_EXPECIONAL'] = data_reg['CONDIC_EXPECIONAL'].fillna('NINGUNO')

data_reg['madre_gestante'] = 'NA'
data_reg.loc[(data_reg['GENERO'].str.contains('FEMENINO')),'madre_gestante'] = 'N'
data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('MADRE GESTANTE')),'madre_gestante'] =  'S'
#data_reg['CONDIC_EXPECIONAL']
#data_reg[~(data_reg['madre_gestante'] == 'NA')]['madre_gestante']

data_reg['madre_lactante'] = 'NA'
data_reg.loc[(data_reg['GENERO'].str.contains('FEMENINO')),'madre_lactante'] = 'N'
data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('MADRE LACTANTE')),'madre_lactante'] =  'S'
#data_reg['CONDIC_EXPECIONAL']
#data_reg[~(data_reg['madre_lactante'] == 'NA')]['madre_lactante']
    

data_reg['discapacidad'] = 'N'
data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('CON DISCAPACIDAD')),'discapacidad'] =  'S'
#data_reg['CONDIC_EXPECIONAL']
#data_reg[~(data_reg['discapacidad'] == 'N')]['discapacidad']



data_reg['adulto_mayor'] = 'N'
data_reg.loc[(data_reg['CONDIC_EXPECIONAL'].str.contains('ADULTO MAYOR')),'adulto_mayor'] =  'S'
#data_reg['CONDIC_EXPECIONAL']
data_reg[~(data_reg['adulto_mayor'] == 'N')]['adulto_mayor']



# insert data on temp table for the procedure
data_reg.to_sql('registros_tmp', con=engine)

# run procedure to normalize the data and insert in the columns
runQuery('SELECT public.tcompararreg();')




# check all ok
#print('Count of data in the people table' )
#print(runQuery('select count(*) from persona')

#print('Count of data in the registry table' )
#print(runQuery('select count(*) from registro')