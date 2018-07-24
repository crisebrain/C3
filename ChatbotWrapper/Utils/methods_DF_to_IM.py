import requests
import json

IM_FIELDS = "IM_fields"
IM_LINK = "http://localhost:5050/infomanager"

def post_data(jdata, link=IM_LINK):
    try:
        r = requests.post(link, data=jdata)
        # Ajustar salida si r no es la respuesta esperada
        return r.json()
    except:
        print("Falló la comunicación con IM.")

def updateIM(req:dict, fields: dict):
    # Gabriel revisa la forma en la que estas definiendo a req
    # y a fields en los parametros de la funcion
    req.update({IM_FIELDS: fields})
    post_data(req)
    # Recuerda que para mandar la peticion de busquedas a im
    # tienes que pasar el diccionario a json
    # con json.dumps(diccionario)
