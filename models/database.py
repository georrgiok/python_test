from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

Base = declarative_base()


class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True, index=True)
    document = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    birthday = Column(Float)


class Pet(Base):
    __tablename__ = "pet"

    pet_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client.client_id"))
    name = Column(String)
    birthday = Column(Float)


class Consultation(Base):
    __tablename__ = "consultation"

    consultation_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(ForeignKey("client.client_id"))
    pet_id = Column(ForeignKey("pet.pet_id"))
    date = Column(Float)
    description = Column(String)
