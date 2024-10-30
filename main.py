from fastapi import FastAPI
import pandas as pd
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"Bienvenido"}
