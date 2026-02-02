import time, pyperclip, re

def login_DBStudio(page):
    try:
        usuario = 'orojas'
        contra = 'Illidan1<1'
        page.wait_for_selector("#input-11")
        page.wait_for_selector("#input-12")
        page.fill("#input-11", usuario)
        page.fill("#input-12", contra)

        page.click("#app > div > main > div > div > div > div.d-flex.col-md-6.col-lg-5.col-12 > div > div.v-card__text.pa-0 > form > button > span")
        return True
    except:
        print("No se pudo loguear")
        return False

def login_ERP(page):
    try:
        usuario = 'orojas'
        contra = 'Illidan1<1'
        page.wait_for_selector("#input-7")
        page.wait_for_selector("#input-11")
        page.fill("#input-7", usuario)
        page.fill("#input-11", contra)

        page.click("#login-btn > span")
        return True
    except Exception as e:
        print(e)
        return False

def DBERP(page, query, lista_ids):
    try:

        page.goto("https://erp.crp.com.pe/os/desktop#/desktop/0")
        page.wait_for_selector("#app > div.v-application--wrap > div > div > header > div > button:nth-child(9) > span > i")
        page.click("#app > div.v-application--wrap > div > div > header > div > button:nth-child(9) > span > i")
        page.wait_for_selector("#app > div.v-application--wrap > div > div > nav.v-navigation-drawer.v-navigation-drawer--fixed.v-navigation-drawer--open.v-navigation-drawer--right.v-navigation-drawer--temporary.theme--dark > div.v-navigation-drawer__content > div > div.pa-0.webos-tools-container-col-2.col-sm-12.col-12 > div > div:nth-child(2) > div > div:nth-child(2) > a > div > div > div.d-flex > div.justify-center.text-center.align-self-center.rounded-lg.v-card.v-card--link.v-sheet.theme--dark.white")
        page.click("#app > div.v-application--wrap > div > div > nav.v-navigation-drawer.v-navigation-drawer--fixed.v-navigation-drawer--open.v-navigation-drawer--right.v-navigation-drawer--temporary.theme--dark > div.v-navigation-drawer__content > div > div.pa-0.webos-tools-container-col-2.col-sm-12.col-12 > div > div:nth-child(2) > div > div:nth-child(2) > a > div > div > div.d-flex > div.justify-center.text-center.align-self-center.rounded-lg.v-card.v-card--link.v-sheet.theme--dark.white")
        page.wait_for_selector("#dbstudio-main-content > div > div > div > div:nth-child(1) > div.v-list-item__content")
        page.click("#dbstudio-main-content > div > div > div > div:nth-child(1) > div.v-list-item__content")
        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1)")
        selector_editor = "#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > div > div:nth-child(1) > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text"
        page.click(selector_editor)

        pyperclip.copy(query)
        page.click(selector_editor)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")

        print("   -> Pegando query masivo...")
        page.keyboard.press("Control+V")

        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > div:nth-child(25) > div > div > div.v-select__slot > div.v-input__append-inner > div > i")
        page.click("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > div:nth-child(25) > div > div > div.v-select__slot > div.v-input__append-inner > div > i")
        page.wait_for_selector("#list-item-209-3")
        page.click("#list-item-209-3")

        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > button:nth-child(4) > span > i")
        page.click("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > button:nth-child(4) > span > i")

        print(" -> Esperando tabla de resultados...")
        page.wait_for_selector("#id_10000001 > div.ax-table-container > div > table > tbody > tr > td.pl-1.pr-2.cell-align-right.ax-grid-cell-rows > div > div")
        texto_total = page.inner_text("#id_10000001 > div.ax-table-container > div > table > tbody > tr > td.pl-1.pr-2.cell-align-right.ax-grid-cell-rows > div > div")
        print(texto_total)
        meta_real = int(''.join(filter(str.isdigit, texto_total)))
        #selector de resultado
        selector_resultados = "#id_10000002 > div.ax-table-container > div"
        page.wait_for_selector(selector_resultados)

    
        caja = page.locator(selector_resultados).bounding_box()
        if caja:
            page.mouse.move(caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2)
        
        resultados_totales = {}

        intentos_sin_cambio = 0
        ultimo_tamano = 0
        
        while len(resultados_totales) < meta_real:
            texto_visible = page.inner_text(selector_resultados)
            nuevos = parsear_texto_visible_ERP(texto_visible)
            resultados_totales.update(nuevos)
            
            actual = len(resultados_totales)
            print(f"   -> Progreso: {actual}/{meta_real}")

            # Si ya tenemos todo, salimos
            if actual >= meta_real:
                break

            # Si se atasca (el contador no sube), salimos para no colgar
            if actual == ultimo_tamano:
                intentos_sin_cambio += 1
                if intentos_sin_cambio > 20: 
                    print("⚠️ Se atascó el scroll. Devolviendo lo encontrado.")
                    break
            else:
                intentos_sin_cambio = 0
                ultimo_tamano = actual
            
            # Scroll suave para que cargue
            page.mouse.wheel(0, 200) 
            time.sleep(0.3)
            
        return list(resultados_totales.values())

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def parsear_texto_visible_ERP(texto):
    resultados = {}
    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    iterador = iter(lineas)
    try:
        while True:
            item = next(iterador)
            if item.startswith("F") and "-" in item and len(item) > 8:
                docser = item
                monto = "0.00"
                estado = "SIN"
                try:
                    sig = next(iterador)
                    if sig.isdigit() and len(sig) < 4: sig = next(iterador) # Salta indices
                    if any(c.isdigit() for c in sig): monto = sig.replace(',', '')
                    else: 
                        if len(sig) <= 3 and sig.isupper(): estado = sig
                    if estado == "SIN":
                        sig = next(iterador)
                        if len(sig) <= 3 and sig.isupper(): estado = sig
                except: pass
                # Llave única para que no borre duplicados
                resultados[f"{docser}|{monto}|{estado}"] = [docser, monto, estado]
    except StopIteration: pass
    return resultados

def DBStudio(page, query, lista_ids):
    try:
        page.goto("https://fas.crp.com.pe/view/portal/518")   
        page.wait_for_selector("#app > div.v-application--wrap > header > div > button:nth-child(7) > span")
        page.click("#app > div.v-application--wrap > header > div > button:nth-child(7) > span")
        page.wait_for_selector("#app > div.v-menu__content.theme--light.rounded-lg.v-menu__content--fixed.menuable__content__active > div > div > div:nth-child(1) > div > div:nth-child(3) > a")
        page.click("#app > div.v-menu__content.theme--light.rounded-lg.v-menu__content--fixed.menuable__content__active > div > div > div:nth-child(1) > div > div:nth-child(3) > a")
        page.wait_for_selector("#dbstudio-main-content > div > div > div > div:nth-child(1)")
        page.click("#dbstudio-main-content > div > div > div > div:nth-child(1)")
        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > div > div:nth-child(1) > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text")
        selector_editor = "#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > div > div:nth-child(1) > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text > div"
        page.click(selector_editor)
        
        pyperclip.copy(query)
        page.click(selector_editor)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")

        print("   -> Pegando query masivo...")
        page.keyboard.press("Control+V")

        
        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > button:nth-child(4) > span > i")
        page.click("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > button:nth-child(4) > span > i")  
       
        selector_resultados = "#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > div > div:nth-child(3) > div > div:nth-child(2) > div > div.container.active-tab-rs.pa-0 > div"
        page.wait_for_selector(selector_resultados)
        
        caja = page.locator(selector_resultados).bounding_box()
        if caja:
            page.mouse.move(caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2)
        
        resultados_totales = {}
        
        for i in range(30):
            texto_visible = page.inner_text(selector_resultados)
            
            nuevos = parsear_texto_visible(texto_visible)
            resultados_totales.update(nuevos)
            
            if len(resultados_totales) >= len(lista_ids):
                break
            
            page.mouse.wheel(0, 200) 
            time.sleep(0.3)
            
        return resultados_totales
    except Exception as e:
        print(e)
        return False
    
def parsear_texto_visible(texto):
    resultados = {}
    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    
    for i, item in enumerate(lineas):
        if item.startswith("F") and "-" in item and len(item) > 10:
            boleta = item
            
            if i + 1 < len(lineas):
                estado = lineas[i+1]
                
                if len(estado) < 15 and not (estado.startswith("F") and "-" in estado):
                    resultados[boleta] = estado
                else:
                    resultados[boleta] = "SIN_ESTADO"
                    
    return resultados