import os
import shutil
import re
from datetime import datetime

def auditor_decorador(funcion):
    def envoltura(*args, **kwargs):
        print(f"[SISTEMA] Ejecutando: {funcion.__name__}")
        try:
            return funcion(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] No se pudo completar {funcion.__name__}: {e}")
            return {}
    return envoltura

@auditor_decorador
def clasificar_por_extension(ruta_carpeta, modo_prueba=False):
    mapa = {
        '.txt': 'Textos', '.pdf': 'Documentos', '.docx': 'Documentos',
        '.jpg': 'Imágenes', '.jpeg': 'Imágenes', '.png': 'Imágenes',
        '.mp3': 'Música', '.mp4': 'Videos', '.py': 'Código',
        '.csv': 'Datos', '.xlsx': 'Datos', '.zip': 'Comprimidos'
    }
    contador = {}
    if not os.path.exists(ruta_carpeta):
        return {}
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa):
            continue
        _, extension = os.path.splitext(archivo)
        extension = extension.lower()
        carpeta = mapa.get(extension, 'Otros') 
        ruta_destino = os.path.join(ruta_carpeta, carpeta)
        contador[carpeta] = contador.get(carpeta, 0) + 1
        if modo_prueba:
            print(f"[SIMULACIÓN] Mover {archivo} a {carpeta}/")
        else:
            os.makedirs(ruta_destino, exist_ok=True)
            shutil.move(ruta_completa, os.path.join(ruta_destino, archivo))
    return contador

@auditor_decorador
def clasificar_por_tamanio(ruta_carpeta, modo_prueba=False):
    contador = {'pequeños': 0, 'medianos': 0, 'grandes': 0}
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa): continue
        tamanio_mb = os.path.getsize(ruta_completa) / (1024 * 1024)
        if tamanio_mb < 1:
            cat, carpeta = 'pequeños', 'Pequeños'
        elif tamanio_mb <= 10:
            cat, carpeta = 'medianos', 'Medianos'
        else:
            cat, carpeta = 'grandes', 'Grandes'
        contador[cat] += 1
        ruta_destino = os.path.join(ruta_carpeta, carpeta)
        if modo_prueba:
            print(f"[SIMULACIÓN] Mover {archivo} ({tamanio_mb:.2f} MB) a {carpeta}/")
        else:
            os.makedirs(ruta_destino, exist_ok=True)
            shutil.move(ruta_completa, os.path.join(ruta_destino, archivo))
    return contador

@auditor_decorador
def clasificar_por_fecha(ruta_carpeta, modo_prueba=False):
    hoy = datetime.now()
    contador = {'hoy': 0, 'esta_semana': 0, 'este_mes': 0, 'antiguos': 0}
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa): continue
        fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
        diferencia = (hoy - fecha_mod).days
        if diferencia == 0:
            cat, carpeta = 'hoy', 'Modificados_Hoy'
        elif diferencia <= 7:
            cat, carpeta = 'esta_semana', 'Esta_Semana'
        elif diferencia <= 30:
            cat, carpeta = 'este_mes', 'Este_Mes'
        else:
            cat, carpeta = 'antiguos', 'Antiguos'
        contador[cat] += 1
        ruta_destino = os.path.join(ruta_carpeta, carpeta)
        if modo_prueba:
            print(f"[SIMULACIÓN] Mover {archivo} (Modificado: {fecha_mod.strftime('%Y-%m-%d')}) a {carpeta}/")
        else:
            os.makedirs(ruta_destino, exist_ok=True)
            shutil.move(ruta_completa, os.path.join(ruta_destino, archivo))
    return contador

@auditor_decorador
def renombrar_con_regex(ruta_carpeta, patron, nuevo_nombre, modo_prueba=False):
    try:
        patron_regex = re.compile(patron)
    except re.error:
        return 0
    contador = 0
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa): continue
        if patron_regex.search(archivo):
            _, extension = os.path.splitext(archivo)
            contador += 1
            nuevo = f"{nuevo_nombre}_{contador}{extension}"
            if modo_prueba:
                print(f"[SIMULACIÓN] Renombrar {archivo} -> {nuevo}")
            else:
                os.rename(ruta_completa, os.path.join(ruta_carpeta, nuevo))
    return contador

def menu_organizer():
    print("=" * 40)
    print("   GESTOR DE ORGANIZACIÓN")
    print("=" * 40)
    ruta = input("Ruta de la carpeta: ")
    if not os.path.exists(ruta):
        print("La ruta no es válida.")
        return
    while True:
        print("\n1. Por extensión\n2. Por tamaño\n3. Por fecha\n4. Renombrar (Regex)\n5. Volver")
        opcion = input("Opción: ")
        if opcion == "5": break
        sim = input("¿Modo simulación? (s/n): ").lower() == "s"
        if opcion == "1":
            res = clasificar_por_extension(ruta, sim)
            print("Resultado:", res)
        elif opcion == "2":
            res = clasificar_por_tamanio(ruta, sim)
            print("Resultado:", res)
        elif opcion == "3":
            res = clasificar_por_fecha(ruta, sim)
            print("Resultado:", res)
        elif opcion == "4":
            patron = input("Patrón Regex: ")
            nombre = input("Nuevo nombre base: ")
            cant = renombrar_con_regex(ruta, patron, nombre, sim)
            print(f"Procesados: {cant} archivos")

if __name__ == "__main__":
    menu_organizer()
#.