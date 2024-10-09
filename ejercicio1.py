import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Multifuncional de Matrices")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Estilos
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))

        # Header
        header = ttk.Label(root, text="Calculadora Multifuncional de Matrices", style='Header.TLabel', background="#f0f0f0")
        header.pack(pady=10)

        # Frame para seleccionar tamaño de matriz
        size_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        size_frame.pack(pady=10, padx=10, fill='x')

        size_label = ttk.Label(size_frame, text="Tamaño de la matriz (n x n):")
        size_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        self.size_entry = ttk.Entry(size_frame, width=5)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5, sticky='W')

        generate_button = ttk.Button(size_frame, text="Generar Matriz", command=self.generate_matrix)
        generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Frame para ingresar matrices
        self.matrix_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        self.matrix_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Frame para botones de operaciones
        operations_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        operations_frame.pack(pady=10, padx=10, fill='x')

        gauss_button = ttk.Button(operations_frame, text="Método Gauss-Jordan", command=self.gauss_jordan)
        gauss_button.grid(row=0, column=0, padx=10, pady=5)

        cramer_button = ttk.Button(operations_frame, text="Regla de Cramer", command=self.cramer)
        cramer_button.grid(row=0, column=1, padx=10, pady=5)

        multiply_button = ttk.Button(operations_frame, text="Multiplicación de Matrices", command=self.multiply)
        multiply_button.grid(row=0, column=2, padx=10, pady=5)

        inverse_button = ttk.Button(operations_frame, text="Calcular Inversa", command=self.inverse)
        inverse_button.grid(row=0, column=3, padx=10, pady=5)

        # Frame para resultados
        result_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)

        result_label = ttk.Label(result_frame, text="Resultados:", style='Header.TLabel')
        result_label.pack(anchor='w')

        self.result_text = tk.Text(result_frame, height=10, wrap='word', bg="#ffffff")
        self.result_text.pack(fill='both', expand=True)

        self.matrix_entries = []  # Para almacenar las entradas de la matriz
        self.second_matrix_entries = []  # Para la segunda matriz en multiplicación

    def generate_matrix(self):
        # Limpiar entradas previas
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []
        self.second_matrix_entries = []

        try:
            size = int(self.size_entry.get())
            if size < 2 or size > 5:
                messagebox.showerror("Error", "Por favor, ingrese un tamaño entre 2 y 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido para el tamaño de la matriz.")
            return

        # Crear pestañas para una o dos matrices según la operación
        self.notebook = ttk.Notebook(self.matrix_frame)
        self.notebook.pack(fill='both', expand=True)

        # Pestaña para la primera matriz
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Matriz A')

        ttk.Label(self.tab1, text="Ingrese los elementos de la Matriz A:").pack(pady=5)

        matrix_a_frame = ttk.Frame(self.tab1)
        matrix_a_frame.pack()

        for i in range(size):
            row = []
            for j in range(size):
                entry = ttk.Entry(matrix_a_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.matrix_entries.append(row)

        # Pestaña para la segunda matriz (solo para multiplicación)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Matriz B')

        ttk.Label(self.tab2, text="Ingrese los elementos de la Matriz B:").pack(pady=5)

        matrix_b_frame = ttk.Frame(self.tab2)
        matrix_b_frame.pack()

        for i in range(size):
            row = []
            for j in range(size):
                entry = ttk.Entry(matrix_b_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.second_matrix_entries.append(row)

    def get_matrix(self, entries):
        matrix = []
        try:
            for row in entries:
                matrix_row = []
                for entry in row:
                    value = float(entry.get())
                    matrix_row.append(value)
                matrix.append(matrix_row)
            return np.array(matrix)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese solo números en las matrices.")
            return None

    def gauss_jordan(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return

        try:
            n = matrix.shape[0]
            augmented = np.hstack((matrix, np.identity(n)))
            for i in range(n):
                # Hacer que el elemento diagonal sea 1
                if augmented[i][i] == 0:
                    # Buscar una fila para intercambiar
                    for j in range(i+1, n):
                        if augmented[j][i] != 0:
                            augmented[[i, j]] = augmented[[j, i]]
                            break
                    else:
                        raise ValueError("La matriz no es invertible.")
                augmented[i] = augmented[i] / augmented[i][i]
                # Hacer que los demás elementos en la columna sean 0
                for j in range(n):
                    if j != i:
                        augmented[j] = augmented[j] - augmented[j][i] * augmented[i]
            inverse = augmented[:, n:]
            self.result_text.insert(tk.END, "Matriz Inversa (Gauss-Jordan):\n")
            self.result_text.insert(tk.END, np.round(inverse, 3))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cramer(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return

        try:
            det = np.linalg.det(matrix)
            if det == 0:
                raise ValueError("El sistema no tiene solución única (determinante es cero).")
            inverse = np.linalg.inv(matrix)
            self.result_text.insert(tk.END, "Matriz Inversa (Regla de Cramer):\n")
            self.result_text.insert(tk.END, np.round(inverse, 3))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multiply(self):
        self.result_text.delete(1.0, tk.END)
        matrix_a = self.get_matrix(self.matrix_entries)
        matrix_b = self.get_matrix(self.second_matrix_entries)
        if matrix_a is None or matrix_b is None:
            return

        try:
            product = np.dot(matrix_a, matrix_b)
            self.result_text.insert(tk.END, "Producto de Matriz A y Matriz B:\n")
            self.result_text.insert(tk.END, np.round(product, 3))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def inverse(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return

        try:
            det = np.linalg.det(matrix)
            if det == 0:
                raise ValueError("La matriz no es invertible (determinante es cero).")
            inverse = np.linalg.inv(matrix)
            self.result_text.insert(tk.END, "Matriz Inversa:\n")
            self.result_text.insert(tk.END, np.round(inverse, 3))
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Inicialización de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculator(root)
    root.mainloop()