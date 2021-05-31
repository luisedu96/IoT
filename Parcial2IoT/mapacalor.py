import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
from scipy.interpolate import griddata

app = dash.Dash()   #6.2386048,-75.5858882,15z

customer_json_file ='Datos_SIATA_Aire_pm25.json'
customers_json = pd.read_json(customer_json_file, convert_dates=True)
latitudes = customers_json.latitud.values.tolist()
longitudes = customers_json.longitud.values.tolist()
nombres=customers_json.nombre.values.tolist()
fechas = []
valorpm=[]

for i in range(len(customers_json.datos[0])):
    cant = []
    for l in range(len(customers_json.datos)):
        cant.append(customers_json.datos[l][i].get('valor'))
    valorpm.append(cant)

for f in range(len(customers_json.datos[0])):
    fechas.append(customers_json.datos[0][f].get('fecha'))

puntos = []
for cor in range(len(longitudes)):
    p = [longitudes[cor],latitudes[cor]]
    puntos.append(p)
"""
grid_x, grid_y = np.mgrid[np.min(longitudes):np.max(longitudes):100j, np.min(latitudes):np.max(latitudes):100j]

grid_z0 = griddata(puntos, valorpm[0], (grid_x, grid_y), method='nearest')
grid_z1 = griddata(puntos, valorpm[0], (grid_x, grid_y), method='linear')
grid_z2 = griddata(puntos, valorpm[0], (grid_x, grid_y), method='cubic')

latnew=[]
for py in grid_y:
    for mo in py:
        latnew.append(mo)
lonnew=[]
for px in grid_x:
    for mu in px:
        lonnew.append(mu)
valorgrid0=[]
for zg in grid_z0:
    for zp in zg:
        valorgrid0.append(zp)
valorgrid1=[]
for zg in grid_z1:
    for zp in zg:
        valorgrid1.append(zp)
valorgrid2=[]
for zg in grid_z2:
    for zp in zg:
        valorgrid2.append(zp)

fig = go.Figure(go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=valorpm[0]
        ),
        text=nombres
    ))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    margin = {'l': 0, 'r': 0, 'b': 0, 't': 0},
    mapbox=dict(
        accesstoken='pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
        bearing=0,
        center=go.layout.mapbox.Center(
            lat= 6.240737,
            lon= -75.589900
        ),
        pitch=0,
        zoom=9.5
    )
)
"""
fig = go.Figure(go.Densitymapbox(lat=latitudes, lon=longitudes, z=valorpm[0],
                                 radius=10))
fig.update_layout(mapbox_style="satellite-streets", mapbox_center_lon=-75.589900)
fig.update_layout(
   margin={"r":0,"t":0,"l":0,"b":0},
   mapbox=dict(
        accesstoken='pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
        bearing=0,
        center=go.layout.mapbox.Center(
            lat= 6.240737,
            lon= -75.589900
        ),
        zoom=9.5
    )
)

fig.show()

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=80)
