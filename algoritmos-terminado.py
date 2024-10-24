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
        self.matrix_frame.pack(pady=10, padx=10, fill='both')

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

        self.matrix_entries = []
        self.second_matrix_entries = []
        self.cramer_entries = []  # Entrada para el método de Cramer

    def generate_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []
        self.second_matrix_entries = []
        self.cramer_entries = []

        try:
            size = int(self.size_entry.get())
            if size < 2 or size > 5:
                messagebox.showerror("Error", "Por favor, ingrese un tamaño entre 2 y 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido para el tamaño de la matriz.")
            return

        self.notebook = ttk.Notebook(self.matrix_frame)
        self.notebook.pack(fill='both', expand=True)

        # Matriz A
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

        # Matriz B
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

        # Matriz para Cramer (n x (n+1))
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Matriz Cramer')

        ttk.Label(self.tab3, text="Ingrese los coeficientes y términos independientes:").pack(pady=5)

        matrix_cramer_frame = ttk.Frame(self.tab3)
        matrix_cramer_frame.pack()

        for i in range(size):
            row = []
            for j in range(size + 1):  # Matriz extendida (n x (n+1))
                entry = ttk.Entry(matrix_cramer_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.cramer_entries.append(row)

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

    # Método de Gauss-Jordan
    def gauss_jordan(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return
        try:
            n = matrix.shape[0]
            augmented = np.hstack((matrix, np.identity(n)))
            steps = []

            for i in range(n):
                # Verificar si el pivote es muy cercano a 0 (para evitar errores de comparación con matrices)
                if np.isclose(augmented[i][i], 0):
                    for j in range(i + 1, n):
                        # Intercambiar filas si hay una que no tenga un pivote cercano a 0
                        if not np.isclose(augmented[j][i], 0):
                            augmented[[i, j]] = augmented[[j, i]]
                            steps.append(f"Intercambio de fila {i + 1} con fila {j + 1}")
                            break
                    else:
                        raise ValueError("La matriz no es invertible o tiene soluciones infinitas.")

                # Normalizar la fila pivote
                pivot = augmented[i][i]
                augmented[i] = augmented[i] / pivot
                steps.append(f"Dividir fila {i + 1} por {pivot:.3f} para hacer el pivote igual a 1")

                # Hacer que los demás elementos en la columna sean 0
                for j in range(n):
                    if j != i:
                        factor = augmented[j][i]
                        augmented[j] = augmented[j] - factor * augmented[i]
                        steps.append(f"Restar {factor:.3f} * fila {i + 1} de fila {j + 1}")

            result = augmented[:, :n] 
            result = np.where(np.isclose(result, 0), 0, result)  # Redondear valores cercanos a 0
            self.result_text.insert(tk.END, "Proceso de Gauss-Jordan:\n")
            for step in steps:
                self.result_text.insert(tk.END, step + "\n")

            # Determinar el tipo de solución
            det = np.linalg.det(matrix)
            if np.isclose(det, 0):
                self.result_text.insert(tk.END, "\nLa matriz no tiene solución única.\n")
            else:
                self.result_text.insert(tk.END, "\nLa matriz tiene solución única.\n")

            self.result_text.insert(tk.END, "\nMatriz resultante (Gauss-Jordan):\n")
            self.result_text.insert(tk.END, np.round(result, 3))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Método de Cramer
    def cramer(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.cramer_entries)  # Usar la nueva matriz para Cramer
        if matrix is None:
            return
        
        try:
            n = matrix.shape[0]
            m = matrix.shape[1]

            if m != n + 1:  # Verifica que la matriz sea (n x (n + 1))
                raise ValueError("La matriz debe ser de tamaño n x (n + 1).")

            A = matrix[:, :-1]  # Coeficientes
            b = matrix[:, -1]  # Términos independientes

            det_A = np.linalg.det(A)
            if np.isclose(det_A, 0):
                raise ValueError("La matriz de coeficientes no es invertible o tiene infinitas soluciones.")

            steps = []
            solutions = []

            # Calcular determinantes y soluciones
            for i in range(n):
                Ai = np.copy(A)
                Ai[:, i] = b
                det_Ai = np.linalg.det(Ai)
                x_i = det_Ai / det_A
                solutions.append(x_i)
                steps.append(f"Det(A{i + 1}) = {det_Ai:.3f}, x{i + 1} = {det_Ai:.3f} / {det_A:.3f} = {x_i:.3f}")

            # Mostrar pasos y soluciones
            self.result_text.insert(tk.END, "Proceso de la Regla de Cramer:\n")
            for step in steps:
                self.result_text.insert(tk.END, step + "\n")

            # Verificar el tipo de solución
            if np.isclose(det_A, 0):
                self.result_text.insert(tk.END, "\nEl sistema tiene infinitas soluciones o no tiene solución.\n")
            else:
                self.result_text.insert(tk.END, "\nSolución única:\n")
                for i, sol in enumerate(solutions):
                    self.result_text.insert(tk.END, f"x{i + 1} = {sol:.3f}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    # Método de multiplicación
    def multiply(self):
        self.result_text.delete(1.0, tk.END)
        matrix_a = self.get_matrix(self.matrix_entries)
        matrix_b = self.get_matrix(self.second_matrix_entries)
        if matrix_a is None or matrix_b is None:
            return
        try:
            result = np.dot(matrix_a, matrix_b)
            steps = []
            steps.append("Multiplicación de matrices:\n")
            for i in range(matrix_a.shape[0]):
                for j in range(matrix_b.shape[1]):
                    sum_product = 0
                    for k in range(matrix_a.shape[1]):
                        product = matrix_a[i][k] * matrix_b[k][j]
                        sum_product += product
                        steps.append(f"{matrix_a[i][k]} * {matrix_b[k][j]} (Fila {i+1}, Columna {j+1})")
                    steps.append(f"Suma: {sum_product}\n")
            self.result_text.insert(tk.END, "Proceso de Multiplicación de Matrices:\n")
            for step in steps:
                self.result_text.insert(tk.END, step)
            self.result_text.insert(tk.END, "\nResultado de la multiplicación:\n")
            self.result_text.insert(tk.END, np.round(result, 3))
        except ValueError:
            messagebox.showerror("Error", "Las matrices no son compatibles para la multiplicación.")

    # Método de inversa
    def inverse(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return
        try:
            inv_matrix = np.linalg.inv(matrix)
            steps = ["Cálculo de la Inversa:\n"]
            det_matrix = np.linalg.det(matrix)

            steps.append(f"Determinante de la matriz: {det_matrix:.3f}\n")
            if det_matrix == 0:
                steps.append("La matriz no es invertible.")
            else:
                for i in range(matrix.shape[0]):
                    for j in range(matrix.shape[1]):
                        minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                        cofactor = ((-1) ** (i + j)) * np.linalg.det(minor)
                        steps.append(f"Cofactor C[{i+1},{j+1}] = {cofactor:.3f}\n")

                steps.append("\nMatriz Inversa:\n")
                for row in inv_matrix:
                    steps.append(" | ".join(f"{value:.3f}" for value in row) + "\n")

            self.result_text.insert(tk.END, "".join(steps))
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "La matriz no es invertible.")

# Crear la ventana de la calculadora
root = tk.Tk()
calculator = MatrixCalculator(root)
root.mainloop()