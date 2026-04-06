# KIT MULTIFUNCIONAL: AUTOMATIZACIÓN DE ARCHIVOS

## DESCRIPCIÓN DEL PROYECTO

## INTEGRANTES DEL EQUIPO

| # | Nombre | Rol | GitHub |
|---|--------|-----|--------|
| 1 | [Eduardo Hernández]|  | [@Eduardo1705v] |
| 2 | [Xariadna Perez] |  | [@deerfoster] |
| 3 | [Ricardo Noriega] |  | [@salvvaged] |
| 4 | [Miguel Agelvis] | | [@miguelucho16e] |
| 5 | [Luis Fuentes] | | [@fuentesluisdavid558] |

### Distribución del trabajo:

| Módulo | Responsable |
|--------|-------------|
| `main.py` | [] |
| `organizer.py` | [] |
| `analyzer.py` | [Xariadna Pérez] |
| `auditor.py` | [Ricardo Noriega]|
| `reports.py` | [Miguel Agelvis] |
| `utils.py` | [] |

## INSTRUCCIONES DE EJECUCIÓN


### Comandos del Sistema de Auditoría
```bash

- Crear snapshot: python auditor.py crear -f "RUTA" -s "NOMBRE"
- Crea un punto de restauración de una carpeta
- Ej: python auditor.py crear -f /home/docs -s backup_2024

- Comparar snapshots: python auditor.py comparar -f "RUTA" -a "SNAPSHOT_ANTERIOR" -s "SNAPSHOT_ACTUAL"
- Detecta archivos nuevos, modificados o eliminados
- Ej: python auditor.py comparar -f /home/docs -a backup_2025 -s backup_2026

- Listar snapshots: python auditor.py listar
- Muestra todos los snapshots disponibles

- Ver log: python auditor.py log -l "LINEAS"
- Muestra el historial de operaciones (por defecto 50 líneas)
- Ej: python auditor.py log -l 100

- Limpiar log: python auditor.py limpiar
- Reinicia el archivo de auditoría

- Limpiar snapshots antiguos: python auditor.py limpiar-snapshots -d "DIAS"
- Elimina snapshots más antiguos de X días (por defecto 30)
- Ej: python auditor.py limpiar-snapshots -d 7
