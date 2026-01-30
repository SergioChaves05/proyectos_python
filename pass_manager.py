from cryptography.fernet import Fernet
import os

def cargar_clave():
    clave_archivo = 'clave.key'
    if not os.path.exists(clave_archivo):
        # Si no existe, creamos, guardamos y devolvemos
        clave = Fernet.generate_key()
        with open(clave_archivo, 'wb') as archivo_clave:
            archivo_clave.write(clave)
        return clave
    else:
        # Si existe, leemos y devolvemos
        with open(clave_archivo, 'rb') as archivo_clave:
            clave = archivo_clave.read()
        return clave

# Inicializamos el motor criptográfico
clave = cargar_clave()
fer = Fernet(clave)

def agregar():
    nombre = input("Ingrese el nombre del sitio: ")
    contrasena = input("Ingrese la contraseña: ")
    
    # Encriptamos
    token = fer.encrypt(contrasena.encode())
    
    # Guardamos (Decode para pasar de bytes a string en el txt)
    with open('contrasenas.txt', 'a') as archivo:
        archivo.write(f"{nombre}|{token.decode()}\n")
    print("✅ Contraseña agregada y encriptada.")

def ver():
    print("\n--- TUS CONTRASEÑAS ---")
    # 🛡️ PROTECCIÓN: Verificamos si el archivo existe antes de leerlo
    if not os.path.exists('contrasenas.txt'):
        print("📭 No tienes contraseñas guardadas todavía.")
        return

    with open('contrasenas.txt', 'r') as archivo:
        for linea in archivo:
            # .rstrip() es importante para quitar el salto de linea final
            datos = linea.rstrip()
            if "|" in datos:
                nombre, token = datos.split('|')
                # Desencriptamos
                try:
                    pass_original = fer.decrypt(token.encode()).decode()
                    print(f"🔐 Sitio: {nombre} | Clave: {pass_original}")
                except Exception:
                    print(f"❌ Error al desencriptar {nombre} (¿Cambiaste la clave?)")

while True:
    print("\n1. Agregar nueva")
    print("2. Ver todas")
    print("3. Salir")
    opcion = input("Elige una opción: ")

    if opcion == '1':
        agregar()
    elif opcion == '2':
        ver()
    elif opcion == '3':
        print("👋 ¡Hasta luego!")
        break
    else:
        print("Opción no válida.")