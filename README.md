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
