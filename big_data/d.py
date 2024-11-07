import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Leer el archivo .xlsx
df = pd.read_excel('Test.xlsx')

# Inspeccionar los datos y los nombres de las columnas
print("Columnas disponibles:", df.columns)
print(df.head())

# Supongamos que descubriste que el nombre de la columna 'c' debería ser 'ColumnaC'
# Actualizar con el nombre correcto
columna_categoria = 'ColumnaC'  # Ajusta esto según los nombres reales de tus columnas

# Verificar si la columna existe antes de proceder
if columna_categoria in df.columns:
    le = LabelEncoder()
    df['b'] = le.fit_transform(df[columna_categoria])
else:
    print(f"Columna '{columna_categoria}' no encontrada en el DataFrame.")

# One-Hot Encoding
if 'a' in df.columns:
    df = pd.get_dummies(df, columns=['a'])
else:
    print("Columna 'a' no encontrada para One-Hot Encoding.")

# Guardar el DataFrame como un archivo .csv
df.to_csv('DataFrame.csv', index=False)
