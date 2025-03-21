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
from tkinter import scrolledtext, filedialog
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

#pedir datos al usuario
def realizar_asignacion():
    bloques = list(map(int, bloques_entry.get().split()))
    procesos = list(map(int, procesos_entry.get().split()))
    
    resultados_text.delete(1.0, tk.END)

    bloques_copia = bloques[:]
    asignacion_primer_ajuste = primer_ajuste(bloques_copia, procesos)
    resultados_text.insert(tk.END, "Primer ajuste:\n")
    for i, asignado in enumerate(asignacion_primer_ajuste):
        if asignado != -1:
            resultados_text.insert(tk.END, f"Proceso {i+1} asignado al bloque {asignado+1}\n")
        else:
            resultados_text.insert(tk.END, f"Proceso {i+1} no pudo ser asignado\n")

    # mejor ajuste
    bloques_copia = bloques[:]
    asignacion_mejor_ajuste = mejor_ajuste(bloques_copia, procesos)
    resultados_text.insert(tk.END, "\nMejor ajuste:\n")
    for i, asignado in enumerate(asignacion_mejor_ajuste):
        if asignado != -1:
            resultados_text.insert(tk.END, f"Proceso {i+1} asignado al bloque {asignado+1}\n")
        else:
            resultados_text.insert(tk.END, f"Proceso {i+1} no pudo ser asignado\n")
    
    # peor ajuste
    bloques_copia = bloques[:]
    asignacion_peor_ajuste = peor_ajuste(bloques_copia, procesos)
    resultados_text.insert(tk.END, "\nPeor ajuste:\n")
    for i, asignado in enumerate(asignacion_peor_ajuste):
        if asignado != -1:
            resultados_text.insert(tk.END, f"  Proceso {i+1} asignado al bloque {asignado+1}\n")
        else:
            resultados_text.insert(tk.END, f"  Proceso {i+1} no asignado\n")
    
     # Siguiente ajuste
    bloques_copia = bloques[:]
    asignacion_siguiente_ajuste = siguiente_ajuste(bloques_copia, procesos)
    resultados_text.insert(tk.END, "\nSiguiente ajuste:\n")
    for i, asignado in enumerate(asignacion_siguiente_ajuste):
        if asignado != -1:
            resultados_text.insert(tk.END, f"  Proceso {i+1} asignado al bloque {asignado+1}\n")
        else:
            resultados_text.insert(tk.END, f"  Proceso {i+1} no asignado\n")

def generar_txt():
    contenido = resultados_text.get(1.0, tk.END)
    archivo = filedialog.asksaveasfilename(defaultextension = ".txt", filetypes = [("*.txt")])

    if archivo:
        with open(archivo, "w") as f:
            f.write(contenido)


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

"""
bloques = list(map(int, input("Ingrese los tamaños de los bloques de memoria: (separados por espacios) ").split()))
time.sleep(1)
procesos = list(map(int, input("Ingrese los tamaños de cada proceso: (separados por espacios) ").split()))
time.sleep(1)

comparar(bloques, procesos)
time.sleep(1)
"""

memoria_root = tk.Tk()
memoria_root.title("Algoritmos de asignación de memoria")

bloques_label = tk.Label(memoria_root, text="Tamaños de los bloques de memoria: (separados por espacios)")
bloques_label.pack()
bloques_entry = tk.Entry(memoria_root)
bloques_entry.pack()

procesos_label = tk.Label(memoria_root, text="Tamaños de los procesos: (separados por espacios)")
procesos_label.pack()
procesos_entry = tk.Entry(memoria_root)
procesos_entry.pack()

asignar_boton = tk.Button(memoria_root, text="Realizar asignación", command=realizar_asignacion)
asignar_boton.pack()

resultados_text = scrolledtext.ScrolledText(memoria_root, width=60, height=20)
resultados_text.pack()

guardar_boton = tk.Button(memoria_root, text="Guardar resultados en un archivo", command=generar_txt)
guardar_boton.pack()

memoria_root.mainloop()