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
        self.query_dict = {'encoding'    :"""select * from persona 
                                             left join registro 
                                             on persona.id_persona = registro.persona_id_persona 
                                             left join delito 
                                             on delito.id_delito = registro.delito_id_delito""",
                           
                           'etl_select_1':"""select * from reconocimiento_etnico""",
                           'etl_select_2':"""select * from diversidad_sexual""",
                           'etl_select_3':"""select * from persona where diversidad_sexual = 2""",
                           
                           'etl_insert_1':"""INSERT INTO public.persona_diversidad_sexual 
                                             (id_persona, id_diversidad_sexual) VALUES({});""",
                           
                           'etl_select_4':"""select * from personas_tmp limit 5""",
                           'etl_select_5':"""select public.tcompararpersonas();""",
                           'etl_select_6':"""select public.tcompararreg();""",
                           'etl_select_7':"""select * from departamento""",
                           
                           'people_query':"""select id_persona as id_people, 
                                                    ne.name_eng_group as "education level", 
                                                    n.pais as "origen country",
                                                    g.name_eng as gender,
                                                    2020-anio_nacimiento as "actual age" ,
                                                    1 as people from persona p 
                                             left join (select *, 
                                                        case when id_nivel_educativo in (6,7,8,9,10,11,12) 
                                                        then 'Higher education'
                                                        else name_eng end as name_eng_group from nivel_educativo) ne 
                                             on p.nivel_educativo = ne.id_nivel_educativo
                                             left join nacionalidad n 
                                             on n.id_pais = p.nacionalidad
                                             left join genero g 
                                             on p.genero = g.id_genero""",
                           
                           'etl_select_8':"""select * from registro
                                             left join (select id_establecimiento, municipio from establecimiento) e
                                             on registro.establecimiento = e.id_establecimiento 
                                             left join (select id_municipio, 
                                                               departamento, 
                                                               nombre as mun_name from municipio) m 
                                             on e.municipio = m.id_municipio  
                                             left join departamento 
                                             on m.departamento = departamento.id_departamento """}
    
    def run(self, sql):
        result = self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(self.query_dict[sql])))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    
    def insert(self, sql):
        return self.engine.connect().execution_options(isolation_level="AUTOCOMMIT")\
                .execute((text(sql)))