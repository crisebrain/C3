# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:33:33 2018

@author: crisebrain
"""

"""
Modified on Sat May 12 2018

@author: ffernare
"""
import pickle
import json
import requests
import re

"""Class to manage the conversation and publish the IntentTree"""
class CognitiveSearchEngine:
    def __init__(self, IdChatBot):
        # retrieve current intentTree
        conference = pickle.load(open('./Sessions/Conference.pck','rb'))
        for intentTree in conference:
            if intentTree.idChatBot == IdChatBot:
                self.currentIntentTree = intentTree
                # falta incluir que dado el IdChatBot, se cargue el modelo de ese chatbot en particular.
                self.currentModel = None
                
    def parse_user_message(self,data):
        """
        Recibe un objeto json que contiene un campo 'msgReq'
        """
        msg = data['msgReq']
        url = "http://text-processing.com/api/phrases/"
        #url="http://text-processing.com/api/tag/"
        data='language=spanish&text='+msg
        headers = {'content-type': 'application/json; charset=utf-8'}
        r = requests.post(url, data=data,headers=headers)        
        """
        Devuelve una lista que contiene el label de la entidad y el nombre extraído.
        """
        output = r.json()
        output["numbers"]=re.findall(r'(\d+)', msg)
        return json.dumps(output)
    
    def predict_intents(self,data, idChatBot):
        msg = data['msgReq']
        # check if idChatBot is currently loaded, if not update currentIntentTree and currentModel
        # hacer el preprocesado de data generando embeddings de msg.
        # hacer el predict utilizando msg como entrada y obteniendo los acc por cada clase.
        # construir array_list utilizando la secuencia de intents conocida y los acc generados.
        output = {"intents":array_list}        
        return json.dumps(output)
    
    def build_model(self,dataset):
        """
        construir el modelo utilizando el dataset en formato [message, class], utilizar word embeddings 
        previamente entrenados para el español. La arquitectura puede ser unas capas de LSTM o GRU, 
        utilizar categorical_cross_entropy, salvar el modelo en hdf5 y ponerlo en sesión ocupando el idChatBot como nombre 
        del archivo.
        """

if __name__ == "__main__":
    cse = CognitiveSearchEngine("testing-b6df8")
    data = {"msgReq": u"Me llamo Juan Gil, vivo en México y quiero contratar un seguro en Profuturo"} 
    print(data["msgReq"])
    print(cse.parse_user_message(data))
    data = {"msgReq": u"Mi nombre es Teresa Santos, y necesito una hipoteca del Banco Banamex"}
    print(data["msgReq"])
    print(cse.parse_user_message(data))
    data = {"msgReq": u"Mi nombre es Gerardo Sánchez y tengo 40 años"}
    print(data["msgReq"])
    print(cse.parse_user_message(data))
    