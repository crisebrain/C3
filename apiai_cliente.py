#!/home/ebraintec/anaconda3/bin/python
#-*- coding: utf-8 -*-
import json
import os
import apiai
import ast
from flask import Flask, make_response, request
import pandas as pd
from Services.bd_busqueda import normaliza

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
    df.to_html("metadata/temp.html", table_id="t01")
    stringout = open("metadata/temp.html", "r").read()
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
    df.to_html("metadata/temp.html", table_id="t00")
    stringout = open("metadata/temp.html", "r").read()
    return stringout

def Chat(text="", leng="es", id="123456" ):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = leng
    request.session_id = id
    request.query = text
    response = request.getresponse()
    plantilla = open("metadata/plantilla_tabla.html", 'r').read()
    results = json.loads(response.read().decode("utf-8"))
    print(results)
    try:
        salida_tabla = results["result"]["fulfillment"]["data"]["resultOut"]
        entrada_tabla = results["result"]["fulfillment"]["data"]["resultIn"]
        googleSpeech = results["result"]["fulfillment"]["messages"][0]["speech"]
        formatotexto = '<br><font face="verdana">{0}</font><br><br>'
        if len(googleSpeech) < 200:
            msg = formatotexto.format("Valores identificados:") + superPandasEntrada(entrada_tabla)
            msg +=  "<br>" + googleSpeech
        else:
            msg = formatotexto.format("Valores identificados:") + superPandasEntrada(entrada_tabla)
            msg += formatotexto.format("Resultados:") + superPandasRespuesta(salida_tabla)
        msg = plantilla + msg
    except KeyError:
        googleSpeech = results["result"]["fulfillment"]["messages"][0]["speech"]
        # msg = "Los parametros ingresados no generan una respuesta valida."
        msg = normaliza(googleSpeech)
    # msg = ""superPandasEntrada(entrada_tabla) + superPandasRespuesta(salida_tabla)
    complemento = '<br><br><input type="button" onclick="javascript:history.go(-1)" value="regresar">'
    return msg + complemento

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
