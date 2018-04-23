# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:33:33 2018

@author: crisebrain
"""
from modulo_cognitivo.cognitivo import cognitive_req

"""
el modulo  cognitive_req
recibe como entrada un json que indica cual fue el mensaje original del usuario

lo que se recibe como respuesta en una lista que contiene todos los objeto
nodos identificados
"""

data = {'msgOriginal': "hola esta es una prueba"}
#ejemplo de la informacion que debe contener los datos pasados a la funcion cognitive_req

res = cognitive_req( data )
#res almacenara la lista de nodos identificado en el modulo cognitivo dado el string de entrada

for i,x in enumerate(res):
	print ('nodo num {:d} \t informacion contenida en el nodo: {:s} '.format(i, x))