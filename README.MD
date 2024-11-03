# Readme Proyecro 1. Jerónimo Martinez

El siguiente proyecto cuenta con los siguiente pasos:
1. ETL.
2. Diseño de las APIs y el sistema de recomendación
3. Repositorio en GitHub  y Deploy en Render.
4. Análisis Exploratorio de los Datos (EDA)

# 1. ETL

Hemos recibido dos dataset: Movies_dataset y Credits. Los hemos extraido del repositorio de github de Henry. Ambos data sets, son muy grandes y con columnas anidadas que exigen que los normalicemos. 
Para ello en primer lugar trabajamos con Movies y en segundo lugar con credits. 
Siguiendo el criterio de la consigna realiamos las siguientes tranformaciones en Movies: 
1. Desanidamos Spoken_leanguages y nos quedamos con "name".
2. Desanidamos "genres" y nos quedamos con "names". 
3. Desanidamos belongs_to_collectión.
4. Eliminamos datos nulos y filas de release date. 
5. Eliminamos columnas innecesarias ('video','imdb_id','adult','original_title','poster_path','homepage')
6. Convertimos a formato año la columna realease.
7. Extrajimos el año y creamos una neuva columnas: release year
8. Eliminamos datos nulos de release date
9.Convertimos variable a numerica para realizar la acción
10. Creamos una nueva columna: return desde revenue y budget.
11. Extracción de datos anidados de "production_companies" y nos quedamos con "name"
12. Exportamos a CVS MoviTranforamdo

Tranformaciones en Credits.
1. Cargamos el archivo. 
2. Ver estructura de las primeras filas para entender la columna 'cast' y 'crew', que son las que vamos a desanidar.
3. Desanidamos ambas columnas y de csat nos quedamos con los nombres de los actores. y Con crew nos quedamos con "job" y los "name" de los "directos". 
4. Nos quedamos con las columnas: "id", "actors", "Directors". 
5. Exportamos a CSV: credits_limpio

Para terminar el ETL decidí unir los datasets: Se realizó la unión entre el dataset creditslimpio.csv y MoviTranformado.csv usando la columna "ID" como anclaje. Este merge se realizo para poder hacer funcionar las apis de directores y actores. 

1. Se importaron los archivos creditslimpio.csv y MoviTranformado.csv 
2. Merge a partir de Id.
3. Eliminamos columnas necesarias para optimizar el CSV:"tagline", "belongs_to_collection", "status", "spoken_languages"
4. Exportamos a MergeLimpio.csv.

Una vez terminada la normalización, cargamos los datos al repositorio personal en GitHub para luego poder ser deployado en render

# 2. Diseño de las APIs y el sistema de recomendación.

Mientras realizaba la normalización de los datos, creamos el entorno virtual en nuestro local, el cual lo pusheamos al GitHub via visualstudiocode. 
En el entorno virtual que subimos a Github trabajamos con el archivo main.py, el cual contienen las apis y el sistema de recomendación. 
También el entorno virtual creo el archivo Requeriments donde se puse las librerías que utilice. 
En el archivo Main.py se puede ver desarrolado el código, con sus comentarios sobre las apis y el sistema de recomendación. (En primer lugar fue probado en visualStudio y luego fue probado y deployado en render). Me parece redundante subir aqui el codigo de las apis y sus comentarios estando en el archivo. 

# 3. Repositorio en Git y deploy en render.

Una vez las Apis desarrolladas en github en el archivo main.py fueron deployadas con éxito en render, donde se pudieron probar y ejecutar correctamente: https://henryp1.onrender.com/docs Aqui podrás acceder para probarlas en caso oportuno en sus respectivos endpoints. 

# 4. Analisis exploratorio de los datos EDA. 

El EDA esta compuesto por las siguiente variables de analisis. Estas variables estan obtenidas de la lectura del dataset MergeLimpio. 
1. Distribución de presupuesto, ingresos y retorno
2. Correlación entre presupuesto, ingresos y popularidad.
3. Relación entre duración y calificación promedio.
4. Análisis de popularidad por año de lanzamiento.
5. Ranking de los géneros más comunes.
6. Comparación entre popularidad y votos.
7. Ingresos promedio por compañía de producción.
8. Rentabilidad promedio por director.
9. Nube de palabras a partir de los títulos de las películas.
10. Análisis de actores más frecuentes

Los resultados del EDA, listas y graficos, y los insights se encuentran en el archivo EDA.ipynb. 
El EDA realizado nos permitió tener una visión más realista del negocio y de las opciones de inversión.
​
Muchas gracias por su lectura. 
