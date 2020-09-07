import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_excel('datamedellinmapa.xls')

app.layout = html.Div([
    html.H1('Covid 19 en el valle de Aburrá'),
    html.Div('hola mundo',id='text-content'),
    dcc.Graph(id='map', figure={
        'data': [{
            'lat': df['lat'],
            'lon': df['lon'],
            'marker': {
                'color': 150,
                'size': df['enfermos'],
                'opacity': 0.6
            },
            'customdata': df['riesgo'],
            'type': 'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
                'center' : {
                    'lat': 6.240737,
                    'lon': -75.589900
                    },
                'zoom' : 10
            },
            'hovermode': 'closest',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
        }
    })
])


if __name__ == '__main__':
    app.run_server(debug=True,port=80)
