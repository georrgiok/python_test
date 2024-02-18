from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import database
from .initial import data, utils

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

Base = database.Base

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_clients(db):
    try:
        utils.create_clients(data.clients, db=db)
    finally:
        db.close()


def create_new_pets(db):
    try:
        utils.create_pets(data.pets, db=db)
    finally:
        db.close()
