import requests
import plotly.express as px
from datetime import datetime, timedelta

end_time = datetime.utcnow()
start_time = end_time - timedelta(days=1)

url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time.strftime('%Y-%m-%d')}&endtime={end_time.strftime('%Y-%m-%d')}&minmagnitude=2.5"

response = requests.get(url)
data = response.json()

terremotos = []
for feature in data['features']:
    props = feature['properties']
    geom = feature['geometry']
    terremotos.append({
        'magnitud': props['mag'],
        'lugar': props['place'],
        'tiempo': datetime.utcfromtimestamp(props['time']/1000),
        'longitud': geom['coordinates'][0],
        'latitud': geom['coordinates'][1],
        'profundidad': geom['coordinates'][2]
    })

# Crear un diccionario con los datos para el gráfico
data_dict = {
    'latitud': [t['latitud'] for t in terremotos],
    'longitud': [t['longitud'] for t in terremotos],
    'magnitud': [t['magnitud'] for t in terremotos],
    'profundidad': [t['profundidad'] for t in terremotos],
    'lugar': [t['lugar'] for t in terremotos],
    'tiempo': [t['tiempo'] for t in terremotos]
}

fig = px.scatter_geo(data_dict, 
                     lat='latitud', 
                     lon='longitud',
                     size='magnitud',
                     color='profundidad',
                     hover_name='lugar',
                     hover_data={
                         'tiempo': True,
                         'magnitud': True,
                         'profundidad': True,
                         'latitud': True,
                         'longitud': True
                     },
                     projection='natural earth',
                     title=f'Terremotos globales en las últimas 24 horas (desde {start_time} UTC)',
                     color_continuous_scale='viridis_r')

fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                showland=True, landcolor="lightgray",
                showocean=True, oceancolor="lightblue")

fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
fig.show()