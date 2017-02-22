import requests
import matplotlib.pyplot as plt
import json




TOKEN = "a6c7400e-5a2f-32cd-b2cf-b9d0c4609a07"
URL_API = "http://www3.inegi.org.mx/sistemas/api/indicadores/v1/Indicador"

import sci

datos = sci.load_xl("/home/fsaldivar/Documents/python/Proyecto-sci/inegi/estados.xlsx", "Hoja2", "A1:E9")

for data in datos:
    areas = sci.data_extract(datos, "AREA")
    for a in areas:
        area = "0%d" % a if a < 10 else str(a)
        url_ingreso = "%s/6200240329/%s/es/true/json/%s" % (URL_API, area, TOKEN)
        url_gasto = "%s/6200240360/%s/es/true/json/%s" %(URL_API, area, TOKEN)

        json_ingreso = json.loads(requests.get(url_ingreso).content)
        json_gasto = json.loads(requests.get(url_gasto).content)

        ingreso = float(json_ingreso["Data"]["Serie"][0]["CurrentValue"])
        gasto = float(json_gasto["Data"]["Serie"][0]["CurrentValue"])

        nvl_riqueza = (2 * ingreso - gasto) / (ingreso + gasto)

