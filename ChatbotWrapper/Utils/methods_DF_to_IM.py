import requests
import json
import sys

IM_FIELDS = "IM_fields"
IM_LINK = "http://localhost:5050/infomanager"

def post_data(jdata, link=IM_LINK):
    """
    Función de comunicación genérica hacia cualquier WS/WH.
    :param jdata: datos que se pasan al WS.
    :param link: EndPoint del WS.
    :return: Respuesta del WS.
    """
    try:
        r = requests.post(link, data=json.dumps(jdata))
        # Ajustar salida si r no es la respuesta esperada
        return r.json()
    except requests.exceptions.ConnectionError:
        print("Falló la conexión a {}".format(link))
        return sys.exc_info()
    except:
        print(sys.exc_info())
        return sys.exc_info()


def updateIM(req:dict, fields: dict):
    """
    Esta función se comunica con el IM, para que actualice los valores del
    árbol del conference con los campos que se pasan en fields.

    :param req: Petición original. Estilo DF.
    :param fields: Diccionario de campos, con nombre y valor de cada uno de los campos que se quieren actualizar.
    :return: Respuesta del IM.
    """
    req.update({IM_FIELDS: fields})
    return post_data(req)


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
