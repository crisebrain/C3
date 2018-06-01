import json
import os
import apiai
import ast
from flask import Flask, make_response, request

CLIENT_ACCESS_TOKEN = '28165eab709744ca9efbcf21e9519df5'
def Chat(text="",leng="es",id="123456" ):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = leng
    request.session_id = id
    request.query = text
    response = request.getresponse()
    results = json.loads(response.read().decode("utf-8"))
    googleSpeech = results["result"]["fulfillment"]["messages"][0]["speech"]
    return googleSpeech

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
    response = json.dumps({'fulfillmentText': response},
                          indent=4)
    r = make_response(response)
    r.headers["Content-Type"] = "application/json"
    return r

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5010))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
