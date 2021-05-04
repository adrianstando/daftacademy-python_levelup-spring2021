from fastapi import FastAPI, HTTPException, Cookie, Depends
from fastapi.responses import Response, JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from pydantic import BaseModel
import uvicorn
import datetime
import hashlib
import re


def encrypt_string(hash_string):
    sha_signature = hashlib.sha512(hash_string.encode()).hexdigest()
    return sha_signature


app = FastAPI()
app.patient_counter = 0
app.dict = dict()

app.credentials = dict({'login': '4dm1n',
                        'password': 'NotSoSecurePa$$'})
app.session_tokens = []
app.login_tokens = []


class Patient(BaseModel):
    name: str
    surname: str


#### HOMEWORK 1

# ZADANIE 1
@app.get("/")
def root():
    return JSONResponse(status_code=200, content={"message": "Hello world!"})


# ZADANIE 2
@app.get("/method")
def method():
    return JSONResponse(status_code=200, content={"method": "GET"})


@app.post("/method")
def method():
    return JSONResponse(status_code=201, content={"method": "POST"})


@app.delete("/method")
def method():
    return JSONResponse(status_code=200, content={"method": "DELETE"})


@app.put("/method")
def method():
    return JSONResponse(status_code=200, content={"method": "PUT"})


@app.options("/method")
def method():
    return JSONResponse(status_code=200, content={"method": "OPTIONS"})


# ZADANIE 3
@app.get("/auth")
def auth(password: Optional[str] = None, password_hash: Optional[str] = None):
    if password is None or password_hash is None:
        raise HTTPException(status_code=401)
    if password == '' or password_hash == '':
        raise HTTPException(status_code=401)
    if encrypt_string(password) == password_hash:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=401)


# ZADANIE 4
@app.post("/register")
def register(patient: Patient):
    app.patient_counter += 1
    today = datetime.date.today()

    name_and_surname = patient.name + patient.surname

    regex = re.compile('[^a-zA-ZĄąĘęŃńŻżŹźÓó]')
    name_and_surname = regex.sub('', name_and_surname)

    vacc_date = today + datetime.timedelta(days=len(name_and_surname))

    app.dict[app.patient_counter] = {'id': app.patient_counter,
                                     'name': patient.name,
                                     'surname': patient.surname,
                                     'register_date': today.strftime("%Y-%m-%d"),
                                     'vaccination_date': vacc_date.strftime("%Y-%m-%d")}

    return JSONResponse(status_code=201, content=app.dict[app.patient_counter])


# ZADANIE 5
@app.get("/patient/{id}")
def patient(id: int):
    if id < 0:
        raise HTTPException(status_code=400)
    elif id > app.patient_counter:
        raise HTTPException(status_code=404)
    else:
        return JSONResponse(status_code=200, content=app.dict[id])


#### HOMEWORK 3

# ZADANIE 1
@app.get("/hello", response_class=HTMLResponse)
def hello_html():
    today = datetime.date.today()
    return "<h1>Hello! Today date is " + today.strftime("%Y-%m-%d") + "</h1>"


# ZADANIE 2
security = HTTPBasic()


@app.post("/login_session")
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == app.credentials.get('login') and credentials.password == app.credentials.get('password'):
        today = datetime.datetime.now()
        session_token = encrypt_string(f"{credentials.username}{credentials.password}{today}")

        app.session_tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)

        response.status_code = 201

        return response
    else:
        response.status_code = 401
        return response


@app.post("/login_token")
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == app.credentials.get('login') and credentials.password == app.credentials.get('password'):
        today = datetime.datetime.now()
        login_token = encrypt_string(f"{credentials.username}{credentials.password}{today}")

        app.login_tokens.append(login_token)

        return JSONResponse(status_code=201, content={"token": login_token})
    else:
        return Response(status_code=401)


# ZADANIE 3
def message(txt, format_message):
    if format == "json":
        return JSONResponse(content={"message": txt}, status_code=200)
    elif format == "html":
        return HTMLResponse(content="<h1>" + txt + "</h1>", status_code=200)
    else:
        return PlainTextResponse(content=txt, status_code=200)


@app.get("/welcome_session")
def welcome_session(session_token: str = Cookie(None), format: Optional[str] = None):
    if session_token in app.session_tokens:
        return message("Welcome!", format)
    else:
        return Response(status_code=401)


@app.get("/welcome_token")
def welcome_token(token: str, format: Optional[str] = None):
    if token in app.login_tokens:
        return message("Welcome!", format)
    else:
        return Response(status_code=401)


# ZADANIE 4
@app.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: Optional[str] = None):
    if session_token in app.session_tokens:
        app.session_tokens.remove(session_token)
        return RedirectResponse(url="/logged_out" + f"?format={format}", status_code=303)
    else:
        return Response(status_code=401)


@app.delete("/logout_token")
def logout_token(token: str, format: Optional[str] = None):
    if token in app.login_tokens:
        app.login_tokens.remove(token)
        return RedirectResponse(url="/logged_out" + f"?format={format}", status_code=303)
    else:
        return Response(status_code=401)


@app.get("/logged_out")
def logged_out(format: Optional[str] = None):
    return message("Logged out!", format)


if __name__ == "__main__":
    uvicorn.run("main:app")
