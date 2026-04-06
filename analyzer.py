#Funcion para leer los archivos
def leer_archivo(nombre_archivo):
    lineas = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                lineas.append(linea.strip())
            return lineas
    except:
        print("El archivo no existe o no coincide. ")
        return []

#Import del regex (regular expressions) en python
import re

#Variable con los patrones a identificar
patrones = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"

#Input para el buscador
user = input("...")