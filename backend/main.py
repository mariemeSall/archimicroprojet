from fastapi import FastAPI
from datetime import datetime
from api.routeur import router as api_routeur
from fastapi_sqlalchemy import DBSessionMiddleware, db
from BDD.models import Coordonnee
from BDD.schema import Coordonnee  as Model_coordonnee

import os
from dotenv import load_dotenv

date_format = '%Y-%m-%d %H:%M:%S'

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])
app.include_router(api_routeur)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/coordonnees/{ip}')
async def get_coordonnees(ip):
    coor = db.session.query(Coordonnee).filter(Coordonnee.ip == ip).all()
    return coor

@app.post('/coordonnees')
async def add_coordonnees(coor: Model_coordonnee):
    db_coor = Coordonnee(latitude = coor.latitude, longitude = coor.longitude, ip = coor.ip, date = datetime.strptime("2024-01-17 17:08:0", date_format))
    db.session.add(db_coor)
    db.session.commit()
    return True