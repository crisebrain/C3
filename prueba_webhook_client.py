import time
# from flask import Flask, request, make_response, jsonify
import json
import requests

def post_data(jdata):
    r = requests.post("http://0.0.0.0:5000/vdn", data=jdata)
    print(r.json())
    # Ajustar salida si r no es la respuesta esperada
    return True

if __name__ == "__main__":
    payload = {"first_name": "Ramon",
               "last_name": "Aparicio"}
    post_data(payload)
