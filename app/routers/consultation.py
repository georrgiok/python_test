from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import database
from models import database as mdb, controller as mct

router = APIRouter(
    prefix="/appointment",
    tags=['appointment']
)


@router.get('/', response_model=list(mct.Consultation))
async def get_appointments(limit: int = 5, offset: int = 0, db: Session = Depends(database.get_db)):
    return db.query(mdb.Consultation).limit(limit).offset(offset)


@router.post('/', response_model=mct.Consultation)
async def post_appointments(appointment: mct.BaseConsultation, db: Session = Depends(database.get_db)):
    consultation = mdb.Consultation(client_id=appointment.client_id, pet_id=appointment.pet_id, date=appointment.date,
                                    description=appointment.description)
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return consultation


@router.put('/', response_model=mct.Consultation)
async def put_appointment(appointment: mct.Consultation, db: Session = Depends(database.get_db)):
    consultation: mdb.Consultation = db.query(mdb.Consultation).filter(
        mdb.Consultation.consultation_id == appointment.consultation_id).first()
    if not consultation:
        return JSONResponse(status_code=404, content={"message": "Консультация не найдена"})
    consultation.client_id = appointment.client_id
    consultation.pet_id = appointment.pet_id
    consultation.date = appointment.date
    consultation.description = appointment.description
    db.commit()
    db.refresh(consultation)
    return consultation


@router.delete('/{consultation_id}', response_model=mct.Client)
async def delete_client(consultation_id: int, db: Session = Depends(database.get_db)):
    consultation: mdb.Consultation = db.query(mdb.Consultation).filter(
        mdb.Consultation.consultation_id == consultation_id).first()
    if not consultation:
        return JSONResponse(status_code=404, content={"message": "Консультация не найдена"})
    db.delete(consultation)
    db.commit()
    return consultation


@router.get('/{consultation_id}', response_model=mct.Client)
async def get_client(consultation_id: int, db: Session = Depends(database.get_db)):
    consultation: mdb.Consultation = db.query(mdb.Consultation).filter(
        mdb.Consultation.consultation_id == consultation_id).first()
    if not consultation:
        return JSONResponse(status_code=404, content={"message": "Консультация не найдена"})
    return consultation