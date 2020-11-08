import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, MetaData
from settings import PostgresConfiguration, HomeTable
from sqlalchemy.orm import sessionmaker

# Connecting to the database
pg = PostgresConfiguration()
engine = create_engine(pg.postgres_db_path)
Session = sessionmaker(bind=engine)
session = Session()

def identify_header(path, n=5, th=0.9):
    df1 = pd.read_csv(path, header='infer', nrows=n)
    df2 = pd.read_csv(path, header=None, nrows=n)
    sim = (df1.dtypes.values == df2.dtypes.values).mean()
    return 1 if sim < th else 0

path_data = "data/data.csv"
skiprow = identify_header(path_data) # check header on csv file and skip row if need 

# Read csv and write to database's table. If exists, then replace 
df = pd.read_csv(path_data,header=None, names=['word', 'number'], skiprows=skiprow)
print(df)
df.to_sql('hometable', engine, if_exists='replace')
print("Recorded csv to table in postgre........")

# SELECT * FROM TABLE;
rows = session.query(HomeTable).all()

# Check data in table
if not rows:
    print("DATA IS NOT EXIST")

else:
    print("=========================== Print data ===========================")
    for row in rows:
        print(row.word, row.number)
    print("=========================== Data is exist ===========================")