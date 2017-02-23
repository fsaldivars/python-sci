import matplotlib.pyplot as plt
import re
import sci


URL_FILE = "/home/fsaldivar/Documents/python/python-sci/inegi/"

datos = sci.load_xl("%smapa_riqueza.xlsx" %(URL_FILE), "Hoja1", "A1:F9")

indicador_riqueza = "Indicador"

def buscar_menor(datos):
    pivote = datos[0][indicador_riqueza]
    total_elemetos = len(datos)
    
    for i in range(0, total_elemetos):
        if datos[i][indicador_riqueza] < pivote:
            pivote = datos[i][indicador_riqueza]
    
    return pivote

def buscar_mayor(datos):
    pivote = datos[0][indicador_riqueza]
    total_elemetos = len(datos)
    
    for i in range(0, total_elemetos):
        if datos[i][indicador_riqueza] > pivote:
            pivote = datos[i][indicador_riqueza]
    
    return pivote
"""
Obtiene las coordenas y las interpreta a al long entendible en el mapa
"""
def latlon(coordenada):
     r = re.search("(\d+).(\d+).(\d+)..(\w)", coordenada)
     
     g = int(r.group(1))
     m = int(r.group(2))
     s = int(r.group(3))

     return g + m / 60.0 + s / 3600.0

indice_riqueza_menor = buscar_menor(datos)
indice_riqueza_mayor = buscar_mayor(datos)

data_nivel_riqueza = []

for r in datos:
    riqueza = r[indicador_riqueza]
    color = int(3 * (riqueza - indice_riqueza_menor) / (indice_riqueza_mayor - indice_riqueza_menor))
    r["Color"] = color
    data_nivel_riqueza.append(r)


sci.write_xl("%smapa_riqueza_B2.xlsx" %(URL_FILE), "Hoja1", "A1", data_nivel_riqueza, ["NOMBRE_ENTIDAD", "AREA", "CAPITAL", "Latitud", "Longitud", "Indicador", "Color"])


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

map = Basemap(projection='cea',
    llcrnrlat=0, urcrnrlat=50,
    llcrnrlon=-120, urcrnrlon=-80)

map.drawmapboundary(fill_color="blue")
map.fillcontinents(color="coral", lake_color="yellow")

lats = sci.data_map(data_nivel_riqueza, lambda ruta: latlon(ruta["Latitud"]))
lons = sci.data_map(data_nivel_riqueza, lambda ruta: -latlon(ruta["Longitud"]))

latlons = zip(lats, lons)

XY = sci.data_map(latlons, lambda (lat, lon): map(lon, lat))

X = sci.data_map(XY, lambda (x, y): x)
Y = sci.data_map(XY, lambda (x, y): y)

plt.plot(X, Y)
plt.plot(X, Y, "ro")

plt.savefig("mapa_riqueza.jpg")








