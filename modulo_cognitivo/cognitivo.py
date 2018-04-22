# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:33:33 2018

@author: crisebrain
"""

def cognitive_req(data):
    """
    recive un arreglo json que contiene al menos un campo
    y cuyo campo es 'msgOriginal'
    """
    msg = data['msgOriginal']
    print("El mensaje original recibido es:", msg)
    
    nodo1 = {"id": "direccion",
             "value": "Reforma 27",
             "acc": 98.7,
             "obligatorios": "direccion",
             "txtEntrada": msg,
             }
    nodosList = [nodo1]
    return nodosList