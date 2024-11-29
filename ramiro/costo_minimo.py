import tkinter as tk
from tkinter import messagebox
import numpy as np

def minimo_costo(suministro, demanda, costos):
    filas, columnas = costos.shape
    asignacion = np.zeros((filas, columnas))
    total_costo = 0

    while np.any(suministro) and np.any(demanda):
        min_val = np.inf
        for i in range(filas):
            for j in range(columnas):
                if costos[i][j] < min_val and suministro[i] > 0 and demanda[j] > 0:
                    min_val = costos[i][j]
                    min_pos = (i, j)
        i, j = min_pos

        cantidad = min(suministro[i], demanda[j])
        asignacion[i][j] = cantidad
        total_costo += cantidad * costos[i][j]

        suministro[i] -= cantidad
        demanda[j] -= cantidad

        if suministro[i] == 0:
            costos[i, :] = np.inf
        if demanda[j] == 0:
            costos[:, j] = np.inf

    return asignacion, total_costo

def solve():
    try:
        suministro = [int(supply_entries[i].get()) for i in range(num_sources)]
        demanda = [int(demand_entries[i].get()) for i in range(num_destinations)]

        costos = []
        for i in range(num_sources):
            fila = [int(cost_entries[i][j].get()) for j in range(num_destinations)]
            costos.append(fila)

        costos = np.array(costos, dtype=float)
        asignacion, total_costo = minimo_costo(np.array(suministro), np.array(demanda), costos)

        # Mostrar resultado
        result_label.config(text=f"Costo total mínimo: {total_costo}")
        for i in range(num_sources):
            for j in range(num_destinations):
                result_table[i][j].config(text=int(asignacion[i][j]))

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def crear_tabla():
    global num_sources, num_destinations, supply_entries, demand_entries, cost_entries, result_table

    # Obtener el número de fuentes y destinos
    num_sources = int(sources_entry.get())
    num_destinations = int(destinations_entry.get())

    # Limpiar tablas anteriores
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Crear entradas para los suministros
    tk.Label(table_frame, text="Suministro").grid(row=0, column=0)
    supply_entries = []
    for i in range(num_sources):
        entry = tk.Entry(table_frame, width=5)
        entry.grid(row=i + 1, column=0)
        supply_entries.append(entry)

    # Crear entradas para las demandas
    tk.Label(table_frame, text="Demanda").grid(row=num_sources + 1, column=1)
    demand_entries = []
    for j in range(num_destinations):
        entry = tk.Entry(table_frame, width=5)
        entry.grid(row=num_sources + 2, column=j + 1)
        demand_entries.append(entry)

    # Crear entradas para la matriz de costos
    cost_entries = []
    for i in range(num_sources):
        fila = []
        for j in range(num_destinations):
            entry = tk.Entry(table_frame, width=5)
            entry.grid(row=i + 1, column=j + 1)
            fila.append(entry)
        cost_entries.append(fila)

    # Crear tabla de resultados
    result_table = []
    for i in range(num_sources):
        fila = []
        for j in range(num_destinations):
            label = tk.Label(table_frame, text="", width=5, bg="lightgray", relief="solid")
            label.grid(row=i + 1, column=j + 1 + num_destinations)
            fila.append(label)
        result_table.append(fila)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Método de Costo Mínimo")

# Sección para configurar fuentes y destinos
config_frame = tk.Frame(root)
config_frame.pack()

tk.Label(config_frame, text="Número de fuentes:").grid(row=0, column=0)
sources_entry = tk.Entry(config_frame, width=5)
sources_entry.grid(row=0, column=1)

tk.Label(config_frame, text="Número de destinos:").grid(row=1, column=0)
destinations_entry = tk.Entry(config_frame, width=5)
destinations_entry.grid(row=1, column=1)

crear_tabla_button = tk.Button(config_frame, text="Crear tabla", command=crear_tabla)
crear_tabla_button.grid(row=2, columnspan=2)

# Tabla de datos
table_frame = tk.Frame(root)
table_frame.pack()

# Botón para resolver
solve_button = tk.Button(root, text="Resolver", command=solve)
solve_button.pack()

# Resultado
result_label = tk.Label(root, text="")
result_label.pack()

# Ejecutar la interfaz
root.mainloop()
