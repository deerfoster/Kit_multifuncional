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

#Funcion para identificar los patrones emails, números, fechas o palabras clave
def busqueda_archivo(archivo , nombre):
#Variable con los patrones a identificar
    patrones = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "telefono": r"\+?\d{10,12}",
        "fecha": r"\d{2}/\d{2}/\d{4}",
        "palabras_clave": r"\b[a-zA-Z]{8,}\b"
    }

    coincidencias = []
    
    #Input para el buscador
    user = input("Archivo: nombre ")