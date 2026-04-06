#Import del regex
import re

#Funcion para leer los archivos
def leer_archivo(nombre_archivo):
    #encoding='utf-8' es para detectar carácteres especiales
    #como ñ o acentos.
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                yield linea.strip()
    except:
        print("El archivo no existe o no coincide. ")

#Funcion para identificar los patrones.
def busqueda_archivo(nombre , tipo):
#Variable con los patrones a identificar
    patrones = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "telefono": r"\+?\d{10,12}",
        "fecha": r"\d{2}/\d{2}/\d{4}",
        "palabras_clave": r"\b[a-zA-Z]{8,}\b"
    }

    patron = patrones.get(tipo)
    coincidencias = []

    if patron:
        for linea in leer_archivo(nombre):
            coincidencia_linea = re.findall(patron , linea)
            coincidencias.extend(coincidencia_linea)
    return coincidencias

#Input + buscador
user_archivo = input("Nombre del archivo: ")
user_tipo = input("Qué tipo de archivo desea buscar? (email/telefono/fecha/palabra clave)")

resultado = busqueda_archivo(user_archivo , user_tipo)

print(f"Se hallaron {len(resultado)} coincidencias: ")

for i in resultado:
    print(f"- {i}")