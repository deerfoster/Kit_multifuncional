import csv

def generar_reporte_txt(datos, ruta_salida):
    try:
        with open(ruta_salida, "w", encoding='utf-8') as archivo:
            archivo.write("=== REPORTE DEL SISTEMA ===\n\n")

            for seccion, info in datos.items():
                archivo.write(f"--- {seccion.upper()} ---\n")
                if isinstance(info, dict):
                    for clave, valor in info.items():
                        archivo.write(f"{clave}: {valor}\n")
                else:
                    archivo.write(f"{info}\n")
                archivo.write("\n")

        print("Reporte TXT generado correctamente")

    except Exception as e:
        print("Error al generar reporte:", e)

def generar_reporte_csv(datos, ruta_salida):
    try:
        with open(ruta_salida, "w", newline="", encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Sección", "Elemento", "Valor"])

            for seccion, info in datos.items():
                if isinstance(info, dict):
                    for clave, valor in info.items():
                        writer.writerow([seccion, clave, valor])
                else:
                    writer.writerow([seccion, "Info", info])

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