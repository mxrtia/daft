import hashlib
import re
from fastapi import FastAPI, Response, status, HTTPException, Depends, Cookie
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import random


app = FastAPI()
app.counter = 0
app.id = 1
app.list = []

security = HTTPBasic()

# app.access_token=""
# app.login_token=""
app.access_token=[]
app.login_token=[]

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


@app.post("/method", status_code=201)
def post_method():
    return {"method": "POST"}


@app.delete("/method")
def delete_method():
    return {"method": "DELETE"}
    
@app.put("/method")
def put_method():
    return {"method": "PUT"}    


@app.options("/method")
def options_method():
    return {"method": "OPTIONS"}
  

@app.get("/auth")
def auth_method(password: Optional[str] = None, password_hash: Optional[str] = None):
    if password is None or password_hash is None or password=="" or password_hash=="":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    hash = hashlib.sha512(password.encode())
    if hash.hexdigest() == password_hash:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


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
    newname = r.sub('', item.name)
    newsurname = r.sub('', item.surname)

    vaccination=len(newname)+len(newsurname)
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
        
        
#ZADANIE DOMOWE 3

#3.1
@app.get("/hello", response_class=HTMLResponse)
def hello():
    datetoday = date.today()
    datetodayf = datetoday.strftime("%Y-%m-%d")
    return f"""
    <html>
        <head>
            <h1>Hello! Today date is {datetodayf}</h1>
        </head>
    </html>
    """
#3.2
# @app.post("/login_session")
# def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = secrets.compare_digest(credentials.username, "4dm1n")
#     correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
#     if credentials.username==None or credentials.password==None or credentials.username=="" or credentials.password=="":
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if not (correct_username and correct_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     else:
#         session_token = hashlib.sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
#         app.access_token=session_token
#         response.set_cookie(key="session_token", value=session_token)
#         response.status_code = status.HTTP_201_CREATED
#         print(session_token)
#         print("access token",app.access_token)

# @app.post("/login_token", response_class=JSONResponse)
# def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = secrets.compare_digest(credentials.username, "4dm1n")
#     correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
#     if not (correct_username and correct_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if not (correct_username and correct_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     else:
#         token_value = hashlib.sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
#         app.login_token=token_value
#         response.status_code = status.HTTP_201_CREATED
#         print("login token",app.login_token)
#         return {"token": token_value}


#3.3
# @app.get("/welcome_session")
# def welcome_session(format: Optional[str]=None, session_token: str = Cookie(None)):
#     if session_token is None or not app.access_token==session_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if format is not None and format=="json":
#         return JSONResponse(content={"message": "Welcome!"}, status_code=status.HTTP_200_OK)
#     elif format is not None and format=="html":
#         return HTMLResponse(content="<h1>Welcome!</h1>", status_code=status.HTTP_200_OK)
#     else:
#         return Response(content="Welcome!", status_code=status.HTTP_200_OK, media_type="text/plain")

# @app.get("/welcome_token")
# def welcome_token(format: Optional[str]=None, token: Optional[str]=None):
#     if token is None or not app.login_token==token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if format is not None and format=="json":
#         return JSONResponse(content={"message": "Welcome!"}, status_code=status.HTTP_200_OK)
#     elif format is not None and format=="html":
#         return HTMLResponse(content="<h1>Welcome!</h1>", status_code=status.HTTP_200_OK)
#     else:
#         return Response(content="Welcome!", status_code=status.HTTP_200_OK, media_type="text/plain")


#3.4
# @app.delete("/logout_session")
# def logout_session(format: Optional[str]=None, session_token: str = Cookie(None)):
#     if session_token is None or not app.access_token==session_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     else:
#         app.access_token=""
#         return RedirectResponse(url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND)

# @app.delete("/logout_token")
# def logout_token(token: Optional[str]=None, format: Optional[str]=None):
#     if token is None or not app.login_token==token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     else:
#         app.login_token=""
#         return RedirectResponse(url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND)


# @app.get("/logged_out")
# def logged_out(format: Optional[str]=None):
#     if format is not None and format=="json":
#         return JSONResponse(content={"message": "Logged out!"}, status_code=status.HTTP_200_OK)
#     elif format is not None and format=="html":
#         return HTMLResponse(content="<h1>Logged out!</h1>", status_code=status.HTTP_200_OK)
#     else:
#         return Response(content="Logged out!", status_code=status.HTTP_200_OK, media_type="text/plain")
    

#3.5

##

@app.post("/login_session", status_code = status.HTTP_201_CREATED)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    # if credentials.username==None or credentials.password==None or credentials.username=="" or credentials.password=="":
    #     raise HTTPException(status_code=sta tus.HTTP_401_UNAUTHORIZED)
    if not (correct_username or correct_password):  #and
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y/%H/%M/%S")
        session_token = hashlib.sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()+dt_string+str(random.randrange(1000, 2000))
        if len(app.access_token)>3:
            app.access_token.pop(0)
            app.access_token.append(session_token)
        else:
            app.access_token.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        # response.status_code = status.HTTP_201_CREATED
        #print(session_token)
        #print("access token",app.access_token)

@app.post("/login_token", status_code = status.HTTP_201_CREATED)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y/%H/%M/%S")
        token_value = hashlib.sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()+dt_string+str(random.randrange(0, 999))	
        # app.login_token=token_value
        if len(app.login_token)>3:
            app.login_token.pop(0)
            app.login_token.append(token_value)
        else:
            app.login_token.append(token_value)
        # response.status_code = status.HTTP_201_CREATED
        #print("login token",app.login_token)
        return {"token": token_value}

##

@app.get("/welcome_session")
def welcome_session(format: Optional[str]=None, session_token: str = Cookie(None)):
    if session_token == None or not session_token in app.access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if format=="json":
        return JSONResponse(content={"message": "Welcome!"}, status_code=status.HTTP_200_OK)
    elif format=="html":
        return HTMLResponse(content="<h1>Welcome!</h1>", status_code=status.HTTP_200_OK)
    else:
        return Response(content="Welcome!", status_code=status.HTTP_200_OK, media_type="text/plain")

@app.get("/welcome_token")
def welcome_token(format: Optional[str]=None, token: Optional[str]=None):
    if token == None or not token in app.login_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if format=="json":
        return JSONResponse(content={"message": "Welcome!"}, status_code=status.HTTP_200_OK)
    elif format=="html":
        return HTMLResponse(content="<h1>Welcome!</h1>", status_code=status.HTTP_200_OK)
    else:
        return Response(content="Welcome!", status_code=status.HTTP_200_OK, media_type="text/plain")

##

@app.delete("/logout_session")
def logout_session(format: Optional[str]=None, session_token: str = Cookie(None)):
    if session_token is None or not session_token in app.access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    app.access_token.remove(session_token)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND)

@app.delete("/logout_token")
def logout_token(token: Optional[str]=None, format: Optional[str]=None):
    if token is None or not token in app.login_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    app.login_token.remove(token)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND)

@app.get("/logged_out")
def logged_out(format: Optional[str]=None):
    # if format == None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if format=="json":
        return JSONResponse(content={"message": "Logged out!"}, status_code=status.HTTP_200_OK)
    elif format=="html":
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=status.HTTP_200_OK)
    else:
        return Response(content="Logged out!", status_code=status.HTTP_200_OK, media_type="text/plain")



          