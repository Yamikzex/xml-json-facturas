import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def procesar_factura():
    # Obtener la ruta del archivo XML seleccionado
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
    
    if not ruta_archivo:
        return
    
    # Parsear el archivo XML
    tree = ET.parse(ruta_archivo)
    root = tree.getroot()

    # Definir los namespaces
    namespaces = {
        'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
        'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
        'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
    }

    # Obtener el número de factura
    numero_factura = root.find('.//cbc:ID', namespaces=namespaces).text

    # Obtener el nombre y NIT del emisor de la factura
    emisor = root.find('.//cac:SenderParty', namespaces=namespaces)
    nombre_emisor = emisor.find('.//cbc:RegistrationName', namespaces=namespaces).text
    nit_emisor = emisor.find('.//cbc:CompanyID', namespaces=namespaces).text

    # Obtener el nombre y NIT del adquiriente de la factura
    adquiriente = root.find('.//cac:ReceiverParty', namespaces=namespaces)
    nombre_adquiriente = adquiriente.find('.//cbc:RegistrationName', namespaces=namespaces).text
    nit_adquiriente = adquiriente.find('.//cbc:CompanyID', namespaces=namespaces).text

# Obtener el detalle de los ítems de la factura
    detalles_items = []
    for item in root.findall('.//cac:InvoiceLine', namespaces=namespaces):
        descripcion = item.find('.//cbc:Description', namespaces=namespaces).text
        cantidad = item.find('.//cbc:InvoicedQuantity', namespaces=namespaces).text
        precio = item.find('.//cbc:PriceAmount', namespaces=namespaces).text
        detalles_items.append({'descripcion': descripcion, 'cantidad': cantidad, 'precio': precio})



    # Mostrar la información en formato de texto plano
    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, "Número de factura: " + numero_factura + "\n\n")
    resultado_text.insert(tk.END, "Emisor:\n")
    resultado_text.insert(tk.END, "  Nombre: " + nombre_emisor + "\n")
    resultado_text.insert(tk.END, "  NIT: " + nit_emisor + "\n\n")
    resultado_text.insert(tk.END, "Adquiriente:\n")
    resultado_text.insert(tk.END, "  Nombre: " + nombre_adquiriente + "\n")
    resultado_text.insert(tk.END, "  NIT: " + nit_adquiriente + "\n\n")
    resultado_text.insert(tk.END, "Detalle de los ítems de la factura:\n")
    for i, item in enumerate(detalles_items, start=1):
        resultado_text.insert(tk.END, f"  - Ítem {i}:\n")
        resultado_text.insert(tk.END, "    Descripción: " + item['descripcion'] + "\n")
        resultado_text.insert(tk.END, "    Cantidad: " + item['cantidad'] + "\n")
        resultado_text.insert(tk.END, "    Precio: " + item['precio'] + " COP\n\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Procesar Factura Electrónica")

# Botón para seleccionar archivo
boton_seleccionar = tk.Button(root, text="Seleccionar Archivo", command=procesar_factura)
boton_seleccionar.pack(pady=10)

# Área de texto para mostrar el resultado
resultado_text = tk.Text(root, height=20, width=70)
resultado_text.pack(padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()