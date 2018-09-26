from ChatbotWrapper.DF.intentLogic import analizeReq
import json
from pprint import pprint

with open('ChatbotWrapper/DF/MyHuman/myhuman.json') as f:
    specjson = json.load(f)

def respfact(req: dict):
    response = analizeReq(req)
    return response
