import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# Función para crear la ventana de presentación
def ventana_presentacion():
    ventana = tk.Tk()
    ventana.title("Proyecto Final")
    ventana.geometry("1200x600")  
    ventana.configure(bg="#e0f7fa")

    presentacion_label = tk.Label(ventana, text="Proyecto Final de Álgebra Lineal", font=("Arial", 20), bg="#e0f7fa")
    presentacion_label.pack(pady=50)

    # Botón para ir a la ventana principal
    continuar_button = tk.Button(ventana, text="Algebra Lineal", command=lambda: [ventana.destroy(), ventana_principal()], bg="#4db6ac", fg="white", font=("Arial", 16))
    continuar_button.pack(pady=20)

    ventana.mainloop()

# Función para crear la ventana principal
def ventana_principal():
    ventana = tk.Tk()
    ventana.title("Aplicación de Álgebra Lineal")
    ventana.geometry("1200x600")  # Aumentar el tamaño de la ventana
    ventana.configure(bg="#e0f7fa")

    bienvenida_label = tk.Label(ventana, text="Bienvenido a la Aplicación de Álgebra Lineal", font=("Arial", 20), bg="#e0f7fa")
    bienvenida_label.pack(pady=20)

    multiplicar_button = tk.Button(ventana, text="Multiplicar Matrices", command=lambda: ventana_multiplicar(ventana), bg="#4db6ac", fg="white", font=("Arial", 16))
    multiplicar_button.pack(pady=10)

    inversa_button = tk.Button(ventana, text="Encontrar Inversa de Matriz", command=lambda: ventana_inversa(ventana), bg="#4db6ac", fg="white", font=("Arial", 16))
    inversa_button.pack(pady=10)

    # Añadir el botón para la nueva funcionalidad de resolver sistemas de ecuaciones lineales
    ecuaciones_button = tk.Button(ventana, text="Resolver Sistemas de Ecuaciones Lineales", command=lambda: ventana_ecuaciones_lineales(ventana), bg="#4db6ac", fg="white", font=("Arial", 16))
    ecuaciones_button.pack(pady=10)

    ventana.mainloop()

# Ventana para la opción de multiplicar matrices
def ventana_multiplicar(ventana):
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Multiplicar Matrices")
    nueva_ventana.geometry("1200x600")  # Aumentar el tamaño de la ventana
    nueva_ventana.configure(bg="#e0f7fa")

    # Frame para las instrucciones y entradas
    left_frame = tk.Frame(nueva_ventana, bg="#e0f7fa")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

    instrucciones_label = tk.Label(left_frame, text="Ingresa las dimensiones de las matrices para multiplicarlas:", font=("Arial", 14), bg="#e0f7fa")
    instrucciones_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    filas1_label = tk.Label(left_frame, text="Filas de la primera matriz:", bg="#e0f7fa", font=("Arial", 12))
    filas1_label.grid(row=1, column=0, padx=10, sticky='w')
    filas1_entry = tk.Entry(left_frame, font=("Arial", 12))
    filas1_entry.grid(row=1, column=1)

    columnas1_label = tk.Label(left_frame, text="Columnas de la primera matriz:", bg="#e0f7fa", font=("Arial", 12))
    columnas1_label.grid(row=2, column=0, padx=10, sticky='w')
    columnas1_entry = tk.Entry(left_frame, font=("Arial", 12))
    columnas1_entry.grid(row=2, column=1)

    filas2_label = tk.Label(left_frame, text="Filas de la segunda matriz:", bg="#e0f7fa", font=("Arial", 12))
    filas2_label.grid(row=3, column=0, padx=10, sticky='w')
    filas2_entry = tk.Entry(left_frame, font=("Arial", 12))
    filas2_entry.grid(row=3, column=1)

    columnas2_label = tk.Label(left_frame, text="Columnas de la segunda matriz:", bg="#e0f7fa", font=("Arial", 12))
    columnas2_label.grid(row=4, column=0, padx=10, sticky='w')
    columnas2_entry = tk.Entry(left_frame, font=("Arial", 12))
    columnas2_entry.grid(row=4, column=1)

    # Título y contexto en la parte derecha
    right_frame = tk.Frame(nueva_ventana, bg="#e0f7fa")
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

    contexto_label = tk.Label(right_frame, text="Contexto sobre la Multiplicación de Matrices", font=("Arial", 16, 'bold'), bg="#e0f7fa")
    contexto_label.pack(anchor='ne', pady=(0, 5))

    contexto_text = (
        "La multiplicación de matrices es una operación que combina dos matrices para producir una tercera matriz. "
        "Esta operación es fundamental en diversas áreas como la ingeniería, la computación y la física. "
        "Para multiplicar dos matrices, el número de columnas de la primera matriz debe ser igual al número de filas "
        "de la segunda matriz. El elemento de la fila i y columna j de la matriz resultante se calcula como la "
        "suma del producto de los elementos de la fila i de la primera matriz por los elementos de la columna j de "
        "la segunda matriz."
    )

    contexto_label_d = tk.Label(right_frame, text=contexto_text, font=("Arial", 12), bg="#e0f7fa", justify="left", wraplength=400)
    contexto_label_d.pack(anchor='ne', padx=10, pady=10)

    resultado_label = tk.Label(left_frame, text="Resultado de la multiplicación:", font=("Arial", 12), bg="#e0f7fa")
    resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

    resultado_frame = tk.Frame(left_frame)
    resultado_frame.grid(row=7, column=0, columnspan=2, pady=10)

    matriz_frame = tk.Frame(left_frame)
    matriz_frame.grid(row=8, column=0, columnspan=2, pady=10)

    def crear_entradas_matrices():
        try:
            filas1 = int(filas1_entry.get())
            columnas1 = int(columnas1_entry.get())
            filas2 = int(filas2_entry.get())
            columnas2 = int(columnas2_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa números válidos.")
            return

        if columnas1 != filas2:
            messagebox.showerror("Error", "El número de columnas de la primera matriz debe coincidir con el número de filas de la segunda matriz.")
            return

        # Limpiar los marcos de la matriz y del resultado antes de generar nuevas entradas
        for widget in matriz_frame.winfo_children():
            widget.destroy()
        for widget in resultado_frame.winfo_children():
            widget.destroy()

        # Generar celdas para la primera matriz
        matriz1_entries = []
        for i in range(filas1):
            fila_entries = []
            for j in range(columnas1):
                entrada = tk.Entry(matriz_frame, width=5, font=("Arial", 12))
                entrada.grid(row=i, column=j)
                fila_entries.append(entrada)
            matriz1_entries.append(fila_entries)

        # Generar celdas para la segunda matriz
        matriz2_entries = []
        for i in range(filas2):
            fila_entries = []
            for j in range(columnas2):
                entrada = tk.Entry(matriz_frame, width=5, font=("Arial", 12))
                entrada.grid(row=i, column=j + columnas1 + 2)  # Separar la segunda matriz
                fila_entries.append(entrada)
            matriz2_entries.append(fila_entries)

        # Calcular y mostrar el resultado de la multiplicación
        def multiplicar_matrices():
            try:
                matriz1 = [[int(matriz1_entries[i][j].get()) for j in range(columnas1)] for i in range(filas1)]
                matriz2 = [[int(matriz2_entries[i][j].get()) for j in range(columnas2)] for i in range(filas2)]
                resultado = [[0] * columnas2 for _ in range(filas1)]

                for i in range(filas1):
                    for j in range(columnas2):
                        for k in range(columnas1):  # o filas2, ya que columnas1 == filas2
                            resultado[i][j] += matriz1[i][k] * matriz2[k][j]

                for i in range(filas1):
                    for j in range(columnas2):
                        entrada_resultado = tk.Label(resultado_frame, text=resultado[i][j], font=("Arial", 12))
                        entrada_resultado.grid(row=i, column=j)

            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa solo números en las matrices.")
                return

        # Botón para multiplicar las matrices
        multiplicar_button = tk.Button(left_frame, text="Multiplicar Matrices", command=multiplicar_matrices, bg="#4db6ac", fg="white", font=("Arial", 12))
        multiplicar_button.grid(row=6, column=0, columnspan=2, pady=20)

    generar_button = tk.Button(left_frame, text="Generar Entradas de Matrices", command=crear_entradas_matrices, bg="#4db6ac", fg="white", font=("Arial", 12))
    generar_button.grid(row=5, column=0, columnspan=2, pady=10)

# Ventana para la opción de encontrar la inversa de una matriz
def ventana_inversa(ventana):
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Encontrar Inversa de Matriz")
    nueva_ventana.geometry("1200x600")  # Aumentar el tamaño de la ventana
    nueva_ventana.configure(bg="#e0f7fa")

    # Frame para las instrucciones y entradas
    left_frame = tk.Frame(nueva_ventana, bg="#e0f7fa")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

    instrucciones_label = tk.Label(left_frame, text="Ingresa las dimensiones de la matriz:", font=("Arial", 14), bg="#e0f7fa")
    instrucciones_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    filas_label = tk.Label(left_frame, text="Filas de la matriz:", bg="#e0f7fa", font=("Arial", 12))
    filas_label.grid(row=1, column=0, padx=10, sticky='w')
    filas_entry = tk.Entry(left_frame, font=("Arial", 12))
    filas_entry.grid(row=1, column=1)

    columnas_label = tk.Label(left_frame, text="Columnas de la matriz:", bg="#e0f7fa", font=("Arial", 12))
    columnas_label.grid(row=2, column=0, padx=10, sticky='w')
    columnas_entry = tk.Entry(left_frame, font=("Arial", 12))
    columnas_entry.grid(row=2, column=1)

    # Título y contexto en la parte derecha
    right_frame = tk.Frame(nueva_ventana, bg="#e0f7fa")
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

    contexto_label = tk.Label(right_frame, text="Contexto sobre la Inversa de Matrices", font=("Arial", 16, 'bold'), bg="#e0f7fa")
    contexto_label.pack(anchor='ne', pady=(0, 5))

    contexto_text = (
        "La inversa de una matriz es un concepto fundamental en álgebra lineal. "
        "Si A es una matriz cuadrada, su inversa se denota como A^(-1), y se define "
        "como la matriz que, cuando se multiplica por A, produce la matriz identidad. "
        "No todas las matrices tienen inversa, y solo las matrices cuadradas que son no singulares (determinante diferente de cero) tienen inversa."
    )

    contexto_label_d = tk.Label(right_frame, text=contexto_text, font=("Arial", 12), bg="#e0f7fa", justify="left", wraplength=400)
    contexto_label_d.pack(anchor='ne', padx=10, pady=10)

    resultado_label = tk.Label(left_frame, text="Resultado de la inversa:", font=("Arial", 12), bg="#e0f7fa")
    resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

    resultado_frame = tk.Frame(left_frame)
    resultado_frame.grid(row=6, column=0, columnspan=2, pady=10)  # Cambiado de 7 a 6 para posicionar correctamente

    matriz_frame = tk.Frame(left_frame)
    matriz_frame.grid(row=7, column=0, columnspan=2, pady=10)

    def crear_entradas_matriz():
        try:
            filas = int(filas_entry.get())
            columnas = int(columnas_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa números válidos.")
            return

        if filas != columnas:
            messagebox.showerror("Error", "La matriz debe ser cuadrada (igual número de filas y columnas).")
            return

        # Limpiar el marco de la matriz y del resultado antes de generar nuevas entradas
        for widget in matriz_frame.winfo_children():
            widget.destroy()
        for widget in resultado_frame.winfo_children():
            widget.destroy()

        # Generar celdas para la matriz
        matriz_entries = []
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entrada = tk.Entry(matriz_frame, width=5, font=("Arial", 12))
                entrada.grid(row=i, column=j)
                fila_entries.append(entrada)
            matriz_entries.append(fila_entries)

        # Calcular y mostrar el resultado de la inversa
        def calcular_inversa():
            try:
                matriz = [[float(matriz_entries[i][j].get()) for j in range(columnas)] for i in range(filas)]
                inversa = calcular_inversa_matriz(matriz)

                # Mostrar el resultado
                if inversa is not None:
                    for i in range(filas):
                        for j in range(columnas):
                            entrada_resultado = tk.Label(resultado_frame, text=f"{inversa[i][j]:.2f}", font=("Arial", 12))
                            entrada_resultado.grid(row=i, column=j)
                else:
                    messagebox.showerror("Error", "La matriz no tiene inversa (determinante es cero).")

            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa solo números en la matriz.")
                return

        # Botón para calcular la inversa
        calcular_button = tk.Button(left_frame, text="Calcular Inversa", command=calcular_inversa, bg="#4db6ac", fg="white", font=("Arial", 12))
        calcular_button.grid(row=8, column=0, columnspan=2, pady=20)  # Cambiado de 6 a 8

    generar_button = tk.Button(left_frame, text="Generar Entradas de Matriz", command=crear_entradas_matriz, bg="#4db6ac", fg="white", font=("Arial", 12))
    generar_button.grid(row=4, column=0, columnspan=2, pady=20)

# Función para calcular la inversa de la matriz
def calcular_inversa_matriz(matriz):
    try:
        matriz_np = np.array(matriz)
        inversa = np.linalg.inv(matriz_np)
        return inversa.tolist()
    except np.linalg.LinAlgError:
        return None  # La matriz no tiene inversa

# Ventana para la opción de resolver sistemas de ecuaciones lineales
def ventana_ecuaciones_lineales(ventana):
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Resolver Sistemas de Ecuaciones Lineales")
    nueva_ventana.geometry("1200x600")
    nueva_ventana.configure(bg="#e0f7fa")

    # Frame para las instrucciones y entradas
    left_frame = tk.Frame(nueva_ventana, bg="#e0f7fa")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

    instrucciones_label = tk.Label(left_frame, text="Ingresa el número de ecuaciones y variables:", font=("Arial", 14), bg="#e0f7fa")
    instrucciones_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    ecuaciones_label = tk.Label(left_frame, text="Número de ecuaciones (2, 3 o 4):", bg="#e0f7fa", font=("Arial", 12))
    ecuaciones_label.grid(row=1, column=0, padx=10, sticky='w')
    ecuaciones_entry = tk.Entry(left_frame, font=("Arial", 12))
    ecuaciones_entry.grid(row=1, column=1)

    metodo_label = tk.Label(left_frame, text="Selecciona el método:", font=("Arial", 12), bg="#e0f7fa")
    metodo_label.grid(row=2, column=0, padx=10, pady=(10, 10))
    
    metodo_var = tk.StringVar(value="Gauss-Jordan")
    gauss_jordan_radiobutton = tk.Radiobutton(left_frame, text="Gauss-Jordan", variable=metodo_var, value="Gauss-Jordan", bg="#e0f7fa", font=("Arial", 12))
    cramer_radiobutton = tk.Radiobutton(left_frame, text="Regla de Cramer", variable=metodo_var, value="Cramer", bg="#e0f7fa", font=("Arial", 12))
    
    gauss_jordan_radiobutton.grid(row=3, column=0, sticky='w')
    cramer_radiobutton.grid(row=3, column=1, sticky='w')

    resultado_label = tk.Label(left_frame, text="Resultado del sistema:", font=("Arial", 12), bg="#e0f7fa")
    resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

    resultado_frame = tk.Frame(left_frame)
    resultado_frame.grid(row=7, column=0, columnspan=2, pady=10)

    matriz_frame = tk.Frame(left_frame)
    matriz_frame.grid(row=8, column=0, columnspan=2, pady=10)

    # Título y contexto en la parte derecha
    right_frame = tk.Frame(nueva_ventana, bg="#e0f7fa")
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

    contexto_label = tk.Label(right_frame, text="Contexto sobre la Inversa de Matrices", font=("Arial", 16, 'bold'), bg="#e0f7fa")
    contexto_label.pack(anchor='ne', pady=(0, 5))

    contexto_text = (
        """
        La resolución de sistemas de ecuaciones lineales incluye abordar sistemas de distintas dimensiones, como 2x2, 3x3 y 4x4. 
        En un sistema 2x2, se resuelven dos ecuaciones con dos incógnitas, mientras que en un 3x3 se trabajan tres ecuaciones con tres variables, 
        y en un 4x4, cuatro ecuaciones con cuatro incógnitas. Se pueden emplear métodos como Gauss-Jordan, 
        que transforma el sistema a una forma escalonada reducida, o la regla de Cramer, que utiliza determinantes para sistemas cuadrados. 
        Al resolver, pueden surgir tres situaciones: soluciones únicas (donde las ecuaciones se intersecan en un único punto), 
        sin solución (cuando las ecuaciones representan líneas o planos paralelos) o soluciones infinitas (cuando las ecuaciones son dependientes y representan la misma línea o plano). 
        """

    )

    contexto_label_d = tk.Label(right_frame, text=contexto_text, font=("Arial", 12), bg="#e0f7fa", justify="left", wraplength=400)
    contexto_label_d.pack(anchor='ne', padx=10, pady=10)

    def crear_entradas_sistema():
        try:
            num_ecuaciones = int(ecuaciones_entry.get())
            if num_ecuaciones not in [2, 3, 4]:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido de ecuaciones (2, 3 o 4).")
            return

        # Limpiar los marcos de la matriz y del resultado antes de generar nuevas entradas
        for widget in matriz_frame.winfo_children():
            widget.destroy()
        for widget in resultado_frame.winfo_children():
            widget.destroy()

        # Generar celdas para los coeficientes de las ecuaciones
        coeficientes_entries = []
        terminos_independientes_entries = []

        for i in range(num_ecuaciones):
            fila_entries = []
            for j in range(num_ecuaciones):
                entrada = tk.Entry(matriz_frame, width=5, font=("Arial", 12))
                entrada.grid(row=i, column=j)
                fila_entries.append(entrada)
            coeficientes_entries.append(fila_entries)

            # Generar entradas para los términos independientes
            entrada_termino_independiente = tk.Entry(matriz_frame, width=5, font=("Arial", 12))
            entrada_termino_independiente.grid(row=i, column=num_ecuaciones + 1)  # Separar por una columna
            terminos_independientes_entries.append(entrada_termino_independiente)

        # Calcular y mostrar el resultado del sistema
        def resolver_sistema():
            try:
                coeficientes = [[float(coeficientes_entries[i][j].get()) for j in range(num_ecuaciones)] for i in range(num_ecuaciones)]
                terminos_independientes = [float(terminos_independientes_entries[i].get()) for i in range(num_ecuaciones)]
                metodo = metodo_var.get()

                if metodo == "Gauss-Jordan":
                    soluciones, mensaje = resolver_por_gauss_jordan(coeficientes, terminos_independientes)
                else:
                    soluciones, mensaje = resolver_por_cramer(coeficientes, terminos_independientes)

                # Mostrar el resultado
                if soluciones is None:
                    resultado_label = tk.Label(resultado_frame, text=mensaje, font=("Arial", 12))
                    resultado_label.grid(row=0, column=0)
                else:
                    for i in range(num_ecuaciones):
                        entrada_resultado = tk.Label(resultado_frame, text=f"x{i+1} = {soluciones[i]:.2f}", font=("Arial", 12))
                        entrada_resultado.grid(row=i, column=0)
                    mensaje_label = tk.Label(resultado_frame, text=mensaje, font=("Arial", 12))
                    mensaje_label.grid(row=num_ecuaciones, column=0)

                    # Llamar a la funcion para graficar
                    graficar_ecuaciones(coeficientes, terminos_independientes)

            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa solo números en las matrices.")
                return

        # Botón para resolver el sistema
        resolver_button = tk.Button(left_frame, text="Resolver Sistema", command=resolver_sistema, bg="#4db6ac", fg="white", font=("Arial", 12))
        resolver_button.grid(row=6, column=0, columnspan=2, pady=20)

    generar_button = tk.Button(left_frame, text="Generar Entradas del Sistema", command=crear_entradas_sistema, bg="#4db6ac", fg="white", font=("Arial", 12))
    generar_button.grid(row=4, column=0, columnspan=2, pady=20)

# Función para graficar las ecuaciones
def graficar_ecuaciones(coeficientes, terminos_independientes):
    # Crear un rango de valores para x
    x_vals = np.linspace(-10, 10, 400)  # Ajusta el rango según sea necesario

    # Graficar cada ecuación
    for i in range(len(coeficientes)):
        # Obteniendo los coeficientes de la ecuación
        a, b = coeficientes[i]
        c = terminos_independientes[i]

        # Calcular los valores de y
        y_vals = (c - a * x_vals) / b  # y = (c - ax) / b
        
        # Graficar la recta
        plt.plot(x_vals, y_vals, label=f'Ecuación {i + 1}')

    plt.axhline(0, color='black', lw=0.5)  # Línea horizontal en y=0
    plt.axvline(0, color='black', lw=0.5)  # Línea vertical en x=0
    plt.xlim(-10, 10)  # Establece límites en x
    plt.ylim(-10, 10)  # Establece límites en y
    plt.grid(color='gray', linestyle='--', linewidth=0.5)  # Grilla
    plt.legend()  # Muestra la leyenda
    plt.title('Gráficas de las Ecuaciones')  # Título de la gráfica
    plt.xlabel('x')  # Etiqueta del eje x
    plt.ylabel('y')  # Etiqueta del eje y
    plt.show()  # Muestra la gráfica

# Función para resolver el sistema de ecuaciones por Gauss-Jordan
def resolver_por_gauss_jordan(coeficientes, terminos_independientes):
    matriz = np.column_stack((coeficientes, terminos_independientes))
    try:
        soluciones = np.linalg.solve(coeficientes, terminos_independientes)
        return soluciones, "Solución única"
    except np.linalg.LinAlgError as e:
        rango_a = np.linalg.matrix_rank(coeficientes)
        rango_aumentada = np.linalg.matrix_rank(matriz)

        if rango_a != rango_aumentada:
            return None, "El sistema no tiene solución"
        elif rango_a == rango_aumentada and rango_a < len(coeficientes):
            return None, "El sistema tiene soluciones infinitas"

# Función para resolver el sistema de ecuaciones por la regla de Cramer
def resolver_por_cramer(coeficientes, terminos_independientes):
    det_a = np.linalg.det(coeficientes)
    if det_a == 0:
        return None, "El sistema no tiene solución o tiene soluciones infinitas"
    else:
        soluciones = []
        for i in range(len(coeficientes)):
            matriz_temp = np.copy(coeficientes)
            matriz_temp[:, i] = terminos_independientes
            soluciones.append(np.linalg.det(matriz_temp) / det_a)
        return soluciones, "Solución única"
    
# Función para graficar las ecuaciones
def graficar_ecuaciones(coeficientes, terminos_independientes):
    x_vals = np.linspace(-10, 10, 400)  # Rango de valores para x
    plt.figure(figsize=(10, 6))

    for i in range(len(coeficientes)):
        # Obtener coeficientes de la ecuación
        a = coeficientes[i]
        b = terminos_independientes[i]

        # Calculamos la pendiente y la intersección
        if len(a) == 2:  # Solo dos coeficientes, es una línea
            m = -a[0] / a[1]  # Pendiente
            b = b / a[1]  # Intersección
            y_vals = m * x_vals + b
            plt.plot(x_vals, y_vals, label=f'Ecuación {i+1}: {a[0]}x + {a[1]}y = {terminos_independientes[i]}')
        elif len(a) == 3:  # Tres coeficientes, plano (solo graficamos si hay más de 2 ecuaciones)
            # Aquí solo graficamos si hay exactamente dos ecuaciones para evitar problemas de dimensión
            if len(coeficientes) == 2:
                x_vals_2d = np.linspace(-10, 10, 400)
                y_vals_1 = (b[0] - a[0] * x_vals_2d) / a[1]
                y_vals_2 = (b[1] - coeficientes[1][0] * x_vals_2d) / coeficientes[1][1]
                plt.plot(x_vals_2d, y_vals_1, label=f'Ecuación 1')
                plt.plot(x_vals_2d, y_vals_2, label=f'Ecuación 2')

    plt.axhline(0, color='black',linewidth=0.5, ls='--')
    plt.axvline(0, color='black',linewidth=0.5, ls='--')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.title('Gráfica de las Ecuaciones')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.show()

ventana_presentacion()
