import requests
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

end_time = datetime.utcnow()
start_time = end_time - timedelta(days=1)

url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time.strftime('%Y-%m-%d')}&endtime={end_time.strftime('%Y-%m-%d')}&minmagnitude=2.5"

response = requests.get(url)
data = response.json()

features = data['features']
terremotos = []
for feature in features:
    accesorios = feature['properties']
    geometria= feature['geometry']
    terremotos.append({
        'magnitud': accesorios['mag'],
        'lugar': accesorios['place'],
        'tiempo': pd.to_datetime(accesorios['time'], unit='ms'),
        'longitud': geometria['coordinates'][0],
        'latitud': geometria['coordinates'][1],
        'profundidad': geometria['coordinates'][2]
    })

df = pd.DataFrame(terremotos)

fig = px.scatter_geo(df, 
                     lat='latitud', 
                     lon='longitud',
                     size='magnitud',
                     color='profundidad',
                     hover_name='lugar',
                     hover_data=['tiempo', 'magnitud', 'profundidad'],
                     projection='natural earth',
                     title=f'Terremotos globales en las últimas 24 horas (desde {start_time} UTC)',
                     color_continuous_scale='viridis_r')

fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                showland=True, landcolor="lightgray",
                showocean=True, oceancolor="lightblue")

fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
fig.show()