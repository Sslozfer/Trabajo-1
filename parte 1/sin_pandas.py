# Importar bibliotecas necesarias
import requests  # Para hacer peticiones web
import plotly.express as px  # Para crear graficos interactivos
from datetime import datetime, timedelta  # Para manejar fechas y tiempos

# Configurar el rango de tiempo (ultimas 24 horas)
tiempo_final = datetime.utcnow()  # Obtener hora actual en UTC
tiempo_inicial = tiempo_final - timedelta(days=1)  # Restar 1 día

# Construir URL para la API de terremotos
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={tiempo_inicial.strftime('%Y-%m-%d')}&endtime={tiempo_final.strftime('%Y-%m-%d')}&minmagnitude=2.5"

# Obtener datos de terremotos
respuesta = requests.get(url)  # Hacer peticion a la API
datos = respuesta.json()  # Convertir respuesta a formato Python

# Procesar datos de terremotos
lista_terremotos = []  # Lista para almacenar terremotos

for terremoto in datos['features']:
    propiedades = terremoto['properties']  # Propiedades del terremoto
    geometria = terremoto['geometry']  # Ubicacion geografica
    
    # Añadir cada terremoto a la lista
    lista_terremotos.append({
        'magnitud': propiedades['mag'],
        'lugar': propiedades['place'],
        'tiempo': datetime.utcfromtimestamp(propiedades['time']/1000),  # Convertir tiempo
        'longitud': geometria['coordinates'][0],
        'latitud': geometria['coordinates'][1],
        'profundidad': geometria['coordinates'][2]
    })

# Preparar datos para el grafico (sin pandas por que nachito no quiere :( )
datos_grafico = {
    'latitud': [t['latitud'] for t in lista_terremotos],
    'longitud': [t['longitud'] for t in lista_terremotos],
    'magnitud': [t['magnitud'] for t in lista_terremotos],
    'profundidad': [t['profundidad'] for t in lista_terremotos],
    'lugar': [t['lugar'] for t in lista_terremotos],
    'tiempo': [t['tiempo'] for t in lista_terremotos]
}

# Crear el mapa interactivo
mapa = px.scatter_geo(datos_grafico, 
                     lat='latitud',  # Columna para latitud
                     lon='longitud',  # Columna para longitud
                     size='magnitud',  # Tamaño segun magnitud
                     color='profundidad',  # Color segun profundidad
                     hover_name='lugar',  # Texto al pasar el mouse
                     hover_data={
                         'tiempo': True,  # Mostrar tiempo
                         'magnitud': True,  # Mostrar magnitud
                         'profundidad': True,  # Mostrar profundidad
                         'latitud': True,  # Mostrar latitud
                         'longitud': True  # Mostrar longitud
                     },
                     projection='natural earth',  # Tipo de proyeccion
                     title=f'Terremotos globales en las últimas 24 horas (desde {tiempo_inicial} UTC)',
                     color_continuous_scale='viridis_r')  # Escala de colores

# Personalizar apariencia del mapa
mapa.update_geos(
    showcoastlines=True, coastlinecolor="Black",  # Mostrar lineas costeras
    showland=True, landcolor="lightgray",  # Color de tierra
    showocean=True, oceancolor="lightblue"  # Color de océano
)

# Ajustar margenes del grafico
mapa.update_layout(margin=dict(l=0, r=0, t=30, b=0))

# Mostrar el mapa interactivo
mapa.show()
