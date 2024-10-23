import tkinter as tk
from tkinter import Button, Toplevel, ttk, messagebox
from matplotlib import pyplot as plt
import numpy as np
import math

# Clase para la Calculadora de Álgebra Lineal
class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Multifuncional de Matrices")
        self.root.geometry("800x600")
        self.root.configure(bg="#282a36")  # Fondo de atras 

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')  # tema compatible con cambios de color
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10, background='#6272a4')
        self.style.map("TButton", background=[('active', '#44475a')])
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('TFrame', background='#282a36')

        # Header
        header = ttk.Label(root, text="Calculadora Multifuncional de Matrices", style='Header.TLabel', background="#f0f0f0")
        header.pack(pady=10)

        # Marco para seleccionar tamaño de matriz
        size_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        size_frame.pack(pady=10, padx=10, fill='x')

        size_label = ttk.Label(size_frame, text="Tamaño de la matriz (n x n):", style='TLabel')
        size_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        self.size_entry = ttk.Entry(size_frame, width=5)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5, sticky='W')

        generate_button = ttk.Button(size_frame, text="Generar Matriz", command=self.generate_matrix)
        generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Marco para ingresar matrices
        self.matrix_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        self.matrix_frame.pack(pady=10, padx=10, fill='both')

        # Marco para botones de operaciones
        operations_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        operations_frame.pack(pady=10, padx=10, fill='x')

        # Botones para las operaciones 
        gauss_button = ttk.Button(operations_frame, text="Método Gauss-Jordan", command=self.gauss_jordan)
        gauss_button.grid(row=0, column=0, padx=10, pady=5)

        cramer_button = ttk.Button(operations_frame, text="Regla de Cramer", command=self.cramer)
        cramer_button.grid(row=0, column=1, padx=10, pady=5)

        multiply_button = ttk.Button(operations_frame, text="Multiplicación de Matrices", command=self.multiply)
        multiply_button.grid(row=0, column=2, padx=10, pady=5)

        inverse_button = ttk.Button(operations_frame, text="Calcular Inversa", command=self.inverse)
        inverse_button.grid(row=0, column=3, padx=10, pady=5)

        # Botón para graficar ecuaciones
        plot_button = ttk.Button(operations_frame, text="Graficar Ecuaciones", command=self.plot_equations)
        plot_button.grid(row=0, column=4, padx=10, pady=5)

        # Marco para resultados
        result_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)

        result_label = ttk.Label(result_frame, text="Resultados:", style='Header.TLabel')
        result_label.pack(anchor='w')

        self.result_text = tk.Text(result_frame, height=10, wrap='word', bg="#44475a", fg="White", font=('Helvetica', 17), borderwidth=2)
        self.result_text.pack(fill='both', expand=True)

        # Variables que sirven para almacenar las entradas de las matrices 
        self.matrix_entries = []
        self.second_matrix_entries = []
        self.cramer_entries = []  # Entrada para el método de Cramer

    # Método para generar matrices según el tamaño que se especifique
    def generate_matrix(self):
        # limpia el marco de las matrices anteriores 
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

        # Crea pestañas para las diferentes matrices 
        self.notebook = ttk.Notebook(self.matrix_frame)
        self.notebook.pack(fill='both', expand=True)

        # Matriz A
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Matriz A')

        ttk.Label(self.tab1, text="Ingrese los elementos de la Matriz A:", background='#282a36', foreground='white').pack(pady=5)

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

        ttk.Label(self.tab2, text="Ingrese los elementos de la Matriz B:", background='#282a36', foreground='white').pack(pady=5)

        matrix_b_frame = ttk.Frame(self.tab2)
        matrix_b_frame.pack()

        for i in range(size):
            row = []
            for j in range(size):
                entry = ttk.Entry(matrix_b_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.second_matrix_entries.append(row)

        # pestaña Matriz para Cramer (n x (n+1))
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Matriz Cramer')

        ttk.Label(self.tab3, text="Ingrese los coeficientes y términos independientes:", background='#282a36', foreground='white').pack(pady=5)

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

    # Método de Gauss-Jordan mejorado para mostrar el procedimiento completo
    def gauss_jordan(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return
        try:
            n = matrix.shape[0]
            augmented = np.hstack((matrix, np.eye(n)))  # Matriz aumentada (A | I)
            steps = []

            for i in range(n):
                if np.isclose(augmented[i][i], 0):
                # Intercambiar con una fila que tenga un valor distinto de cero en la columna i
                    for j in range(i + 1, n):
                        if not np.isclose(augmented[j][i], 0):
                            augmented[[i, j]] = augmented[[j, i]]
                            steps.append(f"Intercambio de fila {i + 1} con fila {j + 1}")
                            break
                    else:
                        self.result_text.insert(tk.END, "El sistema no tiene solución o tiene infinitas soluciones.\n")
                        return

                pivot = augmented[i][i]
                augmented[i] = augmented[i] / pivot
                steps.append(f"Dividir fila {i + 1} por {pivot:.3f} para hacer el pivote igual a 1")

                for j in range(n):
                    if j != i:
                        factor = augmented[j][i]
                        augmented[j] -= factor * augmented[i]
                        steps.append(f"Restar {factor:.3f} * fila {i + 1} de fila {j + 1}")

        # Verificar si la matriz tiene una única solución
            if np.all(np.isclose(augmented[:, :-n], np.eye(n))):  # Si la matriz es la identidad
                self.result_text.insert(tk.END, "El sistema tiene solución única:\n")
                solutions = augmented[:, -n:]
                for i, sol in enumerate(solutions):
                    self.result_text.insert(tk.END, f"x{i + 1} = {sol[0]:.3f}\n")
            else:
                 self.result_text.insert(tk.END, "El sistema no tiene solución o tiene infinitas soluciones.\n")

            self.result_text.insert(tk.END, "\nMatriz final después de Gauss-Jordan:\n")
            self.result_text.insert(tk.END, np.round(augmented, 3))  # Imprimir la matriz final

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
            if det_A == 0:
                raise ValueError("La matriz de coeficientes no es invertible.")

            steps = []
            solutions = []
            for i in range(n):
                # Crear matriz Ai
                Ai = np.copy(A)
                Ai[:, i] = b
                det_Ai = np.linalg.det(Ai)
                x_i = det_Ai / det_A
                solutions.append(x_i)
                steps.append(f"Det(A{i + 1}) = {det_Ai:.3f}, x{i + 1} = {det_Ai:.3f} / {det_A:.3f} = {x_i:.3f}")

            self.result_text.insert(tk.END, "Proceso de la Regla de Cramer:\n")
            for step in steps:
                self.result_text.insert(tk.END, step + "\n")
            self.result_text.insert(tk.END, "\nSoluciones:\n")
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

    # Nueva función para graficar ecuaciones
    def plot_equations(self):
        matrix = self.get_matrix(self.matrix_entries)
        matrix = self.get_matrix(self.cramer_entries)
        if matrix is None:
            return

        try:
            # Extraer los coeficientes y términos independientes
            n = matrix.shape[0]
            A = matrix[:, :-1]  # Coeficientes
            b = matrix[:, -1]  # Términos independientes

            x = np.linspace(-10, 10, 400)  # Rango para la variable x
            plt.figure(figsize=(8, 6))

            # Graficar cada ecuación de la forma Ax + By = C
            for i in range(n):
                if A[i][1] != 0:  # Evitar división por cero
                    y = (b[i] - A[i][0] * x) / A[i][1]
                    plt.plot(x, y, label=f"Ecuación {i+1}")
                else:
                    plt.axvline(x=b[i] / A[i][0], color='r', linestyle='--', label=f'Ecuación {i+1} (x = {b[i] / A[i][0]:.2f})')

            plt.axhline(0, color='black',linewidth=0.5)
            plt.axvline(0, color='black',linewidth=0.5)
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
            plt.legend()
            plt.grid(True)
            plt.title("Gráfica de las Ecuaciones")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        
# Funciones de Matemática Discreta
def factorial(n):
    return math.factorial(n)

def combinaciones(n, r):
    return int(factorial(n) / (factorial(r) * factorial(n - r)))

def combinaciones_con_repeticion(n, r):
    return int(factorial(n + r - 1) / (factorial(r) * factorial(n - 1)))

def permutaciones(n, r):
    return int(factorial(n) / factorial(n - r))

def permutaciones_con_repeticion(n, r):
    return int(n ** r)

# Funciones de evento para botones
def calcular_combinaciones():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())
        if comb_tipo.get() == 1:  # Sin repetición
            if n >= r:
                resultado = combinaciones(n, r)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Combinaciones sin repetición: {resultado}\n")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Error: n debe ser mayor o igual a r.")
        else:  # Con repetición
            resultado = combinaciones_con_repeticion(n, r)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Combinaciones con repetición: {resultado}\n")
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: Ingresa valores válidos para n y r.")

def calcular_permutaciones():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())
        if perm_tipo.get() == 1:  # Sin repetición
            if n >= r:
                resultado = permutaciones(n, r)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Permutaciones sin repetición: {resultado}\n")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Error: n debe ser mayor o igual a r.")
        else:  # Con repetición
            resultado = permutaciones_con_repeticion(n, r)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Permutaciones con repetición: {resultado}\n")
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: Ingresa valores válidos para n y r.")

# Función para iniciar la calculadora de Matemática Discreta
def matematica_discreta():
    discreta_window = tk.Toplevel()
    discreta_window.title("Calculadora de Combinaciones y Permutaciones")
    discreta_window.geometry("600x400")
    discreta_window.configure(bg="#282a36")

    # Estilo
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10, background='#6272a4')
    style.map("TButton", background=[('active', '#44475a')])
    style.configure('TLabel', font=('Helvetica', 10))
    style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
    style.configure('TFrame', background='#282a36')

    # Header
    header = ttk.Label(discreta_window, text="Calculadora de Combinaciones y Permutaciones", style='Header.TLabel', background="#f0f0f0")
    header.pack(pady=10)

    # Marco para valores de n y r
    input_frame = ttk.Frame(discreta_window, padding=10, borderwidth=2, relief="groove")
    input_frame.pack(pady=10, padx=10, fill='x')

    global entry_n, entry_r, comb_tipo, perm_tipo, result_text

    label_n = ttk.Label(input_frame, text="Valor de n:", style='TLabel')
    label_n.grid(row=0, column=0, padx=5, pady=5, sticky='W')
    entry_n = ttk.Entry(input_frame, width=5)
    entry_n.grid(row=0, column=1, padx=5, pady=5, sticky='W')

    label_r = ttk.Label(input_frame, text="Valor de r:", style='TLabel')
    label_r.grid(row=1, column=0, padx=5, pady=5, sticky='W')
    entry_r = ttk.Entry(input_frame, width=5)
    entry_r.grid(row=1, column=1, padx=5, pady=5, sticky='W')

    # Variables de selección
    comb_tipo = tk.IntVar(value=1)
    perm_tipo = tk.IntVar(value=1)

    # Opciones de combinaciones
    comb_frame = ttk.Frame(discreta_window, padding=10, borderwidth=2, relief="groove")
    comb_frame.pack(pady=10, padx=10, fill='x')

    label_comb = ttk.Label(comb_frame, text="Combinaciones:", style='TLabel')
    label_comb.grid(row=0, column=0, padx=5, pady=5, sticky='W')

    radio_comb_sin_rep = ttk.Radiobutton(comb_frame, text="Sin repetición", variable=comb_tipo, value=1)
    radio_comb_sin_rep.grid(row=0, column=1, padx=5, pady=5, sticky='W')

    radio_comb_con_rep = ttk.Radiobutton(comb_frame, text="Con repetición", variable=comb_tipo, value=2)
    radio_comb_con_rep.grid(row=0, column=2, padx=5, pady=5, sticky='W')

    button_comb = ttk.Button(comb_frame, text="Calcular Combinaciones", command=calcular_combinaciones)
    button_comb.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Opciones de permutaciones
    perm_frame = ttk.Frame(discreta_window, padding=10, borderwidth=2, relief="groove")
    perm_frame.pack(pady=10, padx=10, fill='x')

    label_perm = ttk.Label(perm_frame, text="Permutaciones:", style='TLabel')
    label_perm.grid(row=0, column=0, padx=5, pady=5, sticky='W')

    radio_perm_sin_rep = ttk.Radiobutton(perm_frame, text="Sin repetición", variable=perm_tipo, value=1)
    radio_perm_sin_rep.grid(row=0, column=1, padx=5, pady=5, sticky='W')

    radio_perm_con_rep = ttk.Radiobutton(perm_frame, text="Con repetición", variable=perm_tipo, value=2)
    radio_perm_con_rep.grid(row=0, column=2, padx=5, pady=5, sticky='W')

    button_perm = ttk.Button(perm_frame, text="Calcular Permutaciones", command=calcular_permutaciones)
    button_perm.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Resultado
    result_frame = ttk.Frame(discreta_window, padding=10, borderwidth=2, relief="groove")
    result_frame.pack(pady=10, padx=10, fill='both', expand=True)

    result_label = ttk.Label(result_frame, text="Resultados:", style='Header.TLabel')
    result_label.pack(anchor='w')

    result_text = tk.Text(result_frame, height=10, wrap='word', bg="#44475a", fg="white", font=('Helvetica', 18), borderwidth=2)
    result_text.pack(fill='both', expand=True)

# Función para iniciar la calculadora de Álgebra Lineal
def algebra_lineal():
    algebra_window = tk.Toplevel()
    calculator = MatrixCalculator(algebra_window)

# Función para Algoritmos (por implementar)
def algoritmos():
    messagebox.showinfo("Algoritmos", "Aquí irá el código de Algoritmos")

# Crear la ventana principal
root = tk.Tk()
root.title("Menú de Temas")
root.geometry("600x400")

root.configure(bg="#2C3E50")

# Estilo de la etiqueta de título
titulo_estilo = {
        "font": ("Helvetica", 24, "bold"),
        "bg": "#2C3E50",
        "fg": "#ECF0F1"  # Color de texto claro para contrastar el fondo oscuro
    }

label_titulo = tk.Label(root, text="Selecciona una Calculadora", **titulo_estilo)
label_titulo.pack(pady=20)

btn_algebra = tk.Button(root, text="Álgebra Lineal", command=algebra_lineal, width=30, height=2,)
btn_matematica = tk.Button(root, text="Matemática Discreta", command=matematica_discreta, width=30, height=2)
btn_algoritmos = tk.Button(root, text="Algoritmos", command=algoritmos, width=30, height=2)


btn_algebra.pack(pady=20)
btn_matematica.pack(pady=20)
btn_algoritmos.pack(pady=20)

root.mainloop()