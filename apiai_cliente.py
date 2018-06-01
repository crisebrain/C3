#-*- coding: utf-8 -*-
import json
import os
import apiai
import ast
from flask import Flask, make_response, request
import pandas as pd

CLIENT_ACCESS_TOKEN = '28165eab709744ca9efbcf21e9519df5'

def superPandasRespuesta(lista_dicc):
    columns = ['NumeroDocumento', 'FechaEmision', 'Monto', 'NITAdquiriente',
               'NombreAdquiriente', 'NITFacturador', 'Estatus', 'Acuse',
               'Referencia']
    df = pd.DataFrame(columns=columns)
    for dicc in lista_dicc:
        dicpeq = dict()
        for key, value in dicc.items():
            if (value is None) or (value == "?"):
                dicpeq.update({key:" "})
            else:
                dicpeq.update({key:value})
        df = df.append(dicpeq, ignore_index=True)
    df.fillna(" ", inplace=True)
    df.to_html("temp.html", table_id="t01")
    stringout = open("temp.html", "r").read()
    return stringout

def superPandasEntrada(dicc):
    columns = ["periodo", "estado", "numFactura",
               "prefijo", "acuse", "factura"]
    df = pd.DataFrame(columns=columns)
    dicpeq = dict()
    for key, value in dicc.items():
        if (value is None) or (value == "?"):
            dicpeq.update({key:" "})
        else:
            dicpeq.update({key:value})
    df = df.append(dicpeq, ignore_index=True)
    df.fillna(" ", inplace=True)
    df.to_html("temp.html", table_id="t00")
    stringout = open("temp.html", "r").read()
    return stringout

def Chat(text="", leng="es", id="123456" ):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = leng
    request.session_id = id
    request.query = text
    response = request.getresponse()
    print(response)
    results = json.loads(response.read().decode("utf-8"))
    try:
        salida_tabla = results["result"]["fulfillment"]["data"]["resultOut"]
        entrada_tabla = results["result"]["fulfillment"]["data"]["resultIn"]
        googleSpeech = results["result"]["fulfillment"]["messages"][0]["speech"]
        if len(googleSpeech) < 200:
            msg = "Valores identificados: <br>" + superPandasEntrada(entrada_tabla)
            msg +=  "<br>" + googleSpeech
        else:
            msg = "Valores identificados: <br>" + superPandasEntrada(entrada_tabla)
            msg += "<br> Resultados: <br>" + superPandasRespuesta(salida_tabla)
    except KeyError:
        msg = "Disculpe, su peticion no corresponde al servicio de facturas."
    # msg = ""superPandasEntrada(entrada_tabla) + superPandasRespuesta(salida_tabla)
    return msg

app = Flask(__name__)

@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("Ya Jala")
    return r

@app.route("/apiaipythoncliente", methods=["POST"])
def conversa():
    # req = request.get_json(silent=True, force=True)
    req = ast.literal_eval(request.form["json"])  # .get_json(silent=True, force=True)
    response = Chat(req["reqText"])
    # response = json.dumps({'fulfillmentText': response},
    #                       indent=4)
    r = make_response(response)
    r.headers["Content-Type"] = "text/html"
    r.headers["charset"] = "UTF-8",
    return r

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5010))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
