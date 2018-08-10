#!/home/ebraintec/anaconda3/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys

from flask import Flask, request, make_response

from Services import makeWebhookResult

app = Flask(__name__)


@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


if __name__ == "__main__":
    if len(sys.argv) > 1:
        portnumber = int(sys.argv[1])
    else:
        portnumber = 5000
    port = int(os.getenv("PORT", portnumber))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
