import math  # Importa el módulo math para usar la función factorial

def factorial(n):
    return math.factorial(n)

def combinaciones(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def combinaciones_con_repeticion(n, r):
    # Fórmula para combinaciones con repetición: C(n+r-1, r)
    return factorial(n + r - 1) // (factorial(r) * factorial(n - 1))

def permutaciones(n, r):
    return factorial(n) // factorial(n - r)

def permutaciones_con_repeticion(n, r):
    # Fórmula para permutaciones con repetición: n^r
    return n ** r

def menu():
    while True:
        print("\nCalculadora de Combinaciones y Permutaciones")
        print("1. Calcular Combinaciones (nCr)")
        print("2. Calcular Permutaciones (nPr)")
        print("3. Salir")
        
        opcion = input("Elige una opción (1-3): ")
        
        if opcion == '1':
            # Submenú para combinaciones
            print("\nOpciones de Combinaciones:")
            print("1. Sin repetición")
            print("2. Con repetición")
            sub_opcion = input("Elige una opción (1-2): ")
            
            n = int(input("Introduce el valor de n: "))
            r = int(input("Introduce el valor de r: "))
            
            if sub_opcion == '1':
                if n >= r:
                    print(f"Combinaciones ({n}C{r}): {combinaciones(n, r)}")
                else:
                    print("n debe ser mayor o igual a r.")
            elif sub_opcion == '2':
                print(f"Combinaciones con repetición ({n}C{r}): {combinaciones_con_repeticion(n, r)}")
            else:
                print("Opción no válida. Intenta de nuevo.")

        elif opcion == '2':
            # Submenú para permutaciones
            print("\nOpciones de Permutaciones:")
            print("1. Sin repetición")
            print("2. Con repetición")
            sub_opcion = input("Elige una opción (1-2): ")

            n = int(input("Introduce el valor de n: "))
            r = int(input("Introduce el valor de r: "))
            
            if sub_opcion == '1':
                if n >= r:
                    print(f"Permutaciones ({n}P{r}): {permutaciones(n, r)}")
                else:
                    print("n debe ser mayor o igual a r.")
            elif sub_opcion == '2':
                print(f"Permutaciones con repetición ({n}P{r}): {permutaciones_con_repeticion(n, r)}")
            else:
                print("Opción no válida. Intenta de nuevo.")

        elif opcion == '3':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

# Llama a la función menu para ejecutar el programa
menu()
