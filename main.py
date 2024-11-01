from fastapi import FastAPI
import pandas as pd
from datetime import datetime

app = FastAPI()

# Cargar el archivo CSV al iniciar la aplicación
data = pd.read_csv("MoviTransformado.csv")

@app.get("/")
def read_root():
    return {"Bienvenido al proyecto de Jero"}

@app.get("/mes")
def cantidad_filmaciones_mes(mes: str):
    # Convertir el mes a minúsculas para evitar problemas de mayúsculas
    mes = mes.lower()
    
    # Diccionario para convertir el nombre del mes en español al número correspondiente
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    # Validar si el mes ingresado es válido
    if mes not in meses:
        return {"error": "Mes ingresado no válido. Por favor, ingrese un mes en español."}
    
    # Obtener el número del mes correspondiente
    numero_mes = meses[mes]
    
    # Convertir la columna de fechas al tipo datetime si es necesario
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    
    # Filtrar las películas estrenadas en el mes especificado
    peliculas_mes = data[data['release_date'].dt.month == numero_mes]
    cantidad = len(peliculas_mes)
    
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"}

@app.get("/dia")
def cantidad_filmaciones_dia(dia: str):
    # Convertir el día a minúsculas para evitar problemas de mayúsculas
    dia = dia.lower()

    # Diccionario para convertir el nombre del día en español al número correspondiente
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2,
        "jueves": 3, "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6
    }

    # Validar si el día ingresado es válido
    if dia not in dias:
        return {"error": "Día ingresado no válido. Por favor, ingrese un día en español."}

    # Obtener el número del día correspondiente (0=Lunes, 6=Domingo)
    numero_dia = dias[dia]

    # Convertir la columna de fechas al tipo datetime si es necesario
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')

    # Filtrar las películas estrenadas en el día especificado
    peliculas_dia = data[data['release_date'].dt.dayofweek == numero_dia]
    cantidad = len(peliculas_dia)

    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"}


@app.get("/score_titulo")
def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar el dataset para encontrar la película que coincida con el título
    pelicula = data[data['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Verificar si se encontró la película
    if pelicula.empty:
        return {"error": "No se encontró ninguna película con ese título."}

    # Extraer la información relevante
    titulo = pelicula.iloc[0]['title']
    anio_estreno = pd.to_datetime(pelicula.iloc[0]['release_date']).year
    score = pelicula.iloc[0]['popularity']  # Cambia 'popularity' si la columna tiene otro nombre

    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {anio_estreno} con un score/popularidad de {score}"
    }

@app.get("/votos_titulo")
def votos_titulo(titulo_de_la_filmacion: str):
    # Filtrar el dataset para encontrar la película que coincida con el título
    pelicula = data[data['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Verificar si se encontró la película
    if pelicula.empty:
        return {"error": "No se encontró ninguna película con ese título."}

    # Extraer la información relevante
    titulo = pelicula.iloc[0]['title']
    anio_estreno = pd.to_datetime(pelicula.iloc[0]['release_date']).year
    cantidad_votos = pelicula.iloc[0]['vote_count']  # Cambia 'vote_count' si la columna tiene otro nombre
    promedio_votos = pelicula.iloc[0]['vote_average']  # Cambia 'vote_average' si la columna tiene otro nombre

    # Verificar si la película cumple con el requisito de al menos 2000 valoraciones
    if cantidad_votos < 2000:
        return {"mensaje": f"La película '{titulo}' no cuenta con al menos 2000 valoraciones, por lo que no se devuelve ningún valor."}

    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {anio_estreno}. La misma cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}."
    }
