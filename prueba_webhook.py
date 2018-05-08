import time
from flask import Flask, request, make_response, jsonify
import json
app = Flask(__name__)
log = app.logger

@app.route("/vdn", methods=["POST"])
def webhook_vdn():
    req = request.get_json(silent=True, force=True)
    print("el telefono de {0}".format(req))
    print(json.dumps(req))
    res = "5541284922"
    return make_response(jsonify({'telefono': res}))

@app.route("/saldo", methods=["POST"])
def webhook_saldo():
    req = request.get_json(silent=True, force=True)
    print("Tu saldo es 13.00")
    print(req)
    res = "13.00"
    return make_response(jsonify({'saldo': res}))

app.run(debug=True, host="0.0.0.0")
