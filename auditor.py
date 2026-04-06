"""
Sistema de Auditoría de Archivos con Snapshots
Detección de archivos nuevos, modificados o eliminados
"""

import os
import json
import hashlib
import time
import argparse
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
            pass  # No fallar si no se puede escribir el log
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
                pass  # No fallar si no se puede escribir el log
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
        return None  # Retorna None si no se puede leer el archivo

def obtener_archivo_info(filepath, base_path):
    """Obtiene información detallada de un archivo"""
    try:
        # Verificar si el archivo existe
        if not os.path.exists(filepath):
            return None
        
        # Normalizar ruta para consistencia entre sistemas operativos
        rel_path = os.path.relpath(filepath, base_path)
        rel_path = rel_path.replace(os.sep, '/')  # Usar siempre '/' como separador
        
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
    """
    Crea un snapshot del estado actual de una carpeta
    Detecta todos los archivos con sus metadatos y hash
    """
    if not os.path.exists(folder_path):
        raise ValueError(f"La carpeta '{folder_path}' no existe")
    
    if not os.path.isdir(folder_path):
        raise ValueError(f"'{folder_path}' no es una carpeta")
    
    if snapshot_name is None:
        snapshot_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Validar que el nombre del snapshot sea válido para nombre de archivo
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
    
    # Límite de seguridad para carpetas muy grandes
    MAX_FILES = 100000
    file_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        # Saltar directorios ocultos si se quiere (opcional)
        
        for file in files:
            file_count += 1
            if file_count > MAX_FILES:
                print(f"⚠️ Se alcanzó el límite de {MAX_FILES} archivos. Algunos archivos no fueron incluidos.")
                break
            
            filepath = os.path.join(root, file)
            file_info = obtener_archivo_info(filepath, folder_path)
            
            if file_info is None:
                print(f"⚠️ No se pudo procesar: {filepath}")
                continue
            
            snapshot["files"][file_info["path"]] = {
                "size": file_info["size"],
                "modified_time": file_info["modified_time"],
                "hash": file_info["hash"]
            }
            
            snapshot["metadata"]["total_files"] += 1
            snapshot["metadata"]["total_size"] += file_info["size"]
        
        if file_count > MAX_FILES:
            break
    
    # Guardar el snapshot en archivo JSON
    snapshot_file = os.path.join(SNAPSHOTS_DIR, f"{snapshot_name}.json")
    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    # Registrar en audit.log
    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[SNAPSHOT] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ")
            log.write(f"Snapshot creado: {snapshot_name} - Archivos: {snapshot['metadata']['total_files']} - ")
            log.write(f"Tamaño: {snapshot['metadata']['total_size'] / 1024:.2f} KB\n")
    except Exception:
        pass
    
    print(f"✅ Snapshot '{snapshot_name}' creado con {snapshot['metadata']['total_files']} archivos")
    return snapshot_file

@log_ejecucion
@mostrar_tiempo
@log_error
def comparar_snapshots(folder_path, previous_snapshot_name, current_snapshot_name=None):
    """
    Compara dos snapshots y detecta archivos nuevos, modificados o eliminados
    """
    # Validamos que la carpeta existe
    if not os.path.exists(folder_path):
        raise ValueError(f"La carpeta '{folder_path}' no existe")
    
    # Validamos que el snapshot anterior existe
    prev_file = os.path.join(SNAPSHOTS_DIR, f"{previous_snapshot_name}.json")
    if not os.path.exists(prev_file):
        raise FileNotFoundError(f"Snapshot anterior '{previous_snapshot_name}' no encontrado")
    
    # Crear snapshot actual si no se proporciona
    if current_snapshot_name is None:
        current_snapshot_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        crear_snapshot(folder_path, current_snapshot_name)
    
    # Validar que el snapshot actual existe
    curr_file = os.path.join(SNAPSHOTS_DIR, f"{current_snapshot_name}.json")
    if not os.path.exists(curr_file):
        raise FileNotFoundError(f"Snapshot actual '{current_snapshot_name}' no encontrado")
    
    # Cargar snapshots
    with open(prev_file, "r", encoding="utf-8") as f:
        previous_snapshot = json.load(f)
    
    with open(curr_file, "r", encoding="utf-8") as f:
        current_snapshot = json.load(f)
    
    previous_files = set(previous_snapshot["files"].keys())
    current_files = set(current_snapshot["files"].keys())
    
    # Detectar cambios
    new_files = current_files - previous_files
    deleted_files = previous_files - current_files
    
    modified_files = []
    for file in current_files & previous_files:
        prev_data = previous_snapshot["files"][file]
        curr_data = current_snapshot["files"][file]
        prev_hash = prev_data.get("hash")
        curr_hash = curr_data.get("hash")
        
        # Manejar archivos con hash None
        if prev_hash is None and curr_hash is None:
            if prev_data.get("size") != curr_data.get("size") or \
               prev_data.get("modified_time") != curr_data.get("modified_time"):
                modified_files.append(file)
        elif prev_hash != curr_hash:
            modified_files.append(file)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "folder": folder_path,
        "previous_snapshot": previous_snapshot_name,
        "current_snapshot": current_snapshot_name,
        "summary": {
            "new_files": len(new_files),
            "modified_files": len(modified_files),
            "deleted_files": len(deleted_files),
            "total_changes": len(new_files) + len(modified_files) + len(deleted_files)
        },
        "details": {
            "new": list(new_files),
            "modified": modified_files,
            "deleted": list(deleted_files)
        }
    }
    
    # Guardar comparación
    comparison_file = os.path.join(SNAPSHOTS_DIR, f"comparison_{current_snapshot_name}.json")
    with open(comparison_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # Registrar en audit.log
    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[COMPARACIÓN] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ")
            log.write(f"Nuevos: {len(new_files)}, Modificados: {len(modified_files)}, ")
            log.write(f"Eliminados: {len(deleted_files)}\n")
    except Exception:
        pass
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE COMPARACIÓN:")
    print(f"   📄 Archivos nuevos: {len(new_files)}")
    print(f"   ✏️  Archivos modificados: {len(modified_files)}")
    print(f"   🗑️  Archivos eliminados: {len(deleted_files)}")
    print(f"   📈 Total cambios: {result['summary']['total_changes']}")
    
    return result

def listar_snapshots():
    """Lista todos los snapshots disponibles"""
    crear_snapshots_dir()
    snapshots = []
    for f in os.listdir(SNAPSHOTS_DIR):
        if f.endswith(".json") and not f.startswith("comparison_"):
            snapshots.append(f.replace(".json", ""))
    return sorted(snapshots, reverse=True)

def mostrar_diferencias(resultado_comparacion):
    """Muestra de forma legible las diferencias encontradas"""
    if resultado_comparacion["summary"]["total_changes"] == 0:
        print("\n✅ No se detectaron cambios entre los snapshots")
        return
    
    print(f"\n📋 DETALLE DE CAMBIOS:")
    
    if resultado_comparacion["details"]["new"]:
        print(f"\n🆕 Archivos NUEVOS ({len(resultado_comparacion['details']['new'])}):")
        for i, file in enumerate(resultado_comparacion["details"]["new"][:10], 1):
            print(f"   {i}. {file}")
        if len(resultado_comparacion["details"]["new"]) > 10:
            print(f"   ... y {len(resultado_comparacion['details']['new']) - 10} más")
    
    if resultado_comparacion["details"]["modified"]:
        print(f"\n✏️  Archivos MODIFICADOS ({len(resultado_comparacion['details']['modified'])}):")
        for i, file in enumerate(resultado_comparacion["details"]["modified"][:10], 1):
            print(f"   {i}. {file}")
        if len(resultado_comparacion["details"]["modified"]) > 10:
            print(f"   ... y {len(resultado_comparacion['details']['modified']) - 10} más")
    
    if resultado_comparacion["details"]["deleted"]:
        print(f"\n🗑️  Archivos ELIMINADOS ({len(resultado_comparacion['details']['deleted'])}):")
        for i, file in enumerate(resultado_comparacion["details"]["deleted"][:10], 1):
            print(f"   {i}. {file}")
        if len(resultado_comparacion["details"]["deleted"]) > 10:
            print(f"   ... y {len(resultado_comparacion['details']['deleted']) - 10} más")

# ==================== FUNCIONES EXTRA ====================

@log_ejecucion
def mirar_audit_log(lines=50):
    """Muestra las últimas líneas del archivo de auditoría"""
    if not os.path.exists(AUDIT_LOG_FILE):
        print("📄 El archivo audit.log aún no existe")
        return
    
    try:
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as log:
            all_lines = log.readlines()
            last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            print(f"\n{'='*60}")
            print(f"ÚLTIMAS {len(last_lines)} LÍNEAS DE audit.log")
            print(f"{'='*60}")
            for line in last_lines:
                print(line.strip())
            print(f"{'='*60}\n")
    except Exception as e:
        print(f"❌ Error leyendo audit.log: {e}")

def limpiar_audit_log():
    """Limpia el archivo de auditoría"""
    try:
        with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"[SISTEMA] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Log reiniciado\n")
        print("🧹 Audit.log ha sido limpiado")
    except Exception as e:
        print(f"❌ Error limpiando audit.log: {e}")

def limpiar_snapshots_antiguos(dias=30):
    """Elimina snapshots más antiguos de X días"""
    import time as time_module
    
    ahora = time_module.time()
    limite = ahora - (dias * 86400)
    eliminados = 0
    
    for snapshot in listar_snapshots():
        snapshot_file = os.path.join(SNAPSHOTS_DIR, f"{snapshot}.json")
        if os.path.exists(snapshot_file):
            mtime = os.path.getmtime(snapshot_file)
            if mtime < limite:
                os.remove(snapshot_file)
                eliminados += 1
                print(f"🗑️ Eliminado snapshot antiguo: {snapshot}")
    
    print(f"✅ Eliminados {eliminados} snapshots antiguos (más de {dias} días)")