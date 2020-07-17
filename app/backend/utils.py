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
                           'etl_select_1': """select * from reconocimiento_etnico""",
                           'etl_select_2': """select * from diversidad_sexual""",
                           'etl_select_3': """select * from persona where diversidad_sexual = 2""",
                           'etl_insert_1':'INSERT INTO public.persona_diversidad_sexual (id_persona, id_diversidad_sexual) VALUES({});',
                           'etl_select_4':'select * from personas_tmp limit 5',
                           'etl_select_5': 'SELECT public.tcompararpersonas();',
                           'etl_select_6': 'SELECT public.tcompararreg();',
                           'etl_select_7':'select * from departamento'}
    
    def run(self, sql):
        result = self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(self.query_dict[sql])))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    
    def insert(self, sql):
        return self.engine.connect().execution_options(isolation_level="AUTOCOMMIT")\
                .execute((text(sql)))