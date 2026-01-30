import random

def lanzar_dados(cantidad,caras):
    resultados = []
    for _ in range(cantidad):
        resultados.append(random.randint(1, int(caras)))
    return resultados

if __name__ == "__main__":
    while True:
        try:
            cantidad = int(input("Ingrese el número de dados a lanzar: "))
            caras = int(input("Ingrese el número de caras del dado: "))
        except ValueError:
            print("Error: Por favor ingrese valores válidos.")

        lista_resultados = lanzar_dados(cantidad, caras)
        total = sum(lista_resultados)
        print(f"Resultados de los dados: {lista_resultados}")
        print(f"Suma total de los dados: {total}")

        continuar = input("¿Desea lanzar los dados nuevamente? (s/n): ").lower()
        if continuar != 's':
            break