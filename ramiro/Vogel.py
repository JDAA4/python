import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


def calcular_vogel(cost_matrix, supply, demand):
    rows, cols = len(supply), len(demand)
    total_cost = 0
    allocations = np.zeros((rows, cols), dtype=int)
    
    while sum(supply) > 0 and sum(demand) > 0:
        penalties = []
        
        for i in range(rows):
            if supply[i] > 0:
                row = [cost_matrix[i][j] for j in range(cols) if demand[j] > 0]
                if len(row) > 1:
                    penalties.append((i, sorted(row)[1] - sorted(row)[0]))
                else:
                    penalties.append((i, sorted(row)[0]))
        
        for j in range(cols):
            if demand[j] > 0:
                col = [cost_matrix[i][j] for i in range(rows) if supply[i] > 0]
                if len(col) > 1:
                    penalties.append((j + rows, sorted(col)[1] - sorted(col)[0]))
                else:
                    penalties.append((j + rows, sorted(col)[0]))
        
        penalties.sort(key=lambda x: x[1], reverse=True)
        
        if penalties[0][0] < rows:  # Row penalty
            i = penalties[0][0]
            j = np.argmin([cost_matrix[i][k] if demand[k] > 0 else float('inf') for k in range(cols)])
        else:  # Column penalty
            j = penalties[0][0] - rows
            i = np.argmin([cost_matrix[k][j] if supply[k] > 0 else float('inf') for k in range(rows)])
        
        x = min(supply[i], demand[j])
        allocations[i][j] = x
        total_cost += x * cost_matrix[i][j]
        supply[i] -= x
        demand[j] -= x
    
    return total_cost, allocations


def generar_tabla():
    try:
        num_fuentes = int(entry_fuentes.get())
        num_destinos = int(entry_destinos.get())
        
        # Limpiar la tabla anterior si existe
        for widget in frame_tabla.winfo_children():
            widget.destroy()
        
        # Crear entradas para la matriz de costos
        global cost_entries
        cost_entries = []
        ttk.Label(frame_tabla, text="Matriz de Costos", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=num_destinos, pady=5)
        
        for i in range(num_fuentes):
            row_entries = []
            for j in range(num_destinos):
                entry = ttk.Entry(frame_tabla, width=5, justify="center")
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            cost_entries.append(row_entries)
        
        # Crear entradas para suministros
        global supply_entries
        supply_entries = []
        ttk.Label(frame_tabla, text="Supply", font=("Arial", 10, "bold")).grid(row=0, column=num_destinos + 1, padx=5, pady=5)
        
        for i in range(num_fuentes):
            entry = ttk.Entry(frame_tabla, width=5, justify="center")
            entry.grid(row=i + 1, column=num_destinos + 1, padx=5, pady=5)
            supply_entries.append(entry)
        
        # Crear entradas para demandas
        global demand_entries
        demand_entries = []
        ttk.Label(frame_tabla, text="Demand", font=("Arial", 10, "bold")).grid(row=num_fuentes + 1, column=0, columnspan=num_destinos, pady=5)
        
        for j in range(num_destinos):
            entry = ttk.Entry(frame_tabla, width=5, justify="center")
            entry.grid(row=num_fuentes + 2, column=j, padx=5, pady=5)
            demand_entries.append(entry)
    
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce números válidos para fuentes y destinos.")


def resolver_vogel():
    try:
        supply = [int(entry.get()) for entry in supply_entries]
        demand = [int(entry.get()) for entry in demand_entries]
        cost_matrix = [[int(entry.get()) for entry in row] for row in cost_entries]
        
        cost, allocations = calcular_vogel(cost_matrix, supply, demand)
        
        result_text = f"Costo total mínimo: {cost}\nAsignaciones:\n{allocations}"
        messagebox.showinfo("Resultado", result_text)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# Interfaz gráfica
app = tk.Tk()
app.title("Método de Vogel")
app.geometry("600x600")
app.resizable(False, False)

# Estilo
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10))

# Encabezado
header = ttk.Label(app, text="Método de Vogel para Transporte", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Entradas para número de fuentes y destinos
frame_input = ttk.Frame(app)
frame_input.pack(pady=10)

ttk.Label(frame_input, text="Número de Fuentes:").grid(row=0, column=0, padx=5, pady=5)
entry_fuentes = ttk.Entry(frame_input, width=5)
entry_fuentes.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Número de Destinos:").grid(row=1, column=0, padx=5, pady=5)
entry_destinos = ttk.Entry(frame_input, width=5)
entry_destinos.grid(row=1, column=1, padx=5, pady=5)

btn_generar = ttk.Button(frame_input, text="Generar Tabla", command=generar_tabla)
btn_generar.grid(row=2, column=0, columnspan=2, pady=10)

# Marco para la tabla
frame_tabla = ttk.Frame(app)
frame_tabla.pack(pady=10)

btn_resolver = ttk.Button(app, text="Resolver", command=resolver_vogel)
btn_resolver.pack(pady=20)

app.mainloop()
