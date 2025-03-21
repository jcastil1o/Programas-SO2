"""
Este archivo contiene algoritmos relacionados con la gestión de memoria
en sistemas operativos. Aquí se implementarán diferentes técnicas
como paginación, segmentación, y otros métodos de administración de memoria.

1. objetivo de crear una pantalla de ingreso de datos como tamaño de bloques, procesos
1.1 presentación gráfica de memoria y procesos, mostrar los bloques disponibles.
2. comparación de rendimiento de algoritmos de asignación de memoria
3. descarga de pdf de los resultados
"""

#librerias de pantallas
import tkinter as tk
import time
from time import sleep
#funciones de memorias
def primer_ajuste(bloques, procesos):
    asignacion = [-1] * len(procesos)
    for i, proceso in enumerate(procesos):
        for j, bloque in enumerate(bloques):
            if bloque >= proceso:
                asignacion[i] = j
                bloques[j] -= proceso
                break
    return asignacion

def mejor_ajuste(bloques, procesos):
    asignacion = [-1] * len (procesos)
    for i, proceso in enumerate(procesos):
        mejor_indice = -1
        mejor_tamano = float('inf')
        for j, bloque in enumerate(bloques):
            if bloque >= proceso and bloque < mejor_tamano:
                mejor_indice = j
                mejor_tamano = bloque
        
        if mejor_indice != -1:
            asignacion[i] = mejor_indice
            bloques[mejor_indice] -= proceso
    return asignacion

def peor_ajuste(bloques, procesos):
    asignacion = [-1] * len(procesos)
    for i, proceso in enumerate(procesos):
        peor_indice = -1
        peor_tamano = -1
        for j, bloque in enumerate(bloques):
            if bloque >= proceso and bloque > peor_tamano:
                peor_indice = j
                peor_tamano = bloque
        
        if peor_indice != -1:
            asignacion[i] = peor_indice
            bloques[peor_indice] -= proceso
    return asignacion

def siguiente_ajuste(bloques, procesos):
    asignacion = [-1] * len(procesos)
    siguiente_indice = 0
    for i, proceso in enumerate(procesos):
        j = siguiente_indice
        while True:
            if bloques[j] >= proceso:
                asignacion[i] = j
                bloques[j] -= proceso
                siguiente_indice = j
                break
            j = (j + 1) % len(bloques)
            if j == siguiente_indice:
                break
    return asignacion

def mostrar_asignacion (asignacion):
    for i, asignado in enumerate(asignacion):
        if asignado != -1:
            print(f"Proceso {i+1} asignado al bloque {asignado+1}")
        else:
            print(f"Proceso {i+1} no pudo ser asignado")

def mostrar_resultados(bloques, procesos, asignacion):
    print("Bloques de memoria:", bloques)
    print("Procesos:", procesos)
    print("Asignación de procesos:", asignacion)

def comparar (bloques, procesos):
    print("\nPrimer ajuste:")
    bloques_copia = bloques[:]
    a_primer = primer_ajuste(bloques_copia, procesos)
    mostrar_asignacion(a_primer)
    time.sleep(3)
    print("\nMejor ajuste:")
    bloques_copia = bloques[:] 
    a_mejor = mejor_ajuste(bloques_copia, procesos)
    mostrar_asignacion(a_mejor)
    time.sleep(3)
    print("\nPeor ajuste:")
    bloques_copia = bloques[:]
    a_peor = peor_ajuste(bloques_copia, procesos)
    mostrar_asignacion(a_peor)
    time.sleep(3)
    print("\nSiguiente ajuste:")
    bloques_copia = bloques[:]
    a_siguiente = siguiente_ajuste(bloques_copia, procesos)
    mostrar_asignacion(a_siguiente)

bloques = list(map(int, input("Ingrese los tamaños de los bloques de memoria: (separados por espacios) ").split()))
time.sleep(1)
procesos = list(map(int, input("Ingrese los tamaños de cada proceso: (separados por espacios) ").split()))
time.sleep(1)

comparar(bloques, procesos)
time.sleep(1)