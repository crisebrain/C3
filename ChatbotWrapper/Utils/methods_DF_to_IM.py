import requests

IM_FIELDS = "IM_fields"

def post_data(jdata, link="http://localhost:5050/infomanager"):
    r = requests.post(link, data=jdata)
    # Ajustar salida si r no es la respuesta esperada
    return r.json()

def updateIM(req:dict, fields: dict):
    req.update({IM_FIELDS: fields})
    print(req)

