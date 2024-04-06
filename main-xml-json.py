import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import json

def convert_xml_to_json(file_path):
    # Parsear el archivo XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Convertir el XML a un diccionario de Python
    xml_data = parse_element(root)

    # Convertir el diccionario a JSON
    json_data = json.dumps(xml_data, indent=4)

    # Guardar el JSON en un archivo
    with open("output.json", "w") as json_file:
        json_file.write(json_data)

    print("Archivo JSON generado exitosamente.")

def parse_element(element):
    # Convertir el elemento XML a un diccionario
    data = {}
    if element.text:
        data["text"] = element.text.strip()
    if element.attrib:
        data["attributes"] = element.attrib
    for child in element:
        tag = child.tag.split('}')[-1]  # Eliminar el espacio de nombres del tag
        if tag not in data:
            data[tag] = []
        data[tag].append(parse_element(child))
    return data

# Crear una ventana de tkinter
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal de tkinter

# Abrir el explorador de archivos para seleccionar un archivo XML
file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

# Si se selecciona un archivo XML, convertirlo a JSON
if file_path:
    convert_xml_to_json(file_path)