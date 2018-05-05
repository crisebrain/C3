# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:33:33 2018

@author: crisebrain
"""

def cognitive_req(data):
    """
    recibe un arreglo json que contiene al menos un campo
    y cuyo campo es 'msgOriginal'
    """
    msg = data['msgReq']
    print("El mensaje original recibido es:", msg)
    value = 20000
    nodo1 = {"idField": "credito",
             "value": 20000,
             "name": "Ampliacion",
             "acc": 98.7,
             "mandatory": "direccion",
             "txtEntrada": msg,
             "msgAns": "Si hay ampliacion por %d" %value
             }
    nodosList = [nodo1]
    return nodosList
