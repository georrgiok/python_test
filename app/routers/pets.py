from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import database
from models import database as mdb, controller as mct

router = APIRouter(
    prefix="/pets",
    tags=['pets']
)


@router.get('/', response_model=list[mct.Pet])
async def get_pets(limit: int = 5, offset: int = 0, db: Session = Depends(database.get_db)):
    return db.query(mdb.Pet).limit(limit).offset(offset)


@router.post('/', response_model=mct.Pet)
async def post_pets(pet: mct.BasePet, db: Session = Depends(database.get_db)):
    animal = mdb.Pet(client_id=pet.client_id, name=pet.name, birthday=pet.birthday)
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


@router.put('/', response_model=mct.Pet)
async def put_pet(pet: mct.Pet, db: Session = Depends(database.get_db)):
    animal: mdb.Pet = db.query(mdb.Pet).filter(mdb.Pet.pet_id == pet.pet_id).first()
    if not animal:
        return JSONResponse(status_code=404, content={"message": "Питомец не найден"})
    animal.name = pet.name
    animal.birthday = pet.birthday
    animal.client_id = pet.client_id
    db.commit()
    db.refresh(animal)
    return animal


@router.delete('/{pet_id}', response_model=mct.Pet)
async def delete_pet(pet_id: int, db: Session = Depends(database.get_db)):
    pet: mdb.Pet = db.query(mdb.Pet).filter(mdb.Pet.pet_id == pet_id).first()
    if not pet:
        return JSONResponse(status_code=404, content={"message": "Питомец не найден"})
    db.delete(pet)
    db.commit()
    return pet


@router.get('/{pet_id}', response_model=mct.Pet)
async def get_pet(pet_id: int, db: Session = Depends(database.get_db)):
    pet: mdb.Pet = db.query(mdb.Pet).filter(mdb.Pet.pet_id == pet_id).first()
    if not pet:
        return JSONResponse(status_code=404, content={"message": "Питомец не найден"})
    return pet
