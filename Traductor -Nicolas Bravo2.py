import xml.etree.ElementTree as ET
from pathlib import Path
import requests
import time
from typing import Optional, Dict
import sys
from tkinter import Tk, filedialog
import re

class SAPXliffAutoTranslator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.nombres_traducidos: Dict[str, int] = {}
    
    def generar_nombre_unico(self, texto_traducido: str) -> str:
        """Genera un nombre único agregando sufijos numéricos si es necesario"""
        # Limpiar el texto traducido para usar como nombre (mantener espacios)
        nombre_base = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]', '', texto_traducido)
        nombre_base = nombre_base.strip()
        
        if not nombre_base:
            nombre_base = "sin nombre"
        
        # Si el nombre no existe, guardarlo y retornar
        if nombre_base not in self.nombres_traducidos:
            self.nombres_traducidos[nombre_base] = 0
            return nombre_base
        
        # Si existe, incrementar el contador y retornar con sufijo numérico
        self.nombres_traducidos[nombre_base] += 1
        return f"{nombre_base} {self.nombres_traducidos[nombre_base]}"
    
    def translate_text(self, text: str, source_lang: str = 'en', target_lang: str = 'es') -> Optional[str]:
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {'client': 'gtx', 'sl': source_lang, 'tl': target_lang, 'dt': 't', 'q': text}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                texto_traducido = ''.join([item[0] for item in data[0] if item])
                
                # Si el texto parece ser un nombre (sin espacios o muy corto), hacerlo único
                if len(texto_traducido.split()) <= 3 or len(texto_traducido) < 25:
                    texto_traducido = self.generar_nombre_unico(texto_traducido)
                
                return texto_traducido
            return None
        except Exception as e:
            print(f"Error traduciendo '{text}': {e}")
            return None
    
    def traducir_xliff_automatico(self, archivo_entrada: str, archivo_salida: Optional[str] = None):
        try:
            # Reiniciar el diccionario de nombres para cada archivo
            self.nombres_traducidos = {}
            
            ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
            ET.register_namespace('sxmd', 'urn:x-sap:mlt:xliff12:metadata:1.0')
            tree = ET.parse(archivo_entrada)
            root = tree.getroot()
            namespaces = {
                'xliff': 'urn:oasis:names:tc:xliff:document:1.2',
                'sxmd': 'urn:x-sap:mlt:xliff12:metadata:1.0'
            }
            total = traducidos = errores = 0
            print("Iniciando traducción automática...")
            print("-" * 50)
            
            for trans_unit in root.findall('.//xliff:trans-unit', namespaces):
                source_elem = trans_unit.find('xliff:source', namespaces)
                if source_elem is not None and source_elem.text and source_elem.text.strip():
                    texto_original = source_elem.text.strip()
                    total += 1
                    texto_traducido = self.translate_text(texto_original)
                    if texto_traducido:
                        target_elem = trans_unit.find('xliff:target', namespaces)
                        if target_elem is None:
                            target_elem = ET.SubElement(trans_unit, '{urn:oasis:names:tc:xliff:document:1.2}target')
                        target_elem.set('state', 'translated')
                        target_elem.set('state-qualifier', 'exact-match')
                        target_elem.text = texto_traducido
                        print(f"✓ '{texto_original}' -> '{texto_traducido}'")
                        traducidos += 1
                    else:
                        print(f"✗ Error traduciendo: '{texto_original}'")
                        errores += 1
                    time.sleep(0.3)
            
            if archivo_salida is None:
                entrada_path = Path(archivo_entrada)
                archivo_salida = entrada_path.parent / f"{entrada_path.stem}_AUTO_ES.xlf"
            
            tree.write(archivo_salida, encoding='UTF-8', xml_declaration=True)
            
            # Limpiar namespaces
            with open(archivo_salida, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('ns0:', '').replace('xmlns:ns0=', 'xmlns=')
            
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(content)
            
            print("-" * 50)
            print(f"Traducción completada! Total: {total}, Traducidos: {traducidos}, Errores: {errores}")
            print(f"Archivo guardado como: {archivo_salida}")
            return True
        except Exception as e:
            print(f"Error procesando el archivo: {e}")
            return False

def procesar_archivo_manual(archivo_entrada, archivo_salida=None):
    try:
        # Diccionario para trackear nombres únicos en el método manual
        nombres_traducidos = {}
        
        def generar_nombre_unico_manual(texto_traducido):
            # Mantener espacios en lugar de convertirlos a guiones bajos
            nombre_base = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]', '', texto_traducido)
            nombre_base = nombre_base.strip()
            
            if not nombre_base:
                nombre_base = "sin nombre"
            
            if nombre_base not in nombres_traducidos:
                nombres_traducidos[nombre_base] = 0
                return nombre_base
            
            nombres_traducidos[nombre_base] += 1
            return f"{nombre_base} {nombres_traducidos[nombre_base]}"
        
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lineas = f.read().split('\n')
        
        nuevo_contenido = []
        print("Procesando archivo manteniendo estructura SAP...")
        print("-" * 50)
        translator = SAPXliffAutoTranslator()
        total = traducidos = 0
        
        for i, linea in enumerate(lineas):
            if '<source>' in linea and '</source>' in linea:
                inicio = linea.find('<source>') + len('<source>')
                fin = linea.find('</source>')
                texto_original = linea[inicio:fin].strip()
                
                if texto_original:
                    total += 1
                    texto_traducido = translator.translate_text(texto_original)
                    
                    if texto_traducido:
                        # Verificar si es un nombre y hacerlo único si es necesario
                        if len(texto_traducido.split()) <= 3 or len(texto_traducido) < 25:
                            texto_traducido = generar_nombre_unico_manual(texto_traducido)
                        
                        target_line = f'                <target state="translated" state-qualifier="exact-match">{texto_traducido}</target>'
                        
                        # Buscar la siguiente línea para insertar/reemplazar
                        siguiente_linea_index = i + 1
                        while siguiente_linea_index < len(lineas):
                            if '<target' in lineas[siguiente_linea_index]:
                                lineas[siguiente_linea_index] = target_line
                                break
                            siguiente_linea_index += 1
                        else:
                            # Si no encontró target, insertar después del source
                            lineas.insert(i + 1, target_line)
                        
                        traducidos += 1
                        print(f"✓ '{texto_original}' -> '{texto_traducido}'")
                    else:
                        print(f"✗ Error traduciendo: '{texto_original}'")
            
            nuevo_contenido.append(linea)
            time.sleep(0.2)
        
        if archivo_salida is None:
            entrada_path = Path(archivo_entrada)
            archivo_salida = entrada_path.parent / f"{entrada_path.stem}_AUTO_ES.xlf"
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))  # Usar lineas modificadas en lugar de nuevo_contenido
        
        print("-" * 50)
        print(f"Procesamiento completado! Total: {total}, Traducidos: {traducidos}")
        print(f"Archivo guardado como: {archivo_salida}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def seleccionar_archivo():
    root = Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Selecciona el archivo XLIFF", filetypes=[("XLIFF files", "*.xlf *.xliff")])
    root.destroy()
    return archivo

def main():
    if len(sys.argv) == 2:
        archivo_entrada = sys.argv[1]
    else:
        print("No se proporcionó archivo. Se abrirá un selector de archivos...")
        archivo_entrada = seleccionar_archivo()
        if not archivo_entrada:
            print("No se seleccionó ningún archivo. Saliendo...")
            sys.exit(1)
    
    if not Path(archivo_entrada).exists():
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        sys.exit(1)
    
    print("Selecciona el método de procesamiento:")
    print("1. Método automático (puede alterar estructura)")
    print("2. Método manual (preserva estructura exacta)")
    opcion = input("Opción (1 o 2): ").strip()
    
    if opcion == "2":
        success = procesar_archivo_manual(archivo_entrada)
    else:
        translator = SAPXliffAutoTranslator()
        success = translator.traducir_xliff_automatico(archivo_entrada)
    
    if success:
        print("✅ Proceso completado exitosamente!")
        print("\n📝 Instrucciones para importar en SAP Datasphere:")
        print("1. Ve a tu espacio de trabajo de SAP Datasphere")
        print("2. Navega a la sección de traducciones")
        print("3. Selecciona 'Importar traducciones'")
        print("4. Elige el archivo generado con sufijo _AUTO_ES.xlf")
        print("5. Confirma la importación")
    else:
        print("❌ Ocurrieron errores durante el proceso.")
        sys.exit(1)

if __name__ == "__main__":
    main()
