import tkinter as tk
from tkinter import ttk
import psutil
import signal #importamos la libreria signal

def actualizar_procesos():
    for row in tree.get_children():
        tree.delete(row)

    proceso = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
            proceso.append((proc.info['cpu_percent'], proc.info))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    for _, info in sorted(proceso, key=lambda x: x[0], reverse=True):
        tree.insert("", "end", values=(info['pid'], info['name'], info['username'], info['cpu_percent'], info['memory_info'].rss // (1024 * 1024), info['status']))
    admin.after(1500, actualizar_procesos)

def buscar_proceso():
    query = search_var.get().strip()
    for row in tree.get_children():
        tree.delete(row)

    for proc in psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
            if query and str(proc.info['pid']) != query and query.lower() not in proc.info['name'].lower():
                continue
            tree.insert("", "end", values=(proc.info['pid'], proc.info['name'], proc.info['username'], proc.info['cpu_percent'], proc.info['memory_info'].rss // (1024 * 1024), proc.info['status']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def matar_proceso():
    selected_item = tree.selection()
    if selected_item:
        pid = tree.item(selected_item)['values'][0]
        try:
            proceso = psutil.Process(pid)
            proceso.send_signal(signal.SIGTERM) #terminar proceso correctamente en linux
            actualizar_procesos()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except PermissionError:
            tk.messagebox.showerror("Error", "No tienes permisos para terminar este proceso.")

def suspender_proceso():
    selected_item = tree.selection()
    if selected_item:
        pid = tree.item(selected_item)['values'][0]
        try:
            proceso = psutil.Process(pid)
            proceso.suspend()
            actualizar_procesos()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except PermissionError:
            tk.messagebox.showerror("Error", "No tienes permisos para suspender este proceso.")

def resumen_proceso():
    selected_item = tree.selection()
    if selected_item:
        pid = tree.item(selected_item)['values'][0]
        try:
            proceso = psutil.Process(pid)
            proceso.resume()
            actualizar_procesos()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except PermissionError:
            tk.messagebox.showerror("Error", "No tienes permisos para reanudar este proceso.")

admin = tk.Tk()
admin.title("Administrador de procesos")
admin.geometry("1280x1080")
admin.resizable(False, False)

tree = ttk.Treeview(admin, columns=("PID", "Nombre", "Usuario", "CPU (%)", "Memoria (MB)", "Estado"), show="headings")
for col in ("PID", "Nombre", "Usuario", "CPU (%)", "Memoria (MB)", "Estado"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(expand=True, fill="both")

search_var = tk.StringVar()
search_entry = ttk.Entry(admin, textvariable=search_var)
search_entry.pack()
search_button = ttk.Button(admin, text="Buscar", command=buscar_proceso)
search_button.pack()

boton = tk.Frame(admin)
boton.pack()

kill_button = tk.Button(boton, text="Finalizar", command=matar_proceso)
suspend_button = tk.Button(boton, text="Suspender", command=suspender_proceso)
resume_button = tk.Button(boton, text="Reanudar", command=resumen_proceso)

kill_button.pack(side="left")
suspend_button.pack(side="left")
resume_button.pack(side="left")

actualizar_procesos()
admin.mainloop()