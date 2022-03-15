"""Create sqlite database from test data
"""
from sqlalchemy import create_engine
import pandas as pd

cstring = r'sqlite:///spider.db'
engine = create_engine(cstring)

tables = ['network', 'edge', 'node']
for table in tables:
    df = pd.read_csv(f"{table}.csv")
    df.to_sql(table, engine, if_exists='replace')