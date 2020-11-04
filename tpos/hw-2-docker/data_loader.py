import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, MetaData
from settings import PostgresConfiguration, HomeTable
from sqlalchemy.orm import sessionmaker

pg = PostgresConfiguration()
engine = create_engine(pg.postgres_db_path)
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv("data/data.csv",header=None, names=['word', 'number'])
df.to_sql('hometable', engine, if_exists='replace')
print("Recorded csv to table in postgre........")

# SELECT * FROM TABLE;
rows = session.query(HomeTable).all()

if not rows:
    print("DATA IS NOT EXIST")

else:
    print("=========================== Print data ===========================")
    for row in rows:
        print(row.word, row.number)
    print("=========================== Data is exist ===========================")