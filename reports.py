def generar_reporte_txt(datos, ruta_salida):
    pass

def generar_reporte_csv(datos, ruta_salida):
    pass

def generar_reporte_general(organizacion, analisis, auditoria):
    pass

def generar_reporte_txt(datos, ruta_salida):
    try:
        with open(ruta_salida, "w") as archivo:
            archivo.write("=== REPORTE DEL SISTEMA ===\n\n")

            for seccion, info in datos.items():
                archivo.write(f"--- {seccion.upper()} ---\n")
                for clave, valor in info.items():
                    archivo.write(f"{clave}: {valor}\n")
                archivo.write("\n")

        print("Reporte TXT generado correctamente")

    except Exception as e:
        print("Error al generar reporte:", e)

import csv

def generar_reporte_csv(datos, ruta_salida):
    try:
        with open(ruta_salida, "w", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Sección", "Elemento", "Valor"])

            for seccion, info in datos.items():
                for clave, valor in info.items():
                    writer.writerow([seccion, clave, valor])

        print("Reporte CSV generado correctamente")

    except Exception as e:
        print("Error:", e)

def generar_reporte_general(organizacion, analisis, auditoria):
    datos = {
        "organizacion": organizacion,
        "analisis": analisis,
        "auditoria": auditoria
    }

    generar_reporte_txt(datos, "reporte.txt")
    generar_reporte_csv(datos, "reporte.csv")