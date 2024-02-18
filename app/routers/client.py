from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import database
from models import database as mdb, controller as mct

router = APIRouter(
    prefix="/clients",
    tags=['clients']
)


@router.get('/', response_model=list[mct.Client])
async def get_clients(limit: int = 5, offset: int = 0, db: Session = Depends(database.get_db)):
    return db.query(mdb.Client).limit(limit).offset(offset)


@router.post('/', response_model=mct.Client)
async def post_clients(client: mct.BaseClient, db: Session = Depends(database.get_db)):
    person = mdb.Client(document=client.document, first_name=client.first_name, last_name=client.last_name,
                        patronymic=client.patronymic, birthday=client.birthday)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.put('/', response_model=mct.Client)
async def put_clients(client: mct.Client, db: Session = Depends(database.get_db)):
    person: mdb.Client = db.query(mdb.Client).filter(mdb.Client.client_id == client.client_id).first()
    if not person:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    person.document = client.document
    person.first_name = client.first_name
    person.last_name = client.last_name
    person.patronymic = client.patronymic
    person.birthday = client.birthday
    db.commit()
    db.refresh(person)
    return person


@router.delete('/{client_id}', response_model=mct.Client)
async def delete_client(client_id: int, db: Session = Depends(database.get_db)):
    client: mdb.Client = db.query(mdb.Client).filter(mdb.Client.client_id == client_id).first()
    if not client:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    db.delete(client)
    db.commit()
    return client


@router.get('/{client_id}', response_model=mct.Client)
async def get_client(client_id: int, db: Session = Depends(database.get_db)):
    client: mdb.Client = db.query(mdb.Client).filter(mdb.Client.client_id == client_id).first()
    if not client:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return client
