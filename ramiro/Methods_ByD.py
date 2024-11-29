import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class TransportSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Método de Transporte")
        self.master.geometry("1000x900")
        
        self.setup_ui()
        
    def setup_ui(self):
        ttk.Label(
            self.master, 
            text="Método de Transporte", 
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
        
        ttk.Label(config_frame, text="Método:").grid(row=2, column=0, padx=5)
        self.method_var = tk.StringVar()
        self.method_var.set("Esquina Noroeste")
        
        method_options = ["Esquina Noroeste", "Costo Mínimo", "Vogel"]
        method_menu = ttk.OptionMenu(config_frame, self.method_var, *method_options)
        method_menu.grid(row=2, column=1, padx=5)
        
        ttk.Label(config_frame, text="Método de Resolución:").grid(row=3, column=0, padx=5)
        self.resolution_var = tk.StringVar()
        self.resolution_var.set("Banquillo")
        
        resolution_options = ["Banquillo", "DiMO"]
        resolution_menu = ttk.OptionMenu(config_frame, self.resolution_var, *resolution_options)
        resolution_menu.grid(row=3, column=1, padx=5)
        
        ttk.Button(
            config_frame, 
            text="Generar Tabla", 
            command=self.generar_tabla
        ).grid(row=4, column=0, columnspan=2, pady=10)
        
        self.frame_tabla = ttk.Frame(self.master)
        self.frame_tabla.pack(pady=10)
        
        ttk.Button(
            self.master, 
            text="Resolver Método de Transporte", 
            command=self.resolver_transporte
        ).pack(pady=10)
        
        self.resultado_text = tk.Text(
            self.master, 
            height=30, 
            width=100, 
            font=("Courier", 10)
        )
        self.resultado_text.pack(pady=10)

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

    def resolver_transporte(self):
        try:
            supply = [int(entry.get()) for entry in self.supply_entries]
            demand = [int(entry.get()) for entry in self.demand_entries]
            cost_matrix = [[int(entry.get()) for entry in row] for row in self.cost_entries]
            
            if sum(supply) != sum(demand):
                messagebox.showwarning("Advertencia", "La suma de supply y demand no es igual")
            
            # Elige el método de resolución
            method = self.method_var.get()
            if method == "Esquina Noroeste":
                total_cost, allocations, steps = self.metodo_esquina_noroeste(cost_matrix, supply, demand)
            elif method == "Costo Mínimo":
                total_cost, allocations, steps = self.metodo_costo_minimo(cost_matrix, supply, demand)
            elif method == "Vogel":
                total_cost, allocations, steps = self.metodo_vogel(cost_matrix, supply, demand)
            elif method == "Esquina Noroeste":
                total_cost, allocations, steps = self.metodo_esquina_noroeste(cost_matrix, supply, demand)


            # Elige el método de optimización
            resolution_method = self.resolution_var.get()
            if resolution_method == "Banquillo":
                total_cost, steps = self.metodo_banquillo(cost_matrix, supply, demand, total_cost, steps)
            elif resolution_method == "DiMO":
                total_cost, steps = self.metodo_dimo(cost_matrix, supply, demand, total_cost, steps)
            
            result_text = f"Resultados del Método: {method} y Resolución: {resolution_method}\n"
            for i, step in enumerate(steps):
                result_text += f"Iteración {i+1}:\n{step}\n"
                result_text += "-" * 80 + "\n"
            result_text += f"Costo total: {total_cost}\n"

            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def metodo_esquina_noroeste(self, cost_matrix, supply, demand):
        rows, cols = len(supply), len(demand)
        allocations = np.zeros((rows, cols), dtype=int)
        total_cost = 0
        steps = []
        
        i, j = 0, 0
        while sum(supply) > 0 and sum(demand) > 0:
            allocated = min(supply[i], demand[j])
            allocations[i][j] = allocated
            total_cost += allocated * cost_matrix[i][j]
            supply[i] -= allocated
            demand[j] -= allocated

            current_allocation_table = "\n".join(
                ["\t".join(map(str, row)) for row in allocations]
            )
            steps.append(
                f"Asignación: {allocated} unidades de Fuente {i+1} a Destino {j+1}. "
                f"Costo acumulado: {total_cost}\n"
                f"Estado de la tabla de asignaciones:\n{current_allocation_table}\n"
            )

            if supply[i] == 0:
                i += 1
            if demand[j] == 0:
                j += 1
        
        return total_cost, allocations, steps
    
    def metodo_costo_minimo(self, cost_matrix, supply, demand):
        rows, cols = len(supply), len(demand)
        allocations = np.zeros((rows, cols), dtype=int)
        total_cost = 0
        steps = []
        
        while sum(supply) > 0 and sum(demand) > 0:
            min_cost = float("inf")
            min_cell = (-1, -1)
            for i in range(rows):
                for j in range(cols):
                    if supply[i] > 0 and demand[j] > 0 and cost_matrix[i][j] < min_cost:
                        min_cost = cost_matrix[i][j]
                        min_cell = (i, j)

            i, j = min_cell
            allocated = min(supply[i], demand[j])
            allocations[i][j] = allocated
            total_cost += allocated * cost_matrix[i][j]
            supply[i] -= allocated
            demand[j] -= allocated

            current_allocation_table = "\n".join(
                ["\t".join(map(str, row)) for row in allocations]
            )
            steps.append(
                f"Asignación: {allocated} unidades de Fuente {i+1} a Destino {j+1}. "
                f"Costo acumulado: {total_cost}\n"
                f"Estado de la tabla de asignaciones:\n{current_allocation_table}\n"
            )

        return total_cost, allocations, steps

    def metodo_vogel(self, cost_matrix, supply, demand):
        rows, cols = len(supply), len(demand)
        allocations = np.zeros((rows, cols), dtype=int)
        total_cost = 0
        steps = []

        while sum(supply) > 0 and sum(demand) > 0:
            # Calcula las penalizaciones
            row_penalties = []
            col_penalties = []

            for i in range(rows):
                if supply[i] > 0:
                    sorted_row = sorted([cost_matrix[i][j] for j in range(cols) if demand[j] > 0])
                    if len(sorted_row) > 1:
                        row_penalties.append(sorted_row[1] - sorted_row[0])
                    else:
                        row_penalties.append(0)
                else:
                    row_penalties.append(-1)

            for j in range(cols):
                if demand[j] > 0:
                    sorted_col = sorted([cost_matrix[i][j] for i in range(rows) if supply[i] > 0])
                    if len(sorted_col) > 1:
                        col_penalties.append(sorted_col[1] - sorted_col[0])
                    else:
                        col_penalties.append(0)
                else:
                    col_penalties.append(-1)

            # Encuentra el índice de la penalización máxima
            max_penalty_row = max(row_penalties)
            max_penalty_col = max(col_penalties)

            if max_penalty_row >= max_penalty_col:
                row_index = row_penalties.index(max_penalty_row)
                # Asignamos de la fila con la penalización máxima
                valid_cols = [j for j in range(cols) if demand[j] > 0]
                sorted_cols = sorted(valid_cols, key=lambda j: cost_matrix[row_index][j])
                min_cost_idx = sorted_cols[0]
                allocated = min(supply[row_index], demand[min_cost_idx])
                allocations[row_index][min_cost_idx] = allocated
                total_cost += allocated * cost_matrix[row_index][min_cost_idx]
                supply[row_index] -= allocated
                demand[min_cost_idx] -= allocated
                steps.append(f"Penalización de fila {row_index+1}: {max_penalty_row}")
                steps.append(f"Asignación: {allocated} unidades de Fuente {row_index+1} a Destino {min_cost_idx+1}. Costo acumulado: {total_cost}")
            else:
                col_index = col_penalties.index(max_penalty_col)
                # Asignamos de la columna con la penalización máxima
                valid_rows = [i for i in range(rows) if supply[i] > 0]
                sorted_rows = sorted(valid_rows, key=lambda i: cost_matrix[i][col_index])
                min_cost_idx = sorted_rows[0]
                allocated = min(supply[min_cost_idx], demand[col_index])
                allocations[min_cost_idx][col_index] = allocated
                total_cost += allocated * cost_matrix[min_cost_idx][col_index]
                supply[min_cost_idx] -= allocated
                demand[col_index] -= allocated
                steps.append(f"Penalización de columna {col_index+1}: {max_penalty_col}")
                steps.append(f"Asignación: {allocated} unidades de Fuente {min_cost_idx+1} a Destino {col_index+1}. Costo acumulado: {total_cost}")

            # Verificar si las filas o columnas están agotadas
            for i in range(rows):
                if supply[i] == 0:
                    print(f"Fila {i+1} agotada")
            for j in range(cols):
                if demand[j] == 0:
                    print(f"Columna {j+1} agotada")

            # Mostrar el estado de la tabla después de cada asignación
            current_allocation_table = "\n".join(
                ["\t".join(map(str, row)) for row in allocations]
            )
            steps.append(f"Estado actual de la tabla de asignaciones:\n{current_allocation_table}\n")

        return total_cost, allocations, steps


    def metodo_banquillo(self, cost_matrix, supply, demand, total_cost, steps):
        rows, cols = len(supply), len(demand)
        allocations = np.zeros((rows, cols), dtype=int)

        # Inicialización del paso
        current_step = f"Inicio de la mejora Banquillo: Costo actual = {total_cost}\n"
        steps.append(current_step)

        # Mejorar la solución realizando cambios iterativos
        mejora_realizada = True
        while mejora_realizada:
            mejora_realizada = False
            for i in range(rows):
                for j in range(cols):
                    if allocations[i][j] == 0 and supply[i] > 0 and demand[j] > 0:
                        # Calcula el costo si realizamos la asignación
                        temp_alloc = min(supply[i], demand[j])
                        temp_cost = cost_matrix[i][j] * temp_alloc
                        nuevo_costo_total = total_cost + temp_cost

                        # Compara si esta nueva asignación mejora el costo total
                        if nuevo_costo_total < total_cost:
                            # Realiza la asignación y actualiza el costo
                            allocations[i][j] = temp_alloc
                            total_cost = nuevo_costo_total
                            supply[i] -= temp_alloc
                            demand[j] -= temp_alloc

                            current_step = f"Mejora en Fuente {i+1} y Destino {j+1}: Asignación = {temp_alloc}, Costo acumulado = {total_cost}\n"
                            steps.append(current_step)

                            mejora_realizada = True
                            break
                if mejora_realizada:
                    break

        return total_cost, steps

    def metodo_dimo(self, cost_matrix, supply, demand, total_cost, steps):
        rows, cols = len(supply), len(demand)
        allocations = np.zeros((rows, cols), dtype=int)

        # Inicialización del paso
        current_step = f"Inicio de la mejora DiMO: Costo actual = {total_cost}\n"
        steps.append(current_step)

        # Crear una lista de candidatos para movimientos directos
        while sum(supply) > 0 and sum(demand) > 0:
            mejores_movimientos = []
            
            # Recorre todos los posibles movimientos
            for i in range(rows):
                for j in range(cols):
                    if allocations[i][j] == 0 and supply[i] > 0 and demand[j] > 0:
                        movimiento = min(supply[i], demand[j])
                        costo = cost_matrix[i][j] * movimiento
                        mejores_movimientos.append((i, j, costo, movimiento))

            # Ordenar por el costo más bajo
            mejores_movimientos.sort(key=lambda x: x[2])

            # Tomar el mejor movimiento (el de costo más bajo)
            if mejores_movimientos:
                i, j, costo, movimiento = mejores_movimientos[0]
                allocations[i][j] = movimiento
                total_cost += costo
                supply[i] -= movimiento
                demand[j] -= movimiento

                current_step = f"Movimiento en Fuente {i+1} y Destino {j+1}: Asignación = {movimiento}, Costo acumulado = {total_cost}\n"
                steps.append(current_step)
            
        return total_cost, steps

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportSolver(root)
    root.mainloop()