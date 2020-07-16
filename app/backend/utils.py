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
                                        left join delito on delito.id_delito = registro.delito_id_delito'}
    
    def run(self, sql):
        result = self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(self.query_dict[sql])))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    
    def insert(self, sql):
        return self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(self.query_dict[sql])))