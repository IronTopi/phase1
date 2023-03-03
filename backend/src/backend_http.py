from typing import Union

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

@app.get("/")
def read_root():
    return {"Hello": "u dude"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, credentials: HTTPBasicCredentials = Depends(security)):
    return {"item_id": item_id, "q": q}