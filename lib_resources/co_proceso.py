from lib_resources.co_playwright import *
from gspread import Cell

def actualizarERP(resultados_query, lote_actual, sheet):
    datos_agrupados = {}
    for fila in resultados_query:
        boleta = fila[0]
        if boleta not in datos_agrupados:
            datos_agrupados[boleta] = []
        datos_agrupados[boleta].append(fila)
    
    updates = [] 
    for item in lote_actual:
        numero_fila = item[0] 
        boleta_excel = str(item[1]).strip()
        
        if boleta_excel in datos_agrupados:
            coincidencias = datos_agrupados[boleta_excel]
            cantidad = len(coincidencias)
            
            if cantidad > 2:
                print(f"Boleta {boleta_excel} ignorada (>2 resultados).")
                continue
            
            if cantidad >= 1:
                dato_1 = coincidencias[0]
                updates.append({'range': f'G{numero_fila}', 'values': [[dato_1[2]]]}) # Estado
                updates.append({'range': f'H{numero_fila}', 'values': [[dato_1[1]]]}) # Importe
                
                if cantidad == 2:
                    dato_2 = coincidencias[1]
                    updates.append({'range': f'J{numero_fila}', 'values': [[dato_2[2]]]}) # Estado 2
                    updates.append({'range': f'K{numero_fila}', 'values': [[dato_2[1]]]}) # Importe 2
                
                updates.append({'range': f'O{numero_fila}', 'values': [['FINALIZADO']]})

    if updates:
        print(f" -> Escribiendo {len(updates)} cambios en el Excel...")
        try:
            sheet.batch_update(updates)
            print("Actualización completada (Datos + FINALIZADO).")
        except Exception as e:
            print(f"Error guardando en Excel: {e}")
    else:
        print("No se encontraron coincidencias válidas para actualizar.")


def actualizar(resultados_query, lote_actual, sheet ):
    try:
        celdas_a_actualizar = []
        print("   -> Preparando datos para guardar en Excel...")
        for item in lote_actual:
            fila = item[0]
            boleta = item[1]
            if boleta in resultados_query:
                nuevo_estado = resultados_query[boleta] 
                celdas_a_actualizar.append(Cell(row=fila, col=6, value=nuevo_estado))
                celdas_a_actualizar.append(Cell(row=fila, col=11, value="FINALIZADO"))
            else:
                print(f"   [!] OJO: La boleta {boleta} no apareció en los resultados del Query.")
        if celdas_a_actualizar:
            try:
                sheet.update_cells(celdas_a_actualizar)
                print(f"ÉXITO: Se guardaron {len(celdas_a_actualizar)//2} registros en la nube.")
            except Exception as e:
                print(f"ERROR CRÍTICO al guardar en Sheets: {e}")
        else:
            print(" No hubo nada que actualizar en este lote.")
        return True
    except Exception as e:
        return False

def consulta(page, ids_formateados):
    try:
        query = f"select docser,import, estado from cefectos where docser in ({ids_formateados})"
        #resultados_query = DBStudio(page, query, ids_formateados)
        resultados_query = DBERP(page, query, ids_formateados)

        return resultados_query
    
    except Exception as e:
        return False

def principal(page, trabajos_pendientes, total_registros, sheet):
    try:
        tamanio_lote = 1000
        
        for i in range(0, total_registros, tamanio_lote):
            lote_actual = trabajos_pendientes[i : i + tamanio_lote]
            
            ids_para_query = [item[1] for item in lote_actual]
            
            print(f"\n--- Procesando lote {i} al {i + len(lote_actual)} ---")
            ids_formateados = ", ".join([f"'{item[1]}'" for item in lote_actual])
            print(ids_formateados)
            resultados_query = consulta(page, ids_formateados)
            print("NUEVOS VALORES")
            print(resultados_query)

            #actualizar(resultados_query, lote_actual, sheet)
            actualizarERP(resultados_query, lote_actual, sheet)
            

        print("¡Proceso de registros finalizado!")
    
        return True
    except Exception as e:
        return False

