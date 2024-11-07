from bs4 import BeautifulSoup
import pandas as pd

# Cargar y parsear el archivo XML
with open('encuesta_XML.xml', 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'xml')

# Preparar la estructura tabular
data = []

# Iterar por cada fila (<row>) en el XML
for row in soup.find_all('row'):
    identificador = row.find('Identificador_anónimo').text if row.find('Identificador_anónimo') else None
    promedio = row.find('Promedio_semestre_anterior').text if row.find('Promedio_semestre_anterior') else None
    fatiga = row.find('A_la_hora_de_contestar_el_test_presentabas_fatiga').text if row.find('A_la_hora_de_contestar_el_test_presentabas_fatiga') else None
    problemas_salud = row.find('A_la_hora_de_contestar_el_test_presentabas_problemas_de_salud_temporales_como_dolores_de_cabeza_o_enfermedades_pueden_impactar_el_desempeño_en_el_test').text if row.find('A_la_hora_de_contestar_el_test_presentabas_problemas_de_salud_temporales_como_dolores_de_cabeza_o_enfermedades_pueden_impactar_el_desempeño_en_el_test') else None
    test_mide_correctamente = row.find('Consideras_que_el_test_no_esta_bien_diseñado_para_medir_lo_que_pretende_evaluar').text if row.find('Consideras_que_el_test_no_esta_bien_diseñado_para_medir_lo_que_pretende_evaluar') else None
   
    data.append([identificador, promedio, fatiga, problemas_salud, test_mide_correctamente])


df = pd.DataFrame(data, columns=[
    'Identificador',
    'Promedio_semestre_anterior',
    'Fatiga',
    'Problemas_de_Salud_Temporales',
    'Test_Mide_Correctamente'
])

# imprimer en formato de tabla
print(df)

# crea un archivo csv
df.to_csv('Datos.csv', index=False)