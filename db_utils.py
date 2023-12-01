import sqlite3
import pandas as pd
import sqlalchemy


def df_from_db(file_db: str) -> pd.DataFrame:
    with sqlite3.connect(file_db) as conn:
        table = "location"
        query = f"SELECT * FROM {table};"

        df = pd.read_sql_query(query, conn)
        df.columns = ('INDEX', 'LATITUDE', 'LONGITUDE', 'DATETIME')
        df['DATETIME'].apply(lambda d: pd.to_datetime(d))
        df = df.dropna()

        df.set_index('DATETIME', inplace=True)
    return df


# if __name__ == '__main__':
    # file_db = 'data/266.sqlite'

    # with sqlite3.connect(file_db) as conn:
    #     table = "ZFAVORITE"
    #     query = f"SELECT * FROM {table};"

    #     df = pd.read_sql_query(query, conn)
    #     df = df[["Z_PK", "ZLAT", "ZLON"]]
    #     df = df.dropna()
        
    #     file_csv = file_db[file_db.rfind("/") + 1 : file_db.rfind(".")] + ".csv"
    #     df.to_csv(f"csv/{file_csv}", index=False)
    
    # df = df_from_db('db/bolt.db')
