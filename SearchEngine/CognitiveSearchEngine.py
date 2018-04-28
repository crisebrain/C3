# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:33:33 2018

@author: crisebrain
"""

def cognitive_req(respuesta):
    """
    recive un arreglo json que contiene al menos un campo
    y cuyo campo es 'msgOriginal'
    """
    msg = data['msgOriginal']


    nodo1 = {"name":"Ampliacion", "value": respuesta,
             "parent":"TarjetaCredito",
             "idChatBot":idChatBot,
             "msgAns":"Tu respuesta es {0}".format(respuesta)}
    print("El mensaje original recibido es:", nodo1["msgAns"])
    #nodosList = [nodo1]
    return nodo1
