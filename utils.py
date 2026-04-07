import sys
import time

def mostrar_ayuda():
    """Muestra un mensaje de ayuda detallado para el usuario."""
    print("\n--- MENÚ DE AYUDA ---")
    print("Este kit le permite gestionar archivos mediante la línea de comandos.")
    print("1. Organización: Clasifica y mueve archivos por extensión.")
    print("2. Análisis: Busca información específica dentro de los archivos.")
    print("3. Reportes: Genera resúmenes de las acciones realizadas.")
    print("Asegúrese de tener permisos de lectura/escritura en la carpeta objetivo.")
    print("---------------------\n")

def submenu_organizacion():
    """Ejemplo de un submódulo con su propio menú."""
    while True:
        print("\n--- SUBMENÚ: ORGANIZACIÓN DE ARCHIVOS ---")
        print("1. Clasificar por extensión")
        print("2. Renombrar archivos en lote")
        print("3. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción (1-3): ")
        
        if opcion == '1':
            print("\n[+] Iniciando clasificación de archivos...")
            # Aquí iría la llamada a la función del módulo de organización
        elif opcion == '2':
            print("\n[+] Iniciando renombrado en lote...")
            # Aquí iría la llamada a la función correspondiente
        elif opcion == '3':
            print("\n[-] Volviendo al menú principal...")
            break
        else:
            print("\n[!] Error: Por favor, ingrese una opción válida (1, 2 o 3).")

def menu_principal():
    """Punto de entrada principal del Kit Multifuncional."""
    while True:
        print("\n" + "="*45)
        print("  KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN")
        print("="*45)
        print("1. Módulo de Organización")
        print("2. Módulo de Análisis de Archivos")
        print("3. Módulo de Reportes y Auditoría")
        print("4. Ayuda del Sistema")
        print("5. Salir")
        print("="*45)
        
        try:
            # Forzamos la conversión a entero para validar el tipo de dato
            opcion = int(input("Ingrese el número de la opción deseada: "))
            
            if opcion == 1:
                submenu_organizacion()
            elif opcion == 2:
                print("\n[+] Accediendo al módulo de Análisis...")
                # submenu_analisis()
            elif opcion == 3:
                print("\n[+] Accediendo al módulo de Reportes...")
                # submenu_reportes()
            elif opcion == 4:
                mostrar_ayuda()
            elif opcion == 5:
                print("\n[-] Cerrando el sistema. ¡Hasta pronto!")
                time.sleep(1)
                sys.exit(0)
            else:
                print("\n[!] Error: Opción fuera de rango. Seleccione un número del 1 al 5.")
                
        except ValueError:
            # Captura el error si el usuario ingresa letras o símbolos en lugar de números
            print("\n[!] Error fatal de entrada: Debe ingresar un valor numérico.")

if __name__ == "__main__":
    menu_principal()
