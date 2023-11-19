import os
import sqlite3
import pickle
import json


BASE_DIR = 'backup/'

if __name__ == '__main__':
    db_files = []
    
    for subdir, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(('.sqlite', '.sqlite3', '.db', '.db3', '.s3db', '.sl3')):
                db_files.append(os.path.join(subdir, file))
                
    print(len(db_files))
    
    db_files = db_files
    
    metadata = dict()
    k = 0
    
    for db_file in db_files:
        print(db_file)
        k += 1
        db = dict()
        try:
            with sqlite3.connect(db_file) as conn:
                tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                for table in tables:
                    table = table[0]
                    print(f"\n\nTABLE: {table}")
                    
                    db[table] = []
                    
                    data = conn.execute(f"SELECT * FROM {table};")
                    for col in data.description:
                        print(col[0])
                        db[table].append(col[0])
                        
                    # for row in data:
                    #     print(row)
        except:
            continue
        finally:
            metadata[db_file] = db
            print(metadata)
            print(k)
        
        with open('metadata.json', 'w+') as f:
            f.write(json.dumps(metadata, indent=4))
