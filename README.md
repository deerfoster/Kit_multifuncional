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


### Generador de reportes

El módulo de generación de reportes tiene como objetivo transformar los datos procesados por los distintos componentes del sistema en información clara, organizada y exportable.

Este módulo recibe los resultados provenientes de:

* El **gestor de organización de archivos**
* El **analizador de contenido**
* El **auditor de cambios**

A partir de estos datos, se generan reportes automáticos en dos formatos:

## Reporte en formato TXT

* Presenta la información de manera legible para el usuario.
* Organiza los datos por secciones (organización, análisis y auditoría).
* Ideal para consultas rápidas desde la terminal.

## Reporte en formato CSV

* Estructura los datos en forma de tabla.
* Permite su uso en herramientas externas como Excel o Google Sheets.
* Facilita el análisis y la manipulación de la información.

## Funcionamiento

El módulo utiliza estructuras de datos como diccionarios para organizar la información antes de exportarla. Cada sección del reporte corresponde a un conjunto de datos específicos generados por otros módulos.

Para la creación de archivos se emplea `with open()`, garantizando un manejo seguro de los recursos. Además, se implementa manejo de excepciones (`try/except`) para evitar errores durante la generación de los reportes.

## Integración

Este módulo es independiente del procesamiento interno de los datos, ya que trabaja únicamente con estructuras ya generadas. Esto permite una integración sencilla con el resto del sistema a través del menú principal.

## Resultado

Como salida, el sistema genera automáticamente:

* `reporte.txt`
* `reporte.csv`

Ambos archivos contienen un resumen estructurado de las operaciones realizadas por el sistema, facilitando la interpretación de resultados y la toma de decisiones.

