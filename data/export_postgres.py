"""export postgres database to CSV
"""
from sqlalchemy import create_engine
import pandas as pd

cstring = r'postgres://flask:nomoresecrets@localhost:5432/spider'
engine = create_engine(cstring)

tables = ['network', 'edge', 'node']
for table in tables:
    sql = f"SELECT * FROM {table}"
    df = pd.read_sql(sql, engine)
    df.to_csv(f"{table}.csv", index=False)