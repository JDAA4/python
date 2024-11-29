import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd

class DIMOTransportSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("DIMO Transportation Method Solver")
        self.master.geometry("1000x900")
        
        self.setup_ui()
        
    def setup_ui(self):
        ttk.Label(
            self.master, 
            text="Método DIMO para Problemas de Transporte", 
            font=("Courier", 16, "bold")
        ).pack(pady=10)
        
        config_frame = ttk.Frame(self.master)
        config_frame.pack(pady=10)
        
        ttk.Label(config_frame, text="Número de Fuentes:").grid(row=0, column=0, padx=5)
        self.entry_fuentes = ttk.Entry(config_frame, width=5)
        self.entry_fuentes.grid(row=0, column=1, padx=5)
        
        ttk.Label(config_frame, text="Número de Destinos:").grid(row=1, column=0, padx=5)
        self.entry_destinos = ttk.Entry(config_frame, width=5)
        self.entry_destinos.grid(row=1, column=1, padx=5)
        
        ttk.Button(
            config_frame, 
            text="Generar Tabla", 
            command=self.generar_tabla
        ).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.frame_tabla = ttk.Frame(self.master)
        self.frame_tabla.pack(pady=10)
        
        ttk.Button(
            self.master, 
            text="Resolver DIMO", 
            command=self.resolver_dimo
        ).pack(pady=10)
        
        self.resultado_text = tk.Text(
            self.master, 
            height=30, 
            width=100, 
            font=("Courier", 10)
        )
        self.resultado_text.pack(pady=10)
        
    def format_tableau(self, cost_matrix, supply, demand, allocations=None):
        rows, cols = len(supply), len(demand)
        tableau = ""
        
        # Header
        tableau += " " * 10
        for j in range(cols):
            tableau += f"Destino {j+1:<8} "
        tableau += "Supply\n"
        
        # Data rows
        for i in range(rows):
            tableau += f"Fuente {i+1:<2}"
            for j in range(cols):
                if allocations is not None and allocations[i][j] > 0:
                    tableau += f"{cost_matrix[i][j]}[{int(allocations[i][j])}]".ljust(12)
                else:
                    tableau += f"{cost_matrix[i][j]:<12}"
            tableau += f"{int(supply[i])}\n"
        
        # Demand row
        tableau += "Demand".ljust(10)
        for j in range(cols):
            tableau += f"{int(demand[j]):<12}"
        tableau += "\n"
        
        return tableau

    def generar_tabla(self):
        try:
            num_fuentes = int(self.entry_fuentes.get())
            num_destinos = int(self.entry_destinos.get())
            
            for widget in self.frame_tabla.winfo_children():
                widget.destroy()
            
            self.cost_entries = []
            self.supply_entries = []
            self.demand_entries = []
            
            ttk.Label(
                self.frame_tabla, 
                text="Matriz de Costos", 
                font=("Courier", 12, "bold")
            ).grid(row=0, column=0, columnspan=num_destinos, pady=5)
            
            for i in range(num_fuentes):
                row_entries = []
                for j in range(num_destinos):
                    entry = ttk.Entry(self.frame_tabla, width=5, justify="center")
                    entry.grid(row=i+1, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.cost_entries.append(row_entries)
            
            ttk.Label(
                self.frame_tabla, 
                text="Supply", 
                font=("Courier", 10, "bold")
            ).grid(row=0, column=num_destinos+1, padx=5)
            
            for i in range(num_fuentes):
                entry = ttk.Entry(self.frame_tabla, width=5, justify="center")
                entry.grid(row=i+1, column=num_destinos+1, padx=2)
                self.supply_entries.append(entry)
            
            ttk.Label(
                self.frame_tabla, 
                text="Demand", 
                font=("Courier", 10, "bold")
            ).grid(row=num_fuentes+1, column=0, columnspan=num_destinos, pady=5)
            
            for j in range(num_destinos):
                entry = ttk.Entry(self.frame_tabla, width=5, justify="center")
                entry.grid(row=num_fuentes+2, column=j, padx=2)
                self.demand_entries.append(entry)
                
        except ValueError:
            messagebox.showerror("Error", "Introduce números válidos para fuentes y destinos")

    def calcular_dimo(self, cost_matrix, supply, demand):
        rows, cols = len(supply), len(demand)
        total_cost = 0
        allocations = np.zeros((rows, cols), dtype=int)
        steps = []
        
        steps.append({
            'iteration': 0,
            'tableau': self.format_tableau(cost_matrix, supply.copy(), demand.copy()),
            'description': 'Estado inicial',
            'total_cost': 0
        })
        
        supply_copy = supply.copy()
        demand_copy = demand.copy()
        iteration = 1
        
        while sum(supply_copy) > 0 and sum(demand_copy) > 0:
            min_cost = float('inf')
            min_pos = (-1, -1)
            
            for i in range(rows):
                for j in range(cols):
                    if supply_copy[i] > 0 and demand_copy[j] > 0 and cost_matrix[i][j] < min_cost:
                        min_cost = cost_matrix[i][j]
                        min_pos = (i, j)
            
            if min_pos == (-1, -1):
                break
                
            i, j = min_pos
            x = min(supply_copy[i], demand_copy[j])
            allocations[i][j] = x
            total_cost += x * cost_matrix[i][j]
            supply_copy[i] -= x
            demand_copy[j] -= x
            
            steps.append({
                'iteration': iteration,
                'tableau': self.format_tableau(cost_matrix, supply_copy, demand_copy, allocations),
                'description': f'Asignación: {x} unidades de Fuente {i+1} a Destino {j+1}',
                'total_cost': total_cost
            })
            
            iteration += 1
        
        return total_cost, allocations, steps

    def resolver_dimo(self):
        try:
            supply = [int(entry.get()) for entry in self.supply_entries]
            demand = [int(entry.get()) for entry in self.demand_entries]
            cost_matrix = [[int(entry.get()) for entry in row] for row in self.cost_entries]
            
            if sum(supply) != sum(demand):
                messagebox.showwarning("Advertencia", "La suma de supply y demand no es igual")
            
            total_cost, allocations, steps = self.calcular_dimo(cost_matrix, supply, demand)
            
            result_text = ""
            for i, step in enumerate(steps):
                if i == len(steps) - 1:  # Final iteration
                    result_text += "\nIteración Final:\n"
                else:
                    result_text += f"\nIteración {step['iteration']}:\n"
                
                if 'description' in step:
                    result_text += f"{step['description']}\n"
                
                if i == len(steps) - 1:  # Final iteration
                    result_text += f"Costo total: {step['total_cost']}\n\n"
                else:
                    result_text += f"Costo acumulado: {step['total_cost']}\n\n"
                
                result_text += step['tableau']
                result_text += "-" * 80 + "\n"
        
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, result_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

def main():
    root = tk.Tk()
    app = DIMOTransportSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()