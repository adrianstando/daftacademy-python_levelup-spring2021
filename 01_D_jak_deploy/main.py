from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from datetime import date, timedelta
import hashlib


def encrypt_string(hash_string):
    sha_signature = hashlib.sha512(hash_string.encode()).hexdigest()
    return sha_signature


app = FastAPI()
app.patient_counter = 0
app.dict = dict()


class Patient(BaseModel):
    name: str
    surname: str


@app.get("/")
def root():
    return JSONResponse(status_code=200, content={"message": "Hello World"})


@app.get("/method")
def method():
    return JSONResponse(status_code=200, content={"method": "GET"})


@app.get("/auth")
def auth(password: str, password_hash: str):
    if encrypt_string(password) == password_hash:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=401)


@app.post("/register")
def register(patient: Patient):
    app.patient_counter += 1
    today = date.today()
    vacc_date = today + timedelta(days=len(patient.name) + len(patient.surname))

    app.dict[app.patient_counter] = {'id': str(app.patient_counter),
                                     'name': patient.name,
                                     'surname': patient.surname,
                                     'register_date': today.strftime("%Y-/%m-/%d"),
                                     'vaccination_date': vacc_date.strftime("%Y-/%m-/%d")}

    return JSONResponse(status_code=201, content=app.dict[app.patient_counter])


@app.get("/patient/{id}")
def patient(id: int):
    if id < 0:
        raise HTTPException(status_code=400)
    elif id > app.patient_counter:
        raise HTTPException(status_code=404)
    else:
        return JSONResponse(status_code=200, content=app.dict[id])


if __name__ == "__main__":
    uvicorn.run("main:app")
