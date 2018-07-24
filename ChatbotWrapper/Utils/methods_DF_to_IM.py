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


def extractData(phrase: str, list_params: list):
    """
    Esta función se comunica con el IM, para que extraiga los información
    con respecto a los parámetros que se dan para una frase.

    :param phrase: Frase a procesar
    :param list_params: Parámetros de los cuales queremos extraer la información
    :return: información que se encontró que corresponde a la lista de parámetros
    """
    req = {
        "action": "obtieneDatos",
        "datos": {
            "frase": phrase,
            "campos": list_params
        }
    }
    return post_data(req)
