# KIT MULTIFUNCIONAL: AUTOMATIZACIÓN DE ARCHIVOS

## DESCRIPCIÓN DEL PROYECTO

- Este Software de automatización de archivos desarrollado con la herramienta Python permite extraer información desde archivos de texto externos. El Software funciona como un escáner localizando datos específicos (correos, teléfonos, fechas y palabras clave) de manera rápida.

## INTEGRANTES DEL EQUIPO

| # | Nombre | Rol | GitHub |
|---|--------|-----|--------|
| 1 | [Eduardo Hernández]| Líder / Desarrollador | [@Eduardoahs] |
| 2 | [Xariadna Perez] | Desarrollador | [@deerfoster] |
| 3 | [Ricardo Noriega] | Desarrollador | [@salvvaged] |
| 4 | [Miguel Agelvis] | Desarrollador | [@miguelucho16e] |
| 5 | [Luis Fuentes] | Desarrollador | [@fuentesluisdavid558] |

### Distribución del trabajo:

| Módulo | Responsable |
|--------|-------------|
| `main.py` | [Ricardo Noriega] |
| `menus.py` | [Ricardo Noriega] |
| `organizer.py` | [Eduardo Hernández] |
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
```

### Sistema de Auditoría
```markdown

El Sistema de auditoría de archivos permite crear **snapshots** (instantáneas) del estado de una carpeta y detectar cambios posteriores como archivos **nuevos**, **modificados** o **eliminados**.

#### Funcionalidades

- Crear snapshots del estado actual de una carpeta
- Comparar dos snapshots para detectar cambios
- Registro automático de ejecuciones y errores
- Medición de tiempo de ejecución
- Almacenamiento de snapshots en JSON

#### Requisitos de uso

- Python 3.6+
- Módulos estándar: `os`, `json`, `hashlib`, `time`, `datetime`, `functools`

#### Notas

- Los snapshots almacenan el **hash MD5** de cada archivo para detectar modificaciones
- Los nombres de snapshot solo pueden contener caracteres alfanuméricos, `._-`
- Archivos sin acceso de lectura registran hash como `None`
- Las rutas se guardan en formato universal (con `/`) para compatibilidad multiplataforma
```

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

### Gestor de Organización de Archivos

Este módulo es el encargado del ordenamiento lógico y limpieza de directorios. Permite mover archivos masivamente basándose en criterios técnicos y automatizar el renombrado mediante patrones complejos.

#### Capacidades de Clasificación:

* **Por Extensión:** Agrupa archivos en carpetas automáticas según su tipo (Documentos, Imágenes, Videos, Código, etc.).
* **Por Tamaño:** Categoriza los archivos en:
    * **Pequeños:** (< 1 MB)
    * **Medianos:** (1 MB - 10 MB)
    * **Grandes:** (> 10 MB)
* **Por Fecha:** Organiza el contenido según su última modificación en: **Hoy**, **Esta Semana**, **Este Mes** o **Antiguos**.

#### Funcionalidades Avanzadas:

* **Renombrado con Regex:** Permite cambiar el nombre de múltiples archivos simultáneamente utilizando **Expresiones Regulares** para búsquedas precisas de patrones.
* **Modo Simulación (Dry-run):** Opción de seguridad que permite previsualizar todos los cambios (qué archivos se moverán y cuál será su destino) antes de ejecutar la operación real en el disco.
* **Auditoría Integrada:** Implementación de **Decoradores** de Python para registrar cada operación realizada, garantizando un sistema rastreable y profesional.

#### Instrucciones de Uso:

1.  Ejecutar el menú principal (`main.py`) y seleccionar la opción **1. Organizar Archivos**.
2.  Ingresar la **Ruta de la carpeta** que desea procesar (Ej: `C:/Proyectos/Unimar/Descargas`).
3.  Seleccionar el criterio de organización deseado (1-4).
4.  Confirmar si desea activar el **Modo Simulación** (`s/n`).
    * *Nota: Se recomienda usar 's' primero para verificar los cambios sin riesgo.*

#### Ejemplo de Renombrado con Regex:
* **Patrón:** `^proyecto_.*` (Busca todos los archivos que comiencen con "proyecto_").
* **Nuevo nombre:** `Entregable_Final`.
* **Resultado:** `proyecto_v1.pdf` $\rightarrow$ `Entregable_Final_1.pdf`.

## SET DE PRUEBAS (`test_sample/`)

Se ha preparado una carpeta con 9+ archivos de prueba para demostrar las capacidades del sistema:

* **Archivos Pesados:** `geode_installer.exe` (46 MB) para validar la clasificación de archivos "Grandes" (>10MB).
* **Diversidad de Extensiones:** Muestras de `.jpg`, `.mp3`, `.mp4` y `.docx` para probar la organización automática por carpetas.
* **Patrones de Texto:** Archivos `.txt` con ejemplos de correos, numeros y fechas para el módulo de búsqueda (Analizador).
* **Casos de Borde:** Archivos con nombres complejos para probar el sistema de renombrado con **Regex**.

### Herramientas de Interfaz y Utilidades (Módulo Luis Fuentes)

El módulo de utilidades tiene como objetivo estandarizar la interacción entre el usuario y el sistema, asegurando que la navegación por la terminal sea fluida, limpia y libre de errores de entrada. Proporciona las funciones auxiliares necesarias para que el menú principal funcione correctamente.

Este módulo gestiona aspectos críticos de la experiencia de usuario como:

* **Limpieza de la terminal:** Adaptación automática a diferentes sistemas operativos (Windows/Linux).
* **Validación de entradas:** Asegura que el usuario ingrese datos válidos antes de procesar cualquier acción.
* **Asistencia y Guía:** Centraliza la información de ayuda para el manejo de los distintos módulos del sistema.

## Funcionamiento

El módulo utiliza la librería `os` para detectar el entorno de ejecución y aplicar los comandos de limpieza de pantalla (`cls` o `clear`). Además, implementa funciones de pausa controlada para evitar que la información importante desaparezca de la vista del usuario antes de que este pueda leerla, gestionando el flujo mediante esperas de teclado.

## Integración

`utils.py` actúa como una capa de soporte para todos los demás componentes. El menú principal (`main.py`) depende directamente de estas funciones para organizar los submenús de organización, análisis y auditoría, manteniendo un diseño visual profesional y ordenado durante toda la ejecución del software.

## Resultado

Como salida, este componente garantiza que el sistema ofrezca:

* **Navegación Intuitiva:** Menús organizados y fáciles de seguir para el usuario final.
* **Interfaz Limpia:** Eliminación automática de texto residual de operaciones anteriores en la consola.
* **Manejo de Errores de Usuario:** Mensajes claros cuando se ingresa una opción no válida o una ruta inexistente.
* **Sistema de Ayuda:** Un apartado dedicado a explicar brevemente el funcionamiento de cada herramienta, facilitando la curva de aprendizaje.