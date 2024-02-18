from fastapi import FastAPI, Body, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import client, pets
from models import controller as mct
from sqlalchemy.orm import Session
from database import database

app = FastAPI(
    title="Vet Clinic"
)
app.include_router(client.router)
app.include_router(pets.router)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
async def root():
    return FileResponse('static/index.html')


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello/{name}")
async def post_hello(name: str, body=Body(None)):
    print(body)
    if type(body) != str:
        naming = body.get('data')
    else:
        naming = body
    return {"message": f"Hello {naming} from {name}"}


@app.post('/fill', response_model=mct.BaseResponse)
async def fill_db(body: mct.BaseTarget, db: Session = Depends(database.get_db)):
    target = body.target
    match target:
        case target.pets:
            database.create_new_pets(db)
            return {"message": "Created Pets"}
        case target.clients:
            database.create_new_clients(db)
            return {"message": "Created Clients"}
        case _:
            return {"message": "Hello World"}
