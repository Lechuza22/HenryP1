from fastapi import FastAPI
import pandas as pd
from datetime import datetime

# Inicializar la aplicación FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Bienvenido al proyecto de Jero"}     

