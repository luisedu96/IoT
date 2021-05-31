# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 05:53:52 2020

@author: luise
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, date, time, timedelta
from scipy.interpolate import griddata
import numpy as np


app = dash.Dash()

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

grid_x, grid_y = np.mgrid[np.min(longitudes):np.max(longitudes):200j, np.min(latitudes):np.max(latitudes):200j]

latnew=[]
for py in grid_y:
    for mo in py:
        latnew.append(mo)
lonnew=[]
for px in grid_x:
    for mu in px:
        lonnew.append(mu)

def zinter(muestra):
    grid_z0 = griddata(puntos, muestra, (grid_x, grid_y), method='nearest')
    grid_z2 = griddata(puntos, muestra, (grid_x, grid_y), method='cubic')
    for k in range (len(grid_z2)):
        for p in range (len(grid_z2[k])):
            if np.isnan(grid_z2[k][p]):
                grid_z2[k][p]=grid_z0[k][p]
           
    valorgrid2=[]
    for zg in grid_z2:
        for zp in zg:
            valorgrid2.append(zp)
    return valorgrid2

zinterpolacion=[]
for pm25 in valorpm:
    k=zinter(pm25)
    zinterpolacion.append(k)

app.layout = html.Div([
    html.H1(id='Title1',children='Mapa de visualización de los valores de PM2.5',style={'color':'#3A65A6','text-align':'center'}),
    html.Div('Elige la fecha a consultar'),
    dcc.DatePickerSingle(id='datepicker',date=datetime(2019, 2, 21, 0, 0, 0)),
    html.Div('Elige la hora'),
    dcc.Slider(id='hora',min=0,max=23,marks={i: '{} horas'.format(i) for i in range(24)},value=0),
    html.Div(id='encontrar',children=' ',style={'color':'#38629D'}),
    dcc.Graph(id='g1',figure={
          'data': [{
            'lat': latitudes,
            'lon': longitudes,
            'text': nombres,
            'marker': {
                'color': '#00ff00',
                'size': 10,
                'opacity': 0.6
            },
            'type':'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
                'style': "satellite-streets",
                'center' : {
                    'lat': 6.240737,
                    'lon': -75.589900
                    },
                'zoom' : 9.5
            },
            'hovermode': 'closest',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
        }

    })
])
@app.callback(dash.dependencies.Output('encontrar','children'),[dash.dependencies.Input('datepicker','date'),dash.dependencies.Input('hora','value')])
def print_index(datepicker,hora):
   fecha_elegida=str(datetime.strptime(datepicker.split('T')[0],'%Y-%m-%d')+timedelta(hours=hora))
   band=True
   mensaje=' '
   for lec in range(len(fechas)):
       if (fechas[lec]==fecha_elegida):
           band=False
           mensaje='La fecha elegida es {}'.format(fecha_elegida)
   if band:
       mensaje='No se encontraron datos en la fecha elegida'
   return mensaje

@app.callback(dash.dependencies.Output('g1','figure'),[dash.dependencies.Input('datepicker','date'),dash.dependencies.Input('hora','value')])
def actualizar_figura(datepicker,hora):
   fecha_elegida=str(datetime.strptime(datepicker.split('T')[0],'%Y-%m-%d')+timedelta(hours=hora))
   band=True
   muestra=0
   for lec in range(len(fechas)):
       if (fechas[lec]==fecha_elegida):
           band=False
           muestra=lec
   if band:
       band = True
       muestra=0

   if (not band):
       """
       grid_z0 = griddata(puntos, valorpm[muestra], (grid_x, grid_y), method='nearest')
       grid_z2 = griddata(puntos, valorpm[muestra], (grid_x, grid_y), method='cubic')
       for k in range (len(grid_z2)):
           for p in range (len(grid_z2[k])):
               if np.isnan(grid_z2[k][p]):
                   grid_z2[k][p]=grid_z0[k][p]
       
       valorgrid2=[]
       for zg in grid_z2:
           for zp in zg:
               valorgrid2.append(zp)
       """
       figure = go.Figure(go.Densitymapbox(lat=latnew, lon=lonnew, z=zinterpolacion[muestra],radius=15))
       figure.update_layout(mapbox_style="satellite-streets", mapbox_center_lon=-75.589900,mapbox_center_lat= 6.240737)
       figure.update_layout(
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

       figure.show()

   else:
       figure={
               'data': [{
                 'lat': latitudes,
                 'lon': longitudes,
                 'text': nombres,
                 'marker': {
                     'color': '#00ff00',
                     'size': 10,
                     'opacity': 0.6
                 },
                 'style': "stamen-terrain",
                 'type': 'scattermapbox'
             }],

             'layout': {
                 'mapbox': {
                     'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
                     'style': "satellite-streets",
                     'center' : {
                         'lat': 6.240737,
                         'lon': -75.589900
                         },
                     'zoom' : 9.5
                 },
                 'hovermode': 'closest',
                 'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}

        }}
   return figure
if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False) #host = '0.0.0.0',  port=80

