"""
MÓDULO PRINCIPAL - Integración del sistema
"""

import sys

# Importar todos los módulos existentes
import auditor
import analyzer
import organizer
import utils
import menus

def main():
    """Menú principal unificado"""
    
    # Crear directorio de snapshots si no existe (usando la función existente)
    auditor.crear_snapshots_dir()
    
    while True:
        utils.limpiar_pantalla()
        print("\n" + "=" * 50)
        print("   🚀 KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN")
        print("=" * 50)
        print("1. 📁 Auditoría de Archivos (Snapshots)")
        print("2. 🔎 Análisis de Archivos (Regex)")
        print("3. 📂 Organización de Archivos")
        print("4. 📊 Generar Reportes")
        print("5. ❓ Ayuda")
        print("6. 🚪 Salir")
        print("=" * 50)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Usar funciones existentes de Auditor
            menus.submenu_auditoria()
            
        elif opcion == "2":
            # Usar función existente de analyzer
            analyzer.search_box()
            utils.esperar_enter()
            
        elif opcion == "3":
            # Usar menú existente de organizer
            organizer.menu_organizer()
            
        elif opcion == "4":
            # Usar funciones existentes de reports
            menus.submenu_reportes()
            
        elif opcion == "5":
            utils.mostrar_ayuda()
            
        elif opcion == "6":
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("❌ Opción inválida")
            utils.esperar_enter()
            
# Punto de entrada
if __name__ == "__main__":
    main()