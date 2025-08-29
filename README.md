# sap-xliff-translator
herramienta en Python para traducir archivos XLIFF de SAP Datasphere de manera automática.

# SAP Datasphere XLIFF Translator

Este proyecto es una herramienta en **Python** para traducir automáticamente archivos **XLIFF (.xlf)** generados en **SAP Datasphere**, utilizando la API pública de Google Translate.  

Permite convertir los textos de modelos, vistas o etiquetas de **inglés → español** (u otros idiomas), para luego importar las traducciones de nuevo en SAP Datasphere.

---

## ✨ Características

- Traducción automática de archivos `.xlf` y `.xliff`.  
- Dos modos de ejecución:
  1. **Automático** → procesa con `xml.etree.ElementTree` (puede ajustar la estructura).  
  2. **Manual** → conserva la estructura original de SAP.  
- Compatible con Python 3.10+.  
- Opción de seleccionar archivo mediante **ventana gráfica (Tkinter)**.  
- Genera un archivo nuevo con sufijo `_AUTO_ES.xlf`.  

---

## 📦 Requisitos

- Python 3.10 o superior  
- Librerías:
  ```bash
  pip install requests

## Pasos detallados (ejecución local)

Instalar Python

Verifica versión:
python --version o python3 --version

Si no tienes Python 3.10+, instálalo desde python.org o el gestor de tu SO.

Preparar carpeta del proyecto

mkdir xliff-translator
cd xliff-translator


Crear y activar entorno virtual

Windows:

python -m venv venv
.\venv\Scripts\activate


macOS / Linux:

python3 -m venv venv
source venv/bin/activate


Instalar dependencias

pip install requests


Si vas a crear ejecutable más adelante: pip install pyinstaller

Si estás en Linux y la GUI falla, instala tkinter: sudo apt-get install python3-tk (Debian/Ubuntu).

## Guardar el script
Crea translator.py y pega el código corregido que te doy más abajo (sobrescribe el archivo original).

Ejecutar

Por CLI con archivo:

python translator.py /ruta/al/archivo.xlf


O sin argumentos: se abrirá dialog para seleccionar archivo y te pedirá elegir método (1 automático / 2 manual).

Probar con un archivo pequeño antes de usar un XLIFF grande (así detectas problemas de encoding o formato).

Si quieres .exe (Windows):

pyinstaller --onefile translator.py


El ejecutable estará en dist/translator.exe.


## 3) Importar el XLIFF resultante en SAP Datasphere

(Ya tu script imprime instrucciones, aquí un poco más detallado)

Entra a tu espacio/trabajo en SAP Datasphere.

Busca la sección de Localizations / Translations (o el módulo donde importas archivos XLIFF).

Elige Import translations y sube el archivo _AUTO_ES.xlf generado.

Verifica que las cadenas aparezcan y realiza pruebas en un ambiente de desarrollo antes de mover a producción.

Nota: si Datasphere requiere códigos de idioma específicos (ej. es-ES), adapta target_lang antes de importar.

##5) Riesgos y recomendaciones

El endpoint https://translate.googleapis.com/translate_a/single es no oficial y puede dejar de funcionar o aplicarte límites. Para uso serio/producción usa Google Cloud Translate API (requiere proyecto, facturación y credenciales) o DeepL API (muy buena calidad para ES).

Respeta límites y añade time.sleep() (ya lo hiciste) para evitar bloqueos por muchas solicitudes simultáneas.

Respaldar siempre el archivo original XLIFF antes de sobrescribir.
