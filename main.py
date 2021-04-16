from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from datetime import date, timedelta
import hashlib
import re


def encrypt_string(hash_string):
    sha_signature = hashlib.sha512(hash_string.encode()).hexdigest()
    return sha_signature


app = FastAPI()
app.patient_counter = 0
app.dict = dict()


class Patient(BaseModel):
    name: str
    surname: str


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
def auth(password: str, password_hash: str):
    if encrypt_string(password) == password_hash:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=401)


# ZADANIE 4
@app.post("/register")
def register(patient: Patient):
    app.patient_counter += 1
    today = date.today()

    name_and_surname = patient.name + patient.surname

    regex = re.compile('[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]')
    name_and_surname = regex.sub('', name_and_surname)

    vacc_date = today + timedelta(days=len(name_and_surname))

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

# if __name__ == "__main__":
#    uvicorn.run("main:app")
