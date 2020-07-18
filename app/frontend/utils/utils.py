#Packages:
import pandas as pd
import string
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

class DbEngine():
    def __init__(self, user, password, ip, port, db):
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        self.db = db
    
    def connect(self):
        return create_engine('postgresql://{}:{}@{}:{}/{}' \
                                .format(self.user, 
                                        self.password,
                                        self.ip,
                                        self.port,
                                        self.db), max_overflow=20)

class Queries():
    def __init__(self, engine):
        self.engine = engine
        self.query_dict = {'encoding': 'select * from persona \
                                        left join registro on persona.id_persona = registro.persona_id_persona \
                                        left join delito on delito.id_delito = registro.delito_id_delito',
                            'people_query' : """select id_persona as id_people, 
                            ne.name_eng_group as "education level", 
                            n.pais as "origen country",
                            g.name_eng as gender,
                            2020-anio_nacimiento as "actual age" ,
                            1 as people,
                            munic.departamento,
                            reg.establecimiento,
                            reg.fecha_ingreso,
                            reg.delito_id_delito,
                            p.genero,
                            case when reg.condicion_excepcional like 'NINGUNO' then 1 else 2 end as condicion_excepcional
                            from persona p 
                        left join (select *, case when id_nivel_educativo in (6,7,8,9,10,11,12) then 'Higher education'
                    else name_eng end as name_eng_group from nivel_educativo) ne on p.nivel_educativo = ne.id_nivel_educativo
                        left join nacionalidad n on n.id_pais = p.nacionalidad
                        left join genero g on p.genero = g.id_genero
                        left join (select distinct on (persona_id_persona) * from registro) reg on reg.persona_id_persona= p.id_persona
                        left join public.establecimiento est on est.id_establecimiento = reg.establecimiento
                        left join public.municipio munic on est.municipio= munic.id_municipio""",

                        'crime_filter': 'select id_delito, nombre, name_eng from delito',
                        'reclusion_dept' : 'select id_departamento, nombre from public.departamento',
                        'reclusion_entity' : 'select id_establecimiento,est.nombre, departamento from public.establecimiento est left join public.municipio munic on est.municipio = munic.id_municipio'}
    
    def run(self, sql):
        result = self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(self.query_dict[sql])))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    
    def insert(self, sql):
        return self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(self.query_dict[sql])))