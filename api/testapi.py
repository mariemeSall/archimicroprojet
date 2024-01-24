from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List
import uvicorn
import psycopg2
from psycopg2 import sql

app = FastAPI()

def connect_to_db():
    dbname = "coords"
    user = "root"
    password = "password"
    host = "localhost"
    port = "5432"
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection

def retrieve_all_rows():
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            select_query = sql.SQL("""
                SELECT * FROM coordonnee
            """)
            cursor.execute(select_query)

            rows = cursor.fetchall()

            return rows

    finally:
        connection.close()

# Templates configuration
templates = Jinja2Templates(directory="templates")

geolocation_data = []

@app.get("/update_location/")
async def update_location(request: Request):
    global geolocation_data
    coords = retrieve_all_rows()
    geolocation_data = [
                {"lat": row[1], "long": row[2], "ip": row[3], "date": str(row[4])} for row in coords]
    print(f'geodata: {geolocation_data}')
    return {"geolocation_data": geolocation_data}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "coords": geolocation_data})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)