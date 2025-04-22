# Importar las bibliotecas necesarias
import requests  # Para hacer peticiones web
import plotly.express as px  # Para crear graficos interactivos
import pandas as pd  # Para manejar datos en tablas
from datetime import datetime, timedelta  # Para trabajar con fechas

# Configurar el rango de tiempo (últimas 24 horas)
tiempo_final = datetime.utcnow()  # Hora actual en UTC
tiempo_inicial = tiempo_final - timedelta(days=1)  # Restar 1 día

# Construir la URL para la API de terremotos
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={tiempo_inicial.strftime('%Y-%m-%d')}&endtime={tiempo_final.strftime('%Y-%m-%d')}&minmagnitude=2.5"

# Obtener los datos de terremotos
respuesta = requests.get(url)  # Hacer la petición a la API
datos = respuesta.json()  # Convertir la respuesta a formato Python

# Procesar los datos de terremotos
caracteristicas = datos['features']  # Extraer la lista de terremotos
lista_terremotos = []  # Lista para almacenar los terremotos procesados

for caracteristica in caracteristicas:
    propiedades = caracteristica['properties']  # Propiedades del terremoto
    geometria = caracteristica['geometry']  # Ubicación geografica
    
    # Añadir cada terremoto a la lista con sus datos principales
    lista_terremotos.append({
        'magnitud': propiedades['mag'],  # Magnitud del terremoto
        'lugar': propiedades['place'],  # Lugar 
        'tiempo': pd.to_datetime(propiedades['time'], unit='ms'),  # Hora convertida
        'longitud': geometria['coordinates'][0],  # Coordenada de longitud
        'latitud': geometria['coordinates'][1],  # Coordenada de latitud
        'profundidad': geometria['coordinates'][2]  # Profundidad en km
    })

# Crear una tabla con los datos
tabla_terremotos = pd.DataFrame(lista_terremotos)

# Crear el mapa interactivo de terremotos
mapa = px.scatter_geo(tabla_terremotos, 
                     lat='latitud',  # Columna para latitud
                     lon='longitud',  # Columna para longitud
                     size='magnitud',  # Tamaño según magnitud
                     color='profundidad',  # Color segun profundidad
                     hover_name='lugar',  # Texto al pasar el mouse
                     hover_data=['tiempo', 'magnitud', 'profundidad'],  ## Texto al pasar el mouse
                     projection='natural earth',  # Tipo de proyeccion del mapa
                     title=f'Terremotos globales en las últimas 24 horas (desde {tiempo_inicial} UTC)',
                     color_continuous_scale='viridis_r')  # Escala de colores

# Personalizar la apariencia del mapa
mapa.update_geos(
    showcoastlines=True, coastlinecolor="Black",  # Mostrar costas en negro
    showland=True, landcolor="lightgray",  # Mostrar tierra en gris claro
    showocean=True, oceancolor="lightblue"  # Mostrar océano en azul claro
)

# Ajustar los margenes del grafico
mapa.update_layout(margin=dict(l=0, r=0, t=30, b=0))

# Mostrar el mapa interactivo
mapa.show()
