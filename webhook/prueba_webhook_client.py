import time
# from flask import Flask, request, make_response, jsonify
import json
import requests

def post_data(jdata):
    r = requests.post("http://0.0.0.0:5000/webhook", data=jdata)
    print(json.dumps(r.json(), indent=4))
    # Ajustar salida si r no es la respuesta esperada
    return True

if __name__ == "__main__":
    filejson = open("query_VDN.json", "r")
    # Simula el query de DialogFlow
    payload = json.load(filejson)
    post_data(json.dumps(payload, indent=4))
