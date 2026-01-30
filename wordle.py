import random
PALABRAS = ["PERRO", "GATO", "CASA", "ARBOL", "LIBRO", "SILLA", "MESA", "CIELO", "MAR", 
            "SOL", "LUNA", "ESTRELLA", "NUBE", "RÍO", "MONTAÑA", "FLOR", "FRUTA", "CIUDAD", "PAÍS", "MUNDO", 
            "AMIGO", "FAMILIA", "ESCUELA", "TRABAJO", "JUEGO", "MÚSICA", "DANZA", "CINE", "TEATRO", "ARTE", 
            "CIENCIA", "TECNOLOGÍA", "SIDA", "BOGRIFALO", "VIH", "CLAVICEMBALO", "PORTADOR", "MOSQUITO", "HOMOSEXUAL",
            "ORNITORRINCO", "HIPOPÓTAMO", "ELEFANTE", "PINGÜINO", "ORNITÓLOGO", "DEFICIENCIA"]

def elegir_palabra():
    return random.choice(PALABRAS)

def colorear_letra(letra, estado):
    if estado == 'correcta':
        return f"\033[92m{letra}\033[0m"  # Verde
    elif estado == 'presente':
        return f"\033[93m{letra}\033[0m"  # Amarillo
    else:
        return f"\033[90m{letra}\033[0m"  # Gris
    
def jugar_wordle():
    palabra_secreta = elegir_palabra()
    intentos = 6
    longitud_palabra = len(palabra_secreta)
    
    print("¡Bienvenido a Wordle en la Terminal!")
    print(f"Tienes {intentos} intentos para adivinar la palabra de {longitud_palabra} letras.")
    
    for intento in range(intentos):
        while True:
            intento_usuario = input(f"\nIntento {intento + 1}: ").upper()
            if len(intento_usuario) != longitud_palabra:
                print(f"Por favor, ingresa una palabra de {longitud_palabra} letras.")
            else:
                break
        
        # --- NUEVA LÓGICA AVANZADA ---
        
        # 1. Creamos una lista vacía para guardar los estados ('correcta', 'gris')
        # Inicialmente todo es None
        estados_resultado = [None] * longitud_palabra
        
        # 2. Contamos cuántas letras tiene la palabra secreta (Inventario disponible)
        # Ejemplo: ACERO -> {'A':1, 'C':1, 'E':1, 'R':1, 'O':1}
        conteo_secreta = {}
        for letra in palabra_secreta:
            conteo_secreta[letra] = conteo_secreta.get(letra, 0) + 1
            
        # 3. PRIMERA PASADA: Buscar VERDES (Prioridad absoluta)
        for i in range(longitud_palabra):
            letra = intento_usuario[i]
            if letra == palabra_secreta[i]:
                estados_resultado[i] = 'correcta'
                # "Gastamos" una letra del inventario
                conteo_secreta[letra] -= 1
        
        # 4. SEGUNDA PASADA: Buscar AMARILLOS y GRISES
        for i in range(longitud_palabra):
            # Si ya es verde, lo saltamos
            if estados_resultado[i] == 'correcta':
                continue
            
            letra = intento_usuario[i]
            
            # Verificamos si la letra existe en la secreta Y si quedan copias disponibles
            if letra in conteo_secreta and conteo_secreta[letra] > 0:
                estados_resultado[i] = 'presente'
                conteo_secreta[letra] -= 1 # Gastamos la copia disponible
            else:
                estados_resultado[i] = 'ausente'
        
        # --- FIN LÓGICA ---

        # Imprimir resultado visual
        salida_visual = []
        for i in range(longitud_palabra):
            salida_visual.append(colorear_letra(intento_usuario[i], estados_resultado[i]))
            
        print("Resultado: " + " ".join(salida_visual))
        
        if intento_usuario == palabra_secreta:
            print("¡Felicidades! ¡Has adivinado la palabra!")
            break
    else:
        print(f"Lo siento, has agotado tus intentos. La palabra era: {palabra_secreta}")

if __name__ == "__main__":
    jugar_wordle()