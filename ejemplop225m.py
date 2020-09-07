import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

customer_json_file ='Datos_SIATA_Aire_pm25.json'
customers_json = pd.read_json(customer_json_file, convert_dates=True)
latitudes = customers_json.latitud.values.tolist()
longitudes = customers_json.longitud.values.tolist()
fechas = []
m=[]
for i in range(len(customers_json.datos[0])):
    cant = []
    for l in range(21):
        cant.append(customers_json.datos[l][i].get('valor'))
    m.append(cant)
    
for r in range(len(customers_json.datos[1])):
    fechas.append(customers_json.datos[1][r].get('fecha'))
    
# en la variable m esta el nivel de la ultima
puntos = []
lat = []
long = []
for cor in range(len(longitudes)):
    p = [longitudes[cor],latitudes[cor]]
    lat.append(latitudes[cor])
    long.append(longitudes[cor])
    puntos.append(p)
        
grid_x, grid_y = np.mgrid[np.min(longitudes):np.max(longitudes):100j, np.min(latitudes):np.max(latitudes):100j]

grid_z0 = griddata(puntos, m[0], (grid_x, grid_y), method='nearest')
grid_z1 = griddata(puntos, m[0], (grid_x, grid_y), method='linear')
grid_z2 = griddata(puntos, m[0], (grid_x, grid_y), method='cubic')

for g in range (len(grid_z1)):
    for l in range (len(grid_z1[g])):
        if np.isnan(grid_z1[g][l]):
            grid_z1[g][l]=grid_z0[g][l]

for k in range (len(grid_z2)):
    for p in range (len(grid_z2[k])):
        if np.isnan(grid_z2[k][p]):
            grid_z2[k][p]=grid_z0[k][p]
 
plt.subplot(221)
#plt.imshow(, extent=(np.min(longitudes),np.max(longitudes), np.min(latitudes),np.max(latitudes)), origin='lower')
plt.plot(long, lat, 'xb', ms=4)
plt.title('Original')
plt.subplot(222)
plt.contourf(grid_x, grid_y, grid_z0)
plt.plot(long, lat, 'xr', ms=1)
plt.colorbar()
plt.title('Nearest')
plt.subplot(223)
plt.contourf(grid_x, grid_y, grid_z1)
plt.plot(long, lat, 'k.', ms=1)
plt.title('Linear')
plt.colorbar()
plt.subplot(224)
plt.contourf(grid_x, grid_y, grid_z2)
plt.plot(long, lat, 'k.', ms=1)
plt.title('Cubic')
plt.colorbar()
#plt.gcf().set_size_inches(12, 12)
plt.show()
"""
for w in range(len(fechas)):
    if (fechas[w] == '2019-04-03 19:00:00'):
        print(w)
"""
longitud_grid = []
for t1 in grid_x:
    for lo in t1:
        longitud_grid.append(lo)
