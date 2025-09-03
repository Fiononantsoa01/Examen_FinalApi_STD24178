from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristis: Characteristis
class  Characteristics(BaseModel):
    ram_memory: int
    rom_memory: int

phones_stored: List[Phone] = []
@app.get("/health")
async def health():
    return {"message": "ok"}
@app.post("/phones", response_model=Phone)
async def create_phone(phone: Phone):
    for existing_phone in phones_stored:
        if existing_phone.model == phone.model:
            raise HTTPException(status_code=400, detail="Phone model already exists")
    phones_stored.append(phone)
    return phone
@app.get("/phones", response_model=List[Phone])
async def get_phones():
    return phones_stored
@app.get("/phones/{id}", response_model=Phone)
async def get_phone(identifier: str):
    for phone in phones_stored:
        if phone.model == identifier:
            return phone
    raise HTTPException(status_code=404, detail="Phone not found")

