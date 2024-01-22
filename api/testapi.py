from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List
import uvicorn

app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory="templates")

geolocation_data = []

@app.post("/update_location/")
async def update_location(request: Request):
    global geolocation_data
    coords = await request.json()
    geolocation_data = coords.get("geolocation_data", [])
    print(f'geodata: {geolocation_data}')
    return {"geolocation_data": geolocation_data}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "coords": geolocation_data})

@app.get("/geolocation_data", response_class=JSONResponse)
async def get_geolocation_data():
    global geolocation_data
    return {"geolocation_data": geolocation_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)