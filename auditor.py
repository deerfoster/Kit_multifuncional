"""
Sistema de Auditoría de Archivos con Snapshots
Detección de archivos nuevos, modificados o eliminados
"""
import os
import json
import hashlib
import time
from datetime import datetime
from functools import wraps

# ==================== DECORADORES ====================

AUDIT_LOG_FILE = "audit.log"

def log_ejecucion(func):
    """Decorador: Registra la ejecución de la función en audit.log"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[EXECUCIÓN] {timestamp} - Función: {func.__name__}\n")
        except Exception:
            pass
        print(f"🔵 Ejecutando: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def log_error(func):
    """Decorador: Registra errores en audit.log cuando ocurren excepciones"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"[ERROR] {timestamp} - Función: {func.__name__} - Error: {str(e)}\n")
            except Exception:
                pass
            print(f"🔴 ERROR en {func.__name__}: {e}")
            raise
    return wrapper

def mostrar_tiempo(func):
    """Decorador: Mide y registra el tiempo de ejecución de la función"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[TIEMPO] {timestamp} - Función: {func.__name__} - Duración: {elapsed_time:.3f} segundos\n")
        except Exception:
            pass
        print(f"⏱️  {func.__name__} completado en {elapsed_time:.3f} segundos")
        return result
    return wrapper

# ==================== SNAPSHOTS ====================

SNAPSHOTS_DIR = "snapshots"

def crear_snapshots_dir():
    """Asegura que existe el directorio de snapshots"""
    if not os.path.exists(SNAPSHOTS_DIR):
        os.makedirs(SNAPSHOTS_DIR)

def calcular_archivo_hash(filepath):
    """Calcula el hash MD5 de un archivo"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (IOError, OSError, PermissionError):
        return None

def obtener_archivo_info(filepath, base_path):
    """Obtiene información detallada de un archivo"""
    try:
        if not os.path.exists(filepath):
            return None
        
        rel_path = os.path.relpath(filepath, base_path)
        rel_path = rel_path.replace(os.sep, '/') 
        
        stat = os.stat(filepath)
        
        return {
            "path": rel_path,
            "size": stat.st_size,
            "modified_time": stat.st_mtime,
            "modified_time_str": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "hash": calcular_archivo_hash(filepath)
        }
    except Exception as e:
        print(f"⚠️ Error procesando {filepath}: {e}")
        return None

@log_ejecucion
@mostrar_tiempo
@log_error
def crear_snapshot(folder_path, snapshot_name=None):
    """Crea un snapshot del estado actual de una carpeta"""
    if not os.path.exists(folder_path):
        raise ValueError(f"La carpeta '{folder_path}' no existe")
    
    if snapshot_name is None:
        snapshot_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    snapshot_name = "".join(c for c in snapshot_name if c.isalnum() or c in '._-')
    crear_snapshots_dir()
    
    snapshot = {
        "metadata": {
            "name": snapshot_name,
            "created_at": datetime.now().isoformat(),
            "folder_path": os.path.abspath(folder_path),
            "total_files": 0,
            "total_size": 0
        },
        "files": {}
    }
    
    print(f"📸 Creando snapshot de: {folder_path}")
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            file_info = obtener_archivo_info(filepath, folder_path)
            
            if file_info:
                snapshot["files"][file_info["path"]] = {
                    "size": file_info["size"],
                    "modified_time": file_info["modified_time"],
                    "hash": file_info["hash"]
                }
                snapshot["metadata"]["total_files"] += 1
                snapshot["metadata"]["total_size"] += file_info["size"]
    
    snapshot_file = os.path.join(SNAPSHOTS_DIR, f"{snapshot_name}.json")
    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Snapshot '{snapshot_name}' creado")
    return snapshot_name

@log_ejecucion
@mostrar_tiempo
@log_error
def comparar_snapshots(folder_path, previous_snapshot_name, current_snapshot_name=None):
    """Compara dos snapshots y detecta archivos nuevos, modificados o eliminados"""
    crear_snapshots_dir()
    
    prev_file = os.path.join(SNAPSHOTS_DIR, f"{previous_snapshot_name}.json")
    if not os.path.exists(prev_file):
        raise FileNotFoundError(f"Snapshot anterior '{previous_snapshot_name}' no encontrado")
    
    if current_snapshot_name is None:
        current_snapshot_name = crear_snapshot(folder_path)
    
    curr_file = os.path.join(SNAPSHOTS_DIR, f"{current_snapshot_name}.json")
    
    with open(prev_file, "r", encoding="utf-8") as f:
        previous_snapshot = json.load(f)
    
    with open(curr_file, "r", encoding="utf-8") as f:
        current_snapshot = json.load(f)
    
    previous_files = set(previous_snapshot["files"].keys())
    current_files = set(current_snapshot["files"].keys())
    
    new_files = current_files - previous_files
    deleted_files = previous_files - current_files
    modified_files = []

    for file in current_files & previous_files:
        if previous_snapshot["files"][file].get("hash") != current_snapshot["files"][file].get("hash"):
            modified_files.append(file)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "folder": folder_path,
        "summary": {
            "nuevos": len(new_files),
            "modificados": len(modified_files),
            "eliminados": len(deleted_files)
        },
        "detalles": {
            "lista_nuevos": list(new_files),
            "lista_modificados": modified_files,
            "lista_eliminados": list(deleted_files)
        }
    }
    
    return result

def listar_snapshots():
    crear_snapshots_dir()
    snapshots = [f.replace(".json", "") for f in os.listdir(SNAPSHOTS_DIR) if f.endswith(".json") and "comparison" not in f]
    return sorted(snapshots, reverse=True)

def limpiar_audit_log():
    try:
        with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"[SISTEMA] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Log reiniciado\n")
        print("🧹 Audit.log ha sido limpiado")
    except Exception as e:
        print(f"❌ Error limpiando audit.log: {e}")