import requests

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
    req.update({IM_FIELDS: fields})
    post_data(req)
