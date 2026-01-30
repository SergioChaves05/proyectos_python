import yt_dlp
import sys

def descargar_contenido(url, tipo):
    """
    tipo: 'video' para MP4, 'audio' para MP3
    """
    
    # 1. Configuración Base (Común para ambos)
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s', # Nombre del archivo
        'noplaylist': True,             # No descargar listas enteras
        'quiet': False,                 # Ver barra de progreso
    }

    # 2. Configuración Específica según lo que elija el usuario
    if tipo == 'audio':
        print("🎵 Configurando para AUDIO (MP3)...")
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    
    elif tipo == 'video':
        print("🎬 Configurando para VIDEO (MP4)...")
        ydl_opts.update({
            # Descarga el mejor video y el mejor audio por separado
            'format': 'bestvideo+bestaudio/best',
            # ¡IMPORTANTE! Usa FFmpeg para pegarlos en un contenedor MP4
            'merge_output_format': 'mp4', 
        })

    # 3. Proceso de Descarga
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n Analizando: {url}...")
            info = ydl.extract_info(url, download=False)
            
            print(f"Título: {info.get('title')}")
            print(f"Duración: {info.get('duration')} seg")
            
            # Confirmación final
            confirmar = input(f"¿Confirmar descarga en formato {tipo.upper()}? (s/n): ").lower()
            
            if confirmar == 's':
                print("Descargando y procesando... (Paciencia, usa CPU)")
                ydl.download([url])
                print(f"¡Hecho! Archivo guardado como {tipo.upper()}.")
            else:
                print("Cancelado por el usuario.")

    except Exception as e:
        print(f"Error: {e}")

# --- MENÚ PRINCIPAL ---
if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print(" 📺 YT MASTER DOWNLOADER ")
        print("="*40)
        
        url = input("Pegue el enlace (o 'q' para salir): ")
        if url.lower() == 'q':
            print("¡Hasta luego!")
            break

        print("\n¿Qué desea descargar?")
        print("1. 🎵 Solo Audio (.mp3)")
        print("2. 🎬 Video Completo (.mp4)")
        
        opcion = input("Elija una opción (1 o 2): ")

        if opcion == '1':
            descargar_contenido(url, 'audio')
        elif opcion == '2':
            descargar_contenido(url, 'video')
        else:
            print("Opción no válida. Intente de nuevo.")