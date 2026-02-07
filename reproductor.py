import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

# --- 1. CONFIGURACIÓN ---
pygame.mixer.init()
pausado = False

# DICCIONARIO CLAVE: Aquí guardaremos {"Nombre Cancion": "Ruta/Completa/Al/Archivo.mp3"}
# Así Python nunca pierde el archivo.
canciones_path = {}

def cargar_carpeta():
    # Pedimos carpeta
    ruta_carpeta = filedialog.askdirectory()
    
    if ruta_carpeta:
        # Limpiamos la lista visual y el diccionario interno
        playlist.delete(0, tk.END)
        canciones_path.clear()
        
        print(f"📂 Analizando carpeta: {ruta_carpeta}")
        
        try:
            # NO usamos os.chdir. Leemos la ruta directamente.
            archivos = os.listdir(ruta_carpeta)
            
            contador = 0
            for archivo in archivos:
                # Depuración: Ver qué ve Python exactamente
                # print(f"Visto: {archivo} (Termina en mp3?: {archivo.lower().endswith('.mp3')})")
                
                if archivo.lower().endswith(".mp3"):
                    # Guardamos la ruta COMPLETA
                    ruta_completa = os.path.join(ruta_carpeta, archivo)
                    
                    # Añadimos al diccionario y a la lista visual
                    canciones_path[archivo] = ruta_completa
                    playlist.insert(tk.END, archivo)
                    contador += 1
            
            if contador == 0:
                print("❌ La carpeta existe, pero os.listdir no ve MP3s.")
                print("Archivos encontrados en bruto:", archivos)
                messagebox.showwarning("Vacío", "No se encontraron archivos .mp3 (Revisa la terminal negra)")
            else:
                lbl_estado.config(text=f"Cargadas {contador} canciones.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la carpeta:\n{e}")

def reproducir():
    global pausado
    try:
        seleccion = playlist.curselection()
        if seleccion:
            nombre_cancion = playlist.get(seleccion[0])
            
            # RECUPERAMOS LA RUTA COMPLETA DEL DICCIONARIO
            ruta_a_reproducir = canciones_path[nombre_cancion]
            
            print(f"▶ Reproduciendo: {ruta_a_reproducir}")
            
            pygame.mixer.music.load(ruta_a_reproducir)
            pygame.mixer.music.play()
            
            lbl_estado.config(text=f"Sonando: {nombre_cancion[:30]}...")
            pausado = False
        else:
            messagebox.showinfo("Atención", "Selecciona una canción primero.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al reproducir:\n{e}")

def pausar():
    global pausado
    if pausado:
        pygame.mixer.music.unpause()
        pausado = False
        lbl_estado.config(text="Reanudado ▶")
    else:
        pygame.mixer.music.pause()
        pausado = True
        lbl_estado.config(text="Pausado ⏸")

def parar():
    pygame.mixer.music.stop()
    lbl_estado.config(text="Detenido ⏹")

# --- GUI ---
root = tk.Tk()
root.title("PyAmp Pro 🎵")
root.geometry("500x550")
root.config(bg="#1e1e1e")
root.resizable(False, False)

# Título
tk.Label(root, text="PyAmp Player", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)

# Lista
playlist = tk.Listbox(root, bg="#222", fg="#0f0", width=55, height=15, selectbackground="#444", borderwidth=0)
playlist.pack(padx=20, pady=5)

lbl_estado = tk.Label(root, text="---", bg="#1e1e1e", fg="gray")
lbl_estado.pack()

frame_controles = tk.Frame(root, bg="#1e1e1e")
frame_controles.pack(pady=20)

# --- CARGA DE IMÁGENES SEGURA ---
# Al no usar os.chdir, Python siempre buscará las imágenes junto al script
try:
    # Ajusta el subsample según necesites (8, 10, 15...)
    img_play = tk.PhotoImage(file="play.png").subsample(10, 10)
    img_pause = tk.PhotoImage(file="pause.png").subsample(10, 10)
    img_stop = tk.PhotoImage(file="stop.png").subsample(10, 10)

    btn_pause = tk.Button(frame_controles, image=img_pause, command=pausar, bg="#1e1e1e", borderwidth=0)
    btn_play = tk.Button(frame_controles, image=img_play, command=reproducir, bg="#1e1e1e", borderwidth=0)
    btn_stop = tk.Button(frame_controles, image=img_stop, command=parar, bg="#1e1e1e", borderwidth=0)

    btn_pause.grid(row=0, column=0, padx=10)
    btn_play.grid(row=0, column=1, padx=10)
    btn_stop.grid(row=0, column=2, padx=10)

except Exception as e:
    print(f"⚠️ Error cargando imágenes: {e}")
    tk.Button(frame_controles, text="PLAY", command=reproducir).pack(side=tk.LEFT)
    tk.Button(frame_controles, text="PAUSE", command=pausar).pack(side=tk.LEFT)
    tk.Button(frame_controles, text="STOP", command=parar).pack(side=tk.LEFT)

btn_cargar = tk.Button(root, text="📂 ABRIR CARPETA", command=cargar_carpeta, 
                       bg="#007acc", fg="white", font=("Arial", 10, "bold"), relief="flat")
btn_cargar.pack(pady=15)

root.mainloop()