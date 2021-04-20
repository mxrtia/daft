# -*- coding: utf-8 -*-

import hashlib
import re
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, timedelta
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.counter = 0
app.id = 1
app.list = []

class HelloResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
def hello_name_view(name: str):
    return HelloResp(msg=f"Hello {name}")


@app.get("/method")
def get_method():
    return {"method": "GET"}


@app.post("/method")
def get_method():
    return {"method": "POST"}


@app.delete("/method")
def get_method():
    return {"method": "DELETE"}
    
@app.put("/method")
def get_method():
    return {"method": "PUT"}    


@app.options("/method")
def get_method():
    return {"method": "OPTIONS"}
  

@app.get("/auth")
def auth_method(password: Optional[str] = None, password_hash: Optional[str] = None):
    hash = hashlib.sha512(password.encode())
    if hash.hexdigest() == password_hash:
        raise HTTPException(status_code=204)
    else:
        raise HTTPException(status_code=401)


class Item(BaseModel):
    id: Optional[int]
    name: str
    surname: str
    register_date: Optional[date]
    vaccination_date: Optional[date]
    
    
@app.post("/register")
async def register(item: Item, response: Response):
    item.id=app.id
    item.register_date=date.today()
    
    r= re.compile('[^a-zA-ZąĄćĆęĘłŁńŃóÓśŚżŻźŹ]')
    item.name = r.sub('', item.name)
    item.surname = r.sub('', item.surname)

    vaccination=len(item.name)+len(item.surname)
    item.vaccination_date=date.today()+timedelta(vaccination)
    
    app.id +=1
    app.list.append(item)
    response.status_code = status.HTTP_201_CREATED
    return jsonable_encoder(item)


@app.get("/patient/{id}")
async def getinfo(id: int, response: Response):
    if not app.list:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif id>=1:
        for i in app.list:
            if i.id == id:
                response.status_code = status.HTTP_200_OK
                return jsonable_encoder(i)
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
