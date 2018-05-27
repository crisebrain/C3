#-*- coding: utf-8 -*-
import time
import json
import requests

def post_data(jdata, link="http://0.0.0.0:5050/infomanager"):
    r = requests.post(link, data=jdata)
    print(json.dumps(r.json(), indent=4))
    # Ajustar salida si r no es la respuesta esperada
    return True


def send_request(filejsonname):
    filejson = open(filejsonname, "r")
    # Simula el query de DialogFlow
    payload = json.load(filejson)
    post_data(json.dumps(payload, indent=4))

if __name__ == "__main__":
    send_request("query_default_fallback.json")
