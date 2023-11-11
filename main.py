from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Path
from fastapi import HTTPException
from fastapi import Query
from typing import List


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


class DogsByTypeResponse(BaseModel):
    dogs: List[Dog]


@app.get('/')
def root():
    return "Welcome to clinics microservice"


@app.get('/dogs', response_model=List[Dog])
def get_dogs():
    return List(dogs_db.values())


@app.get('/dogs/{dog_id}', response_model=Dog)
def get_dog_by_id(dog_id: int = Path(..., title="Dog ID")):
    dog = dogs_db.get(dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@app.post('/add_dog', response_model=Dog)
def create_dog(dog: Dog):
    new_dog_id = max(dogs_db.keys(), default=-1) + 1
    dog.pk = new_dog_id
    dogs_db[new_dog_id] = dog
    return dog


@app.get('/dogs_by_type', response_model=DogsByTypeResponse)
def get_dogs_by_type(kind: DogType = Query(..., title="Dog Type")):
    filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
    return {"dogs": filtered_dogs}


@app.patch('/dog/update/{dog_id}', response_model=Dog)
def update_dog(dog_id: int = Path(..., title="Dog ID"), updated_dog: Dog = None):
    if dog_id not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")

    existing_dog = dogs_db[dog_id]

    if updated_dog:
        existing_dog.name = updated_dog.name
        existing_dog.kind = updated_dog.kind

    return existing_dog
