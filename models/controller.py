from enum import Enum

from pydantic import BaseModel


class BaseClient(BaseModel):
    document: str
    first_name: str
    last_name: str
    patronymic: str
    birthday: float


class Client(BaseClient):
    client_id: int


class BaseConsultation(BaseModel):
    client_id: int
    pet_id: int
    date: float
    description: str


class Consultation(BaseConsultation):
    consultation_id: int


class BasePet(BaseModel):
    client_id: int
    name: str
    birthday: float


class Pet(BasePet):
    pet_id: int


class Target(Enum):
    pets = 'pets'
    clients = 'clients'


class BaseTarget(BaseModel):
    target: Target


class BaseResponse(BaseModel):
    message: str


class Appointment(BaseModel):
    consultation_id: int
    date: float
    description: str
    client: Client
    pet: Pet