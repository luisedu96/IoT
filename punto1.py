import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, date, time, timedelta

app = dash.Dash()   #6.2386048,-75.5858882,15z

customer_json_file ='Datos_SIATA_Aire_pm25.json'
customers_json = pd.read_json(customer_json_file, convert_dates=True)
latitudes = customers_json.latitud.values.tolist()
longitudes = customers_json.longitud.values.tolist()
fechas = []
valorpm=[]
date=' '

for i in range(len(customers_json.datos[0])):
    cant = []
    for l in range(len(customers_json.datos)):
        cant.append(customers_json.datos[l][i].get('valor'))
    valorpm.append(cant)

for f in range(len(customers_json.datos[0])):
    fechas.append(customers_json.datos[0][f].get('fecha'))

app.layout = html.Div([
    html.H1(id='Title1',children='Mapa de visualización de los valores de PM2.5',style={'color':'#3A65A6','text-align':'center'}),
    html.Div('Graficando el mapa',id='c1'),
    html.Div(id='encontrar'),
    html.Div('Ahora vamos a programar un slider para mostrar datos'),
    dcc.Slider(id='barra1',min=0,max=9,step=1,value=0),
    html.Div('Elige la hora'),
    dcc.Slider(id='hora',min=0,max=23,marks={i: '{} horas'.format(i) for i in range(24)},value=0),
    html.Div(id='texto1'),
    dcc.DatePickerSingle(id='date-picker-single',date=datetime(2019, 2, 21, 0, 0, 0)),
    dcc.Graph(id='g1',figure={
          'data': [{
            'lat': latitudes,
            'lon': longitudes,
            'marker': {
                'color': '#00ff00',
                'size': 10,
                'opacity': 0.6
            },
            'type': 'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
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

@app.callback(dash.dependencies.Output('texto1','children'),[dash.dependencies.Input('barra1','value')])
def actualizar_texto(value):
   return 'la fecha observada es "{}"'.format(fechas[value])
@app.callback(dash.dependencies.Output('encontrar','children'),[dash.dependencies.Input('date-picker-single','date')],[dash.dependencies.Input('hora','value')] )
def print_index(date,value):
   fecha_elegida=str(datetime.strptime(date.split('T')[0],'%Y-%m-%d')+timedelta(hours=value))
   band=True
   muestra=0
   mensaje=' '
   for lec in range(len(fechas)):
       if (fechas[lec]==fecha_elegida):
           band=False
           muestra=lec
   if band:
       mensaje='no se encontraron datos en la fecha elegida'
       muestra=' '
   return 'la fecha elegida es {} y el numero de muestra es {} {}'.format(fecha_elegida, muestra, mensaje)

@app.callback(dash.dependencies.Output('g1','figure'),[dash.dependencies.Input('date-picker-single','date')],[dash.dependencies.Input('hora','value')])
def actualizar_figura(date,value):
   fecha_elegida=str(datetime.strptime(date.split('T')[0],'%Y-%m-%d')+timedelta(hours=value))
   band=True
   muestra=0
   for lec in range(len(fechas)):
       if (fechas[lec]==fecha_elegida):
           band=False
           muestra=lec
   if band:
       band = True
       muestra=0

   latitudnueva = latitudes
   longitudnueva = longitudes
#  temperaturanueva = temperatura[value]
#  mnuevo = valorpm[muestra]
   if (not band):
       figure={
             'data': [{
                 'lat': latitudnueva,
                 'lon': longitudnueva,
                 'marker': {
                     'color': valorpm[muestra],
                     'size': valorpm[muestra],
                     'opacity': 0.6
                 },
                 'type': 'scattermapbox'
             }],

             'layout': {
                 'mapbox': {
                     'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
                     'center' : {
                         'lat': 6.240737,
                         'lon': -75.589900
                         },
                     'zoom' : 9.5
                 },
                 'hovermode': 'closest',
                 'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}

        }}
   else:
       figure={
               'data': [{
                 'lat': latitudnueva,
                 'lon': longitudnueva,
                 'marker': {
                     'color': '#00ff00',
                     'size': 10,
                     'opacity': 0.6
                 },
                 'type': 'scattermapbox'
             }],

             'layout': {
                 'mapbox': {
                     'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
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
    app.run_server()

