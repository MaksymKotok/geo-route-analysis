import shutil
import os

BASE_DIR = 'backup/'

if __name__ == '__main__':
    db_files = []
    
    for subdir, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(('.sqlite', '.sqlite3', '.db', '.db3', '.s3db', '.sl3')):
                print(os.path.join(subdir, file))
                try:
                    shutil.copyfile(os.path.join(subdir, file), os.path.join("data/", file))
                except:
                    continue
