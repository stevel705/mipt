from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import json 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import PostgresConfiguration, HomeTable

app = FastAPI()

pg = PostgresConfiguration()
engine = create_engine(pg.postgres_db_path)

Session = sessionmaker(bind=engine)
session = Session()

from starlette.exceptions import HTTPException as StarletteHTTPException
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    # return RedirectResponse("/")  
    return JSONResponse({"message": "Something went wrong"}, status_code=400)

from sqlalchemy import select

@app.get('/')
def get_all_items():
    """Возвращает данные из БД в виде JSON """ 
    rows = session.query(HomeTable).all()
    return [ix.as_dict() for ix in rows]


@app.get('/health')
def hello():
    """Test endpoint""" 
    return {'status': 200}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)