import xml.etree.ElementTree as ET
tree = ET.parse('encuesta_XML.xml')
root = tree.getroot()

# Imprimir la etiqueta raíz
print("Etiqueta raíz:", root.tag)

# Iterar sobre los elementos y extraer datos
for elemento in root.findall('elemento'):
    id_ = elemento.find('id').text
    nombre = elemento.find('nombre').text
    valor = elemento.find('valor').text


    print(f"ID: {id_}, Nombre: {nombre}, Valor: {valor}")