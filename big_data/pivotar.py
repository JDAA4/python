import pandas as pd
import matplotlib.pyplot as plt

file_path = "big_data/prendas.csv"
df = pd.read_csv(file_path)

type_counts = df.groupby('Type').size()
color_counts = df.groupby('Color').size()


plt.figure(figsize=(8, 6))
type_counts.sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title("Cantidad de elementos por tipo de prenda")
plt.xlabel("Tipo de prenda")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
color_counts.sort_values(ascending=False).plot(kind='bar', color='salmon')
plt.title("Cantidad de elementos por color")
plt.xlabel("Color")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()