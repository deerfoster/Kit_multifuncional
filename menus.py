import utils
import auditor
import reports
import os

def submenu_auditoria():
    """Submenú usando funciones existentes de Auditor"""
    while True:
        utils.limpiar_pantalla()
        print("\n--- AUDITORÍA DE ARCHIVOS ---")
        print("1. Crear snapshot")
        print("2. Comparar snapshots")
        print("3. Listar snapshots")
        print("4. Limpiar log")
        print("5. Volver")
        
        opcion = input("Opción: ").strip()
        
        if opcion == "1":
            ruta = input("Ruta de la carpeta: ")
            if os.path.exists(ruta):
                auditor.crear_snapshot(ruta)
            else:
                print("❌ Ruta no existe")
            utils.esperar_enter()
            
        elif opcion == "2":
            snapshots = auditor.listar_snapshots()
            if snapshots:
                print("Snapshots disponibles:")
                for i, s in enumerate(snapshots, 1):
                    print(f"  {i}. {s}")
                try:
                    idx = int(input("Seleccione snapshot anterior: ")) - 1
                    ruta = input("Ruta actual: ")
                    if os.path.exists(ruta):
                        resultado = auditor.comparar_snapshots(ruta, snapshots[idx])
                        print(f"\n📊 Nuevos: {resultado['summary']['nuevos']}")
                        print(f"✏️ Modificados: {resultado['summary']['modificados']}")
                        print(f"🗑️ Eliminados: {resultado['summary']['eliminados']}")
                    else:
                        print("❌ Ruta no existe")
                except:
                    print("❌ Selección inválida")
            else:
                print("❌ No hay snapshots")
            utils.esperar_enter()
            
        elif opcion == "3":
            snapshots = auditor.listar_snapshots()
            print("\nSnapshots guardados:")
            for s in snapshots:
                print(f"  📸 {s}")
            utils.esperar_enter()
            
        elif opcion == "4":
            auditor.limpiar_audit_log()
            utils.esperar_enter()
            
        elif opcion == "5":
            break

def submenu_reportes():
    """Submenú usando funciones existentes de reports"""
    utils.limpiar_pantalla()
    print("\n--- GENERAR REPORTES ---")
    
    # Recopilar datos básicos
    datos_organizacion = {"estado": "Módulo de organización disponible"}
    datos_analisis = {"estado": "Módulo de análisis disponible"}
    datos_auditoria = {
        "total_snapshots": len(auditor.listar_snapshots()),
        "log_file": auditor.AUDIT_LOG_FILE
    }
    
    reports.generar_reporte_general(datos_organizacion, datos_analisis, datos_auditoria)
    print("\n✅ Reportes generados: reporte.txt y reporte.csv")
    utils.esperar_enter()
