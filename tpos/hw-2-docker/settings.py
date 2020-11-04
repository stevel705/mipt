import os
from starlette.config import Config
base_dir = os.path.relpath(os.path.dirname(__file__))
env_path = os.path.join(base_dir, ".env")
config = Config(env_path)

from sqlalchemy import Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class HomeTable(Base):
    __tablename__ = 'hometable'
    word = Column(String, primary_key=True)
    number = Column(Integer)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class PostgresConfiguration:
    POSTGRES_USER = config("POSTGRES_USER", default="postgres")
    POSTGRES_DB_PASSWORD = config("POSTGRES_DB_PASSWORD", default="postgres")
    POSTGRES_DB_HOST = config("POSTGRES_DB_HOST", default="db")
    POSTGRES_DB_NAME = config("POSTGRES_DB_NAME", default="postgres")
    POSTGRES_DB_PORT = config("POSTGRES_DB_PORT", default="5432")

    @property
    def postgres_db_path(self):
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_DB_PASSWORD}@' \
               f'{self.POSTGRES_DB_HOST}:' \
               f'{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}'