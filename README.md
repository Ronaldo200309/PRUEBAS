import math
import tkinter as tk
from tkinter import messagebox

# Funciones para cálculos
def factorial(n):
    return math.factorial(n)

def combinaciones(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def combinaciones_con_repeticion(n, r):
    return factorial(n + r - 1) // (factorial(r) * factorial(n - 1))

def permutaciones(n, r):
    return factorial(n) // factorial(n - r)

def permutaciones_con_repeticion(n, r):
    return n ** r

# Función para manejar el cálculo
def calcular():
    n = int(entry_n.get())
    r = int(entry_r.get())
    
    if var_tipo_calculo.get() == "Combinaciones":
        if var_tipo.get() == "Sin repetición":
            if n >= r:
                resultado = combinaciones(n, r)
            else:
                messagebox.showerror("Error", "n debe ser mayor o igual a r.")
                return
        else:
            resultado = combinaciones_con_repeticion(n, r)
    
    elif var_tipo_calculo.get() == "Permutaciones":
        if var_tipo.get() == "Sin repetición":
            if n >= r:
                resultado = permutaciones(n, r)
            else:
                messagebox.showerror("Error", "n debe ser mayor o igual a r.")
                return
        else:
            resultado = permutaciones_con_repeticion(n, r)
    
    label_resultado.config(text=f"Resultado: {resultado}")

# Función para mostrar el menú de selección de tipo de cálculo (combinaciones o permutaciones)
def menu_tipo_calculo():
    menu_inicial.pack_forget()  # Ocultar menú inicial
    menu_tipo.pack()  # Mostrar menú de tipo de cálculo

# Función para mostrar el menú para elegir si es con o sin repetición
def menu_repeticion():
    menu_tipo.pack_forget()  # Ocultar el menú de tipo de cálculo
    menu_repetir.pack()  # Mostrar menú de repetición

# Función para mostrar el menú de entrada de valores de n y r
def menu_entrar_valores():
    menu_repetir.pack_forget()  # Ocultar el menú de repetición
    menu_valores.pack()  # Mostrar menú para ingresar valores

# Ventana principal
root = tk.Tk()
root.title("Calculadora de Combinaciones y Permutaciones")

# Menu inicial
menu_inicial = tk.Frame(root)
label_bienvenida = tk.Label(menu_inicial, text="Bienvenido a la Calculadora", font=("Arial", 16))
label_bienvenida.pack(pady=10)

boton_iniciar = tk.Button(menu_inicial, text="Iniciar", command=menu_tipo_calculo)
boton_iniciar.pack(pady=10)

menu_inicial.pack()

# Menú para elegir tipo de cálculo (combinaciones o permutaciones)
menu_tipo = tk.Frame(root)
label_tipo = tk.Label(menu_tipo, text="Elige el tipo de cálculo", font=("Arial", 14))
label_tipo.pack(pady=10)

var_tipo_calculo = tk.StringVar(value="Combinaciones")
radio_combinaciones = tk.Radiobutton(menu_tipo, text="Combinaciones", variable=var_tipo_calculo, value="Combinaciones")
radio_combinaciones.pack(pady=5)

radio_permutaciones = tk.Radiobutton(menu_tipo, text="Permutaciones", variable=var_tipo_calculo, value="Permutaciones")
radio_permutaciones.pack(pady=5)

boton_siguiente_tipo = tk.Button(menu_tipo, text="Siguiente", command=menu_repeticion)
boton_siguiente_tipo.pack(pady=10)

# Menú para elegir si es con o sin repetición
menu_repetir = tk.Frame(root)
label_repeticion = tk.Label(menu_repetir, text="¿Con o sin repetición?", font=("Arial", 14))
label_repeticion.pack(pady=10)

var_tipo = tk.StringVar(value="Sin repetición")
radio_sin_repeticion = tk.Radiobutton(menu_repetir, text="Sin repetición", variable=var_tipo, value="Sin repetición")
radio_sin_repeticion.pack(pady=5)

radio_con_repeticion = tk.Radiobutton(menu_repetir, text="Con repetición", variable=var_tipo, value="Con repetición")
radio_con_repeticion.pack(pady=5)

boton_siguiente_repeticion = tk.Button(menu_repetir, text="Siguiente", command=menu_entrar_valores)
boton_siguiente_repeticion.pack(pady=10)

# Menú para ingresar los valores de n y r
menu_valores = tk.Frame(root)
label_n = tk.Label(menu_valores, text="Introduce el valor de n:")
label_n.pack(pady=5)

entry_n = tk.Entry(menu_valores)
entry_n.pack()

label_r = tk.Label(menu_valores, text="Introduce el valor de r:")
label_r.pack(pady=5)

entry_r = tk.Entry(menu_valores)
entry_r.pack()

boton_calcular = tk.Button(menu_valores, text="Calcular", command=calcular)
boton_calcular.pack(pady=10)

# Etiqueta para mostrar el resultado
label_resultado = tk.Label(menu_valores, text="Resultado:")
label_resultado.pack(pady=10)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
