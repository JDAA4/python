import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


class TransportSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Transport Problem Solver")
        self.root.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self.root, text="Transport Problem Solver", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Input frame
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Number of Sources:").grid(row=0, column=0, padx=5, pady=5)
        self.sources_entry = ttk.Entry(input_frame, width=10)
        self.sources_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Number of Destinations:").grid(row=0, column=2, padx=5, pady=5)
        self.destinations_entry = ttk.Entry(input_frame, width=10)
        self.destinations_entry.grid(row=0, column=3, padx=5, pady=5)

        create_button = ttk.Button(input_frame, text="Create Grid", command=self.create_grid)
        create_button.grid(row=0, column=4, padx=10)

        # Grid frame
        self.grid_frame = ttk.Frame(self.root, padding=10)
        self.grid_frame.pack()

    def create_grid(self):
        try:
            self.num_sources = int(self.sources_entry.get())
            self.num_destinations = int(self.destinations_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for sources and destinations.")
            return

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.cost_entries = []
        self.supply_entries = []
        self.demand_entries = []

        # Create cost grid
        ttk.Label(self.grid_frame, text="Cost Matrix", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=self.num_destinations + 2, pady=10)
        for i in range(self.num_sources):
            row = []
            for j in range(self.num_destinations):
                entry = ttk.Entry(self.grid_frame, width=5, justify="center")
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(entry)
            self.cost_entries.append(row)

        # Create supply inputs
        for i in range(self.num_sources):
            entry = ttk.Entry(self.grid_frame, width=5, justify="center")
            entry.grid(row=i + 1, column=self.num_destinations + 1, padx=5, pady=5)
            self.supply_entries.append(entry)

        # Create demand inputs
        for j in range(self.num_destinations):
            entry = ttk.Entry(self.grid_frame, width=5, justify="center")
            entry.grid(row=self.num_sources + 1, column=j, padx=5, pady=5)
            self.demand_entries.append(entry)

        ttk.Button(self.grid_frame, text="Solve", command=self.solve).grid(
            row=self.num_sources + 2, column=0, columnspan=self.num_destinations + 2, pady=10
        )

    def solve(self):
        try:
            cost_matrix = np.array([[int(entry.get()) for entry in row] for row in self.cost_entries])
            supply = np.array([int(entry.get()) for entry in self.supply_entries])
            demand = np.array([int(entry.get()) for entry in self.demand_entries])
        except ValueError:
            messagebox.showerror("Input Error", "Please fill all cells with valid integers.")
            return

        if sum(supply) != sum(demand):
            messagebox.showerror("Balance Error", "Supply and demand totals must be equal.")
            return

        allocation = self.northwest_corner(cost_matrix, supply.copy(), demand.copy())
        if allocation is not None:
            total_cost = self.calculate_total_cost(allocation, cost_matrix)
            self.show_solution(allocation, total_cost)
        else:
            messagebox.showerror("Error", "Failed to solve the problem.")

    def northwest_corner(self, cost, supply, demand):
        m, n = cost.shape
        allocation = np.zeros_like(cost)

        i, j = 0, 0
        while i < m and j < n:
            allocation[i][j] = min(supply[i], demand[j])
            supply[i] -= allocation[i][j]
            demand[j] -= allocation[i][j]
            if supply[i] == 0:
                i += 1
            elif demand[j] == 0:
                j += 1

        return allocation

    def calculate_total_cost(self, allocation, cost):
        return np.sum(allocation * cost)

    def show_solution(self, allocation, total_cost):
        solution_window = tk.Toplevel(self.root)
        solution_window.title("Solution")
        solution_window.geometry("400x300")
        ttk.Label(solution_window, text="Optimal Allocation", font=("Arial", 14, "bold")).pack(pady=10)

        frame = ttk.Frame(solution_window, padding=10)
        frame.pack()

        for i, row in enumerate(allocation):
            for j, val in enumerate(row):
                ttk.Label(frame, text=f"{int(val)}", relief="solid", width=5, anchor="center").grid(row=i, column=j, padx=5, pady=5)

        ttk.Label(solution_window, text=f"Total Cost: {total_cost}", font=("Arial", 12, "bold")).pack(pady=10)


# Run the application
root = tk.Tk()
app = TransportSolver(root)
root.mainloop()
