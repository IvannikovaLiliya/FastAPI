from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Union, list

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


@app.get('/')
# возвращаем списком post_db для проверки работы метода /post
def root():
    return post_db


@app.post('/post', response_model=Timestamp)
# создаем новую запись в post_db и возвращаем её в случае успешного создания
def get_post():
    try:
        last_timestamp = post_db[-1]
        new_row = Timestamp(id=last_timestamp.id + 1, timestamp=last_timestamp.timestamp + 1)
    except IndexError:
        new_row = Timestamp(id=1, timestamp=1)
    post_db.append(new_row)
    return new_row


@app.get('/dog', response_model=list[Dog])
# возвращаем инофрмацию о всех собаках вводимой породы, иначе ошибку. Если порода не выбрана, воззвращаем всех собак
def get_dogs(kind: Union[str, None] = None):
    if kind is None:
        dog_list = [dog for dog in dogs_db.values()]
        return dog_list
    else:
        dog_list = [dog for dog in dogs_db.values() if dog.kind == kind]
        return dog_list


@app.post('/dog', response_model=Dog)
# создаем новую запись в dogs_db и возвращаем её в случае успешного создания
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=422, detail="Данный PK занят!")
    dogs_db[dog.pk] = dog
    return dog


@app.get("/dog/{pk}", response_model=Dog)
def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=422, detail=f"Собака по данному PK ({pk}) не найдена!")
    return dogs_db[pk]


@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=422, detail=f"Собака по данному PK ({pk}) не найдена!")
    elif dog.pk != pk:
        raise HTTPException(status_code=422, detail=f"Нельзя менять pk!")
    dogs_db[pk] = dog
    return dog
