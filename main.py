from typing import Optional
from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el archivo CSV al iniciar la aplicación
file_path = 'mergeLimpio.csv'
data = pd.read_csv(file_path)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Bienvenid jero capo de la vida"}

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

@app.get("/actor")
def get_actor(nombre_actor: str):
    # Filtrar el dataset para encontrar las películas en las que ha participado el actor
    peliculas_actor = data[data['actors'].str.contains(nombre_actor, case=False, na=False)]

    # Verificar si el actor tiene alguna película en el dataset
    if peliculas_actor.empty:
        return {"error": f"No se encontró ningún registro para el actor {nombre_actor}."}

    # Calcular la cantidad de películas
    cantidad_peliculas = len(peliculas_actor)

    # Calcular el retorno total y el promedio de retorno por película
    retorno_total = peliculas_actor['return'].sum()  # Cambia 'return' si la columna tiene otro nombre
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    return {
        "mensaje": f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    }


@app.get("/director")
def get_director(nombre_director: str):
    # Filtrar el dataset para encontrar las películas dirigidas por el director
    peliculas_director = data[data['directors'].str.contains(nombre_director, case=False, na=False)]

    # Verificar si el director tiene alguna película en el dataset
    if peliculas_director.empty:
        return {"error": f"No se encontró ningún registro para el director {nombre_director}."}

    # Calcular el retorno total del director
    retorno_total = peliculas_director['return'].sum()  # Cambia 'return' si la columna tiene otro nombre

    # Crear una lista para almacenar los detalles de cada película
    detalles_peliculas = []
    for _, pelicula in peliculas_director.iterrows():
        titulo = pelicula['title']
        fecha_lanzamiento = pelicula['release_date']
        retorno_individual = pelicula['return']  # Cambia 'return' si la columna tiene otro nombre
        costo = pelicula['budget']  # Cambia 'budget' si la columna tiene otro nombre
        ganancia = pelicula['revenue']  # Cambia 'revenue' si la columna tiene otro nombre
        
        detalles_peliculas.append({
            "titulo": titulo,
            "fecha_lanzamiento": fecha_lanzamiento,
            "retorno_individual": retorno_individual,
            "costo": costo,
            "ganancia": ganancia
        })

    return {
        "mensaje": f"El director {nombre_director} ha conseguido un retorno total de {retorno_total}.",
        "detalles_peliculas": detalles_peliculas
    }
