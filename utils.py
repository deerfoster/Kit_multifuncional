import sys
import time
import os  

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo."""
    # 'nt' es Windows, 'posix' es Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar_enter():
    """Pausa el programa hasta que el usuario presione una tecla."""
    input("\nPresione Enter para continuar...")

def mostrar_ayuda():
    """Muestra un mensaje de ayuda detallado para el usuario."""
    limpiar_pantalla()
    print("\n--- MENÚ DE AYUDA ---")
    print("Este kit le permite gestionar archivos mediante la línea de comandos.")
    print("1. Auditoria: Capturar el estado de una carpeta y compararlo")
    print("2. Organización: Clasifica y mueve archivos por extensión.")
    print("3. Análisis: Busca información específica dentro de los archivos.")
    print("4. Reportes: Genera resúmenes de las acciones realizadas.")
    print("Asegúrese de tener permisos de lectura/escritura en la carpeta objetivo.")
    print("---------------------\n")
    esperar_enter()

def submenu_organizacion():
    """Ejemplo de un submódulo con su propio menú."""
    while True:
        limpiar_pantalla()
        print("\n--- SUBMENÚ: ORGANIZACIÓN DE ARCHIVOS ---")
        print("1. Clasificar por extensión")
        print("2. Renombrar archivos en lote")
        print("3. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción (1-3): ")
        
        if opcion == '1':
            print("\n[+] Iniciando clasificación de archivos...")
            # Llamada a organizer.py
            esperar_enter()
        elif opcion == '2':
            print("\n[+] Iniciando renombrado en lote...")
            esperar_enter()
        elif opcion == '3':
            break
        else:
            print("\n[!] Error: Por favor, ingrese una opción válida.")
            time.sleep(1)

def menu_principal():
    """Punto de entrada principal del Kit Multifuncional."""
    while True:
        limpiar_pantalla()
        print("\n" + "="*45)
        print("   KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN")
        print("="*45)
        print("1. Módulo de Organización")
        print("2. Módulo de Análisis de Archivos")
        print("3. Módulo de Reportes y Auditoría")
        print("4. Ayuda del Sistema")
        print("5. Salir")
        print("="*45)
        
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            
            if opcion == 1:
                submenu_organizacion()
            elif opcion == 2:
                print("\n[+] Accediendo al módulo de Análisis...")
                time.sleep(1)
            elif opcion == 3:
                print("\n[+] Accediendo al módulo de Reportes...")
                time.sleep(1)
            elif opcion == 4:
                mostrar_ayuda()
            elif opcion == 5:
                print("\n[-] Cerrando el sistema. ¡Hasta pronto!")
                time.sleep(1)
                sys.exit(0)
            else:
                print("\n[!] Error: Opción fuera de rango.")
                time.sleep(1)
                
        except ValueError:
            print("\n[!] Error fatal de entrada: Debe ingresar un valor numérico.")
            time.sleep(1)
            
if __name__ == "__main__":
    menu_principal()
