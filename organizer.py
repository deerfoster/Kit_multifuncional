import os
import shutil
import re
from datetime import datetime

# DECORADOR DE AUDITORÍA: Sirve para centralizar la gestión de errores 
# y notificar qué función se está ejecutando sin repetir código en cada una.
def auditor_decorador(funcion):
    def envoltura(*args, **kwargs):
        print(f"[SISTEMA] Ejecutando: {funcion.__name__}")
        try:
            return funcion(*args, **kwargs)
        except Exception as e:
            # Si algo falla (permisos, archivos bloqueados), el programa no se detiene
            print(f"[ERROR] No se pudo completar {funcion.__name__}: {e}")
            return {}
    return envoltura

@auditor_decorador
def clasificar_por_extension(ruta_carpeta, modo_prueba=False):
    """Clasifica archivos en carpetas según su formato (.pdf, .jpg, etc.)"""
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
        
        # Saltamos carpetas para no mover directorios dentro de otros
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
            # Creamos la carpeta destino solo si no existe
            os.makedirs(ruta_destino, exist_ok=True)
            shutil.move(ruta_completa, os.path.join(ruta_destino, archivo))
            
    return contador

@auditor_decorador
def clasificar_por_tamanio(ruta_carpeta, modo_prueba=False):
    """Organiza archivos por su peso en MB (Pequeños, Medianos, Grandes)"""
    contador = {'pequeños': 0, 'medianos': 0, 'grandes': 0}
    
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa): continue
        
        # Conversión de Bytes a Megabytes
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
    """Clasifica archivos según su última fecha de modificación"""
    hoy = datetime.now()
    contador = {'hoy': 0, 'esta_semana': 0, 'este_mes': 0, 'antiguos': 0}
    
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa): continue
        
        # Obtenemos la fecha de modificación y calculamos la diferencia en días
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
            print(f"[SIMULACIÓN] Mover {archivo} (Modificado hace {diferencia} días) a {carpeta}/")
        else:
            os.makedirs(ruta_destino, exist_ok=True)
            shutil.move(ruta_completa, os.path.join(ruta_destino, archivo))
            
    return contador

@auditor_decorador
def renombrar_con_regex(ruta_carpeta, patron, nuevo_nombre, modo_prueba=False):
    """Busca archivos con un patrón específico y los renombra masivamente"""
    try:
        patron_regex = re.compile(patron)
    except re.error:
        print("[!] Patrón Regex inválido.")
        return 0
        
    contador = 0
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if os.path.isdir(ruta_completa): continue
        
        # Si el nombre del archivo coincide con el patrón Regex...
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
    """Interfaz de usuario para el módulo de organización"""
    print("=" * 40)
    print("      GESTOR DE ORGANIZACIÓN")
    print("=" * 40)
    
    ruta = input("Ruta de la carpeta a organizar: ")
    if not os.path.exists(ruta):
        print("La ruta no es válida.")
        return
        
    while True:
        print("\n1. Por extensión\n2. Por tamaño\n3. Por fecha\n4. Renombrar (Regex)\n5. Volver")
        opcion = input("Opción: ")
        
        if opcion == "5": 
            break
            
        # El modo simulación permite ver qué pasaría sin alterar los archivos reales
        sim = input("¿Ejecutar como simulación? (s/n): ").lower() == "s"
        
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
            patron = input("Ingrese el patrón a buscar (ej. ^doc_.*): ")
            nombre = input("Nuevo nombre base: ")
            cant = renombrar_con_regex(ruta, patron, nombre, sim)
            print(f"Éxito: {cant} archivos procesados.")

if __name__ == "__main__":
    menu_organizer()