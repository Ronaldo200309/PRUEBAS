import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk

class MatrixCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora de Matrices")
        master.geometry("450x700")  # Tamaño de la ventana

        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        # Selección de Dimensión
        self.label_dimension = ttk.Label(master, text="Seleccionar Dimensión de Matriz:")
        self.label_dimension.pack(pady=5)

        self.dimension_var = tk.IntVar(value=2)
        self.dimensions = [2, 3, 4]
        self.dimension_menu = ttk.Combobox(master, textvariable=self.dimension_var, values=self.dimensions, state='readonly')
        self.dimension_menu.pack(pady=5)
        self.dimension_menu.bind("<<ComboboxSelected>>", self.generar_campos)  # Generar campos al seleccionar

        self.frame_matrices = tk.Frame(master)
        self.frame_matrices.pack(pady=10)

        # Método de resolución
        self.label_method = ttk.Label(master, text="Seleccionar Método (solo para sistemas):")
        self.label_method.pack(pady=5)

        self.method_var = tk.StringVar(value="Gauss-Jordan")
        self.method_menu = ttk.Combobox(master, textvariable=self.method_var, values=["Gauss-Jordan", "Regla de Cramer"], state='readonly')
        self.method_menu.pack(pady=5)

        self.button_restart = ttk.Button(master, text="Reiniciar Cálculo", command=self.reiniciar)
        self.button_restart.pack(pady=10)

        # Botones de Operaciones
        self.frame_buttons = tk.Frame(master)
        self.frame_buttons.pack(pady=10)

        self.button_inversa = ttk.Button(self.frame_buttons, text="Calcular Inversa", command=self.calcular_inversa)
        self.button_inversa.grid(row=0, column=0, padx=5)

        self.button_multiplicar = ttk.Button(self.frame_buttons, text="Multiplicar Matrices", command=self.multiplicar_matrices)
        self.button_multiplicar.grid(row=0, column=1, padx=5)

        self.button_resolver = ttk.Button(self.frame_buttons, text="Resolver Sistema", command=self.resolver_sistema)
        self.button_resolver.grid(row=0, column=2, padx=5)

        self.button_graficar = ttk.Button(self.frame_buttons, text="Graficar Ecuaciones", command=self.graficar_ecuaciones)
        self.button_graficar.grid(row=0, column=3, padx=5)

        self.campos_matriz_a = []
        self.campos_matriz_b = []

        self.generar_campos()  # Generar campos iniciales

    def generar_campos(self, event=None):
        # Limpiar campos existentes
        for widget in self.frame_matrices.winfo_children():
            widget.destroy()

        dim = self.dimension_var.get()

        # Crear campos para matriz A
        tk.Label(self.frame_matrices, text="Matriz A:").pack()
        for i in range(dim):
            fila = []
            frame_fila = tk.Frame(self.frame_matrices)
            frame_fila.pack(pady=2)
            for j in range(dim):
                campo = tk.Entry(frame_fila, width=5)
                campo.pack(side=tk.LEFT, padx=2)
                fila.append(campo)
            self.campos_matriz_a.append(fila)

        # Crear campos para matriz B (solo para sistemas)
        tk.Label(self.frame_matrices, text="Matriz B:").pack()
        for i in range(dim):
            campo = tk.Entry(self.frame_matrices, width=5)
            campo.pack(pady=2)
            self.campos_matriz_b.append(campo)

    def multiplicar_matrices(self):
        try:
            dim_a = self.dimension_var.get()
            dim_b = dim_a  # Para simplificar, asumimos que multiplicamos matrices del mismo tamaño

            # Habilitar campos para la segunda matriz
            self.campos_matriz_b.clear()
            for widget in self.frame_matrices.winfo_children():
                widget.destroy()

            self.generar_campos()  # Generar campos para la matriz A
            tk.Label(self.frame_matrices, text="Matriz B:").pack()
            for i in range(dim_b):
                fila = []
                frame_fila = tk.Frame(self.frame_matrices)
                frame_fila.pack(pady=2)
                for j in range(dim_b):
                    campo = tk.Entry(frame_fila, width=5)
                    campo.pack(side=tk.LEFT, padx=2)
                    fila.append(campo)
                self.campos_matriz_b.append(fila)

            # Procesar matrices
            matrix_a = np.zeros((dim_a, dim_a))
            matrix_b = np.zeros((dim_b, dim_b))

            for i in range(dim_a):
                for j in range(dim_a):
                    valor_a = self.campos_matriz_a[i][j].get()
                    matrix_a[i, j] = float(valor_a)

            for i in range(dim_b):
                for j in range(dim_b):
                    valor_b = self.campos_matriz_b[i][j].get()
                    matrix_b[i, j] = float(valor_b)

            producto = np.dot(matrix_a, matrix_b)
            messagebox.showinfo("Producto", f"El producto es:\n{producto}")

    def calcular_inversa(self):
        try:
            dim = self.dimension_var.get()
            matrix = np.zeros((dim, dim))

            for i in range(dim):
                for j in range(dim):
                    valor = self.campos_matriz_a[i][j].get()
                    matrix[i, j] = float(valor)

            inversa = np.linalg.inv(matrix)
            messagebox.showinfo("Inversa", f"La inversa es:\n{inversa}")
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "La matriz no es invertible.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def resolver_sistema(self):
        try:
            dim = self.dimension_var.get()
            a = np.zeros((dim, dim))
            b = np.zeros(dim)

            for i in range(dim):
                for j in range(dim):
                    valor = self.campos_matriz_a[i][j].get()
                    a[i, j] = float(valor)
                b[i] = float(self.campos_matriz_b[i].get())

            if self.method_var.get() == "Gauss-Jordan":
                self.gaus_jordan(a, b)
            else:
                self.regla_de_cramer(a, b)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gaus_jordan(self, a, b):
        try:
            a = np.hstack([a, b.reshape(-1, 1)])  # Concatenar b a A
            n = len(b)

            for i in range(n):
                a[i] = a[i] / a[i, i]
                for j in range(n):
                    if i != j:
                        a[j] = a[j] - a[i] * a[j, i]

            soluciones = a[:, -1]
            messagebox.showinfo("Soluciones", f"Las soluciones son:\n{soluciones}")
            self.verificar_soluciones(a)
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "El sistema no tiene solución o tiene infinitas soluciones.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def regla_de_cramer(self, a, b):
        try:
            det_a = np.linalg.det(a)
            if det_a == 0:
                messagebox.showinfo("Resultado", "El sistema no tiene solución única.")
                return

            n = len(b)
            soluciones = np.zeros(n)

            for i in range(n):
                temp_matrix = a.copy()
                temp_matrix[:, i] = b
                soluciones[i] = np.linalg.det(temp_matrix) / det_a

            messagebox.showinfo("Soluciones", f"Las soluciones son:\n{soluciones}")
            self.verificar_soluciones(a)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def verificar_soluciones(self, a):
        rank_a = np.linalg.matrix_rank(a[:, :-1])
        rank_augmented = np.linalg.matrix_rank(a)
        if rank_a < rank_augmented:
            messagebox.showinfo("Resultado", "El sistema tiene infinitas soluciones.")
        elif rank_a == rank_augmented:
            messagebox.showinfo("Resultado", "El sistema tiene solución única.")
        else:
            messagebox.showinfo("Resultado", "El sistema no tiene solución.")

    def graficar_ecuaciones(self):
        try:
            dim = self.dimension_var.get()
            a = np.array([[float(self.campos_matriz_a[i][j].get()) for j in range(dim)] for i in range(dim)])
            b = np.array([float(self.campos_matriz_b[i].get()) for i in range(dim)])

            if dim == 2:  # Para 2x2
                x = np.linspace(-10, 10, 200)
                y1 = (b[0] - a[0, 0] * x) / a[0, 1]
                y2 = (b[1] - a[1, 0] * x) / a[1, 1]

                plt.plot(x, y1, label='Ecuación 1')
                plt.plot(x, y2, label='Ecuación 2')
                plt.axhline(0, color='black', lw=0.5, ls='--')
                plt.axvline(0, color='black', lw=0.5, ls='--')
                plt.title("Gráfica de Ecuaciones 2x2")
                plt.legend()
                plt.grid()
                plt.show()

            elif dim == 3:  # Para 3x3
                x = np.linspace(-10, 10, 20)
                y = np.linspace(-10, 10, 20)
                X, Y = np.meshgrid(x, y)

                Z1 = (b[0] - a[0, 0] * X - a[0, 1] * Y) / a[0, 2]
                Z2 = (b[1] - a[1, 0] * X - a[1, 1] * Y) / a[1, 2]
                Z3 = (b[2] - a[2, 0] * X - a[2, 1] * Y) / a[2, 2]

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(X, Y, Z1, alpha=0.5)
                ax.plot_surface(X, Y, Z2, alpha=0.5)
                ax.plot_surface(X, Y, Z3, alpha=0.5)
                ax.set_title("Gráfica de Planos 3x3")
                plt.show()

            elif dim == 4:  # Para 4x4
                messagebox.showinfo("Graficar", "Para 4x4, la visualización es complicada y no se implementa en esta versión.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reiniciar(self):
        # Limpiar todos los campos
        for widget in self.frame_matrices.winfo_children():
            widget.destroy()

        self.campos_matriz_a = []
        self.campos_matriz_b = []
        self.generar_campos()  # Regenerar campos según la dimensión seleccionada

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculator(root)
    root.mainloop()
