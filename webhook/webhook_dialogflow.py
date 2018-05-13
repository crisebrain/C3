import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True, force=True)
    # print("Request")
    # print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

def makeWebhookResult(req):
    if req.get("queryResult").get("action") == "VDN":
        return makeresponseVDN(req)

def makeresponseVDN(req):
    from bd_busqueda import BDbusquedas
    bd = BDbusquedas()
    result = req.get("queryResult").get("parameters")
    coincidencias = bd.busqueda(result.get("personname"))
    print(json.dumps(coincidencias, indent=4))
    returnCode = calcCode(coincidencias)
    textresp = mensajson(coincidencias, returnCode)
    resp = {"result":coincidencias,
            "returnCode": returnCode,
            "source": req.get("queryResult").get("intent").get("displayName"),
            "displayText": textresp,
            "speech": textresp}
    return resp

def calcCode(array):
    ncoincidencias = len(array)
    if ncoincidencias == 0:
        code = 0
    elif ncoincidencias == 1:
        code = 1
    elif ncoincidencias < 4:
        code = 2
    else:
        code = 3
    return code

def mensajson(array, code):
    if code == 0:
        Text = "No hay referencia de esa persona"
    elif code == 1:
        elem = array[0]
        Text = "El telefono de {0} {1} es {2}".format(elem["Nombre"],
                                                      elem["Apellido"],
                                                      elem["telefono"])
    elif code == 2:
        textnames = [elem["Nombre"] + " " + elem["Apellido"] for elem in array]
        textnames = ' o '.join(textnames)
        Text = "¿A cual persona te refieres? a {0}".format(textnames)
    else:
        Text = "Tengo {0} coincidencias, necesitas ser mas especifico".format(len(array))
    return Text

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
