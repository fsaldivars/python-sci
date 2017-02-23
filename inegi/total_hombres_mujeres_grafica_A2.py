import json

import matplotlib.pyplot as plt
import requests

TOKEN = "3e4bac1e-07ad-2db4-44d4-fc13628338b2"
w = 0.4

def add(X, w):
    return [x + w for x in X]

URL_API = "http://www3.inegi.org.mx/sistemas/api/indicadores/v1/Indicador"

for a in range(33):
    area = "0%d" % a if a < 10 else str(a)
    labels = ['Hombres', 'Mujeres']
    url_hombres = "%s/1002000002/%s/es/false/json/%s" % (URL_API, area, TOKEN)
    url_mujeres = "%s/1002000003/%s/es/false/json/%s" %(URL_API, area, TOKEN)
    json_hombres = json.loads(requests.get(url_hombres).content)
    json_mujeres = json.loads(requests.get(url_mujeres).content)

    len_series = len(json_mujeres["Data"]["Serie"])
    total_hombres = []
    total_mujeres = []
    periodosH = []
    periodosM = []

    for serie in range(len_series):
        periodosH.append(int(json_hombres["Data"]["Serie"][serie]["TimePeriod"]))
        periodosM.append(int(json_hombres["Data"]["Serie"][serie]["TimePeriod"]))
        total_hombres.append(int(json_hombres["Data"]["Serie"][serie]["CurrentValue"]))
        total_mujeres.append(int(json_mujeres["Data"]["Serie"][serie]["CurrentValue"]))



    fig, ax = plt.subplots()
    barraHombres = ax.bar(periodosH, total_hombres, w, color='blue')

    barraMujeres = ax.bar(add(periodosM,w), total_mujeres, w, color='pink')
    ax.legend((barraHombres[0], barraMujeres[0]), labels)


    nombre_region = json_hombres["MetaData"]["Region"]
    nombre_archivo = "img_a2/%s. %shist.png" % (area, nombre_region.replace(",", " - "))
    plt.savefig(nombre_archivo)