from lib_resources.co_sheets import *
import time

def buscando_sheets():
    try:
        print("--- PASO 1: Conectando a Google Sheets ---")
        sheet = conectar_sheet()
        if not sheet:
            return False, None, None

        print("--- PASO 2: Descargando datos... ---")
        datos = sheet.get_all_values()
        
        hay_trabajo = False
        for fila in datos[1:]: 
            if len(fila) > 10:
                if fila[14].strip() == "PENDIENTE" and fila[2].strip().upper() == "AXIONAL":
                    hay_trabajo = True
                    break
        
        if hay_trabajo:
            print(f">>> ¡Filas encontradas! Preparando listas...")
            return True, datos, sheet
        else:
            print(">>> No se encontraron pendientes AXIONAL.")
            return False, datos, sheet

    except Exception as e:
        print(f"Error en buscando_sheets: {e}")
        return False, None, None

def filtrar_pendientes(datos):
    trabajos_pendientes = []
    
    print("--- Clasificando pendientes (esto puede tardar unos segundos) ---")
    
    for i, fila in enumerate(datos):
        if i == 0: continue # Saltamos cabecera

        if len(fila) > 10:
            estado = fila[14].strip() # Columna K
            tipo   = fila[2].strip()  # Columna C

            if estado == "PENDIENTE" and tipo.upper() == "AXIONAL":
                dato_input = fila[5] # Columna D (Dato para el Query)
                fila_excel = i + 1   # Fila real en el Sheet
                
                # Guardamos la pareja (Fila, Dato) en la lista
                trabajos_pendientes.append((fila_excel, dato_input))
    
    print(f"--- Total detectado: {len(trabajos_pendientes)} registros para procesar ---")
    return trabajos_pendientes

def actualizar_lote_en_sheet(sheet, lista_lote, resultados_dict):
    """
    Recibe el lote actual (ej: 50 items) y las respuestas del bot.
    Actualiza el Excel fila por fila.
    """
    contador_exitos = 0
    
    for fila_excel, boleta_id in lista_lote:
        # Verificamos si esa boleta vino en la respuesta del Query
        if boleta_id in resultados_dict:
            nuevo_estado = resultados_dict[boleta_id] # Ej: 'E'
            
            try:
                # Actualizar Columna F (6) con el estado (E)
                sheet.update_cell(fila_excel, 6, nuevo_estado)
                
                # Actualizar Columna K (11) a FINALIZADO
                sheet.update_cell(fila_excel, 15, "FINALIZADO")
                
                contador_exitos += 1
            except Exception as e:
                print(f"Error actualizando fila {fila_excel}: {e}")
                # Si falla Google, esperamos un poco
                time.sleep(5)
    
    print(f"   -> Lote guardado: {contador_exitos} filas actualizadas.")