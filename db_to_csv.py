import sqlite3
import pandas as pd
import sqlalchemy


file_db = 'data/266.sqlite'

with sqlite3.connect(file_db) as conn:
    table = "ZFAVORITE"
    query = f"SELECT * FROM {table};"

    df = pd.read_sql_query(query, conn)
    df = df[["Z_PK", "ZLAT", "ZLON"]]
    df = df.dropna()
    
    file_csv = file_db[file_db.rfind("/") + 1 : file_db.rfind(".")] + ".csv"
    df.to_csv(f"csv/{file_csv}", index=False)
