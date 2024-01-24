import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2 import sql

app = FastAPI()

class Coord(BaseModel):
    lat: float
    long: float
    ip: str
    date: str

def connect_to_db():
    dbname = "coords"
    user = "root"
    password = "password"
    host = "localhost"
    port = "5432"
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection


@app.post("/push_to_db")
def push_to_db(coord: Coord):
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO coordonnee (longitude, latitude, date, ip)
                VALUES (%s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (coord.long, coord.lat, coord.date, coord.ip))

        connection.commit()

    finally:
        connection.close()
    return {"status": "Message pushed to the database successfully"}

@app.get("/retrieve_all_rows")
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

@app.delete("/clear_from_db")
def clear_from_db():
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            delete_query = sql.SQL("""
                DELETE FROM coordonnee
            """)
            cursor.execute(delete_query)

        connection.commit()

    finally:
        connection.close()
    
    return {"status": "All rows cleared from the database"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
