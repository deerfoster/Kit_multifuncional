# KIT MULTIFUNCIONAL: AUTOMATIZACIÓN DE ARCHIVOS

## DESCRIPCIÓN DEL PROYECTO

- Este Software de automatización de archivos desarrollado con la herramienta Python permite extraer información desde archivos de texto externos. El Software funciona como un escáner localizando datos específicos (correos, teléfonos, fechas y palabras clave) de manera rápida.

## INTEGRANTES DEL EQUIPO

| # | Nombre | Rol | GitHub |
|---|--------|-----|--------|
| 1 | [Eduardo Hernández]| Líder / Desarrollador | [@Eduardo1705v] |
| 2 | [Xariadna Perez] | Desarrollador | [@deerfoster] |
| 3 | [Ricardo Noriega] | Desarrollador | [@salvvaged] |
| 4 | [Miguel Agelvis] | Desarrollador | [@miguelucho16e] |
| 5 | [Luis Fuentes] | Desarrollador | [@fuentesluisdavid558] |

### Distribución del trabajo:

| Módulo | Responsable |
|--------|-------------|
| `main.py` | [] |
| `organizer.py` | [] |
| `analyzer.py` | [Xariadna Pérez] |
| `auditor.py` | [Ricardo Noriega]|
| `reports.py` | [Miguel Agelvis] |
| `utils.py` | [Luis Fuentes] |

## INSTRUCCIONES DE EJECUCIÓN

#Comandos del sistema analizador de contenido
```bash

- Al ejecutar el código, tener en cuenta:
    
    - Nombre del archivo: Nombre completo.txt
    - Tipo de búsqueda: Sólo hay 4 tipos:

| # | Comando | Qué busca | Ejemplo |
|---|---------|-----------|---------|
| 1 | Email | Correos eléctrónicos | usuario@correo.com |
| 2 | Teléfono | Números de 10 a 12 digitos | +58412000000 |
| 3 | Fecha | Fechas en formato DD/MM/AAAA | 06/04/2026 |
| 4 | Palabras clave | Palabras de 8 a más letras | Archivo |

- Al tener coincidencias el sistema muestra el número de coincidencias y una lista con los mismos.

- Si el archivo no existe mostrará Error "No hay coincidencias o no existe". El archivo puede estar mal escrito o
. en la ruta incorrecta


### Comandos del Sistema de Auditoría

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
