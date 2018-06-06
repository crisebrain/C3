import requests
import json

def sendReq(jdata, link, authorization):
    # ---------------------------------------------------------------------
    headers = {"Content-Type": "application/json",
               "Authorization": authorization,
               "charset": "UTF-8"}
    req = requests.post(link,
                        data=json.dumps(jdata, indent=4), headers=headers)
    return req


if __name__ == "__name__":
    link = "https://dialogflow.googleapis.com/v2/projects/chatfase1/agent/sessions/4fe0f059:detectIntent"
    token = "ya29.c.El_QBQWnd2RGa4q3OlSFseyRPS_NBrH3D40iWeALXy6goUq4I05M0uIrWuTaWcolTxg27zozBNX5rCqdCI6jSukvTyrKIUc8zXi6dJwBucgdsmwEXbe7U9lAburX6xVliA"
    authTok = "Bearer {0}".format(token)
    data = {"queryInput": {"event": {"name": "salida",
                                     "parameters": {"prueba": "1"},
                                     "languageCode": "es"}},
            "queryParams": {"timeZone": "America/Mexico_City"}}
    req = sendReq(data, link, authTok)
    print(req.json())
