import random
import time 
import os

def limpiar_pantalla():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls') # Windows

# --- CLASE PERSONAJE ---
class Personaje:
    def __init__(self, nombre, fuerza, defensa, x, y):
        self.nombre = nombre
        self.fuerza = fuerza
        self.defensa = defensa
        self.vida = 100
        self.max_vida = 100
        self.x = x
        self.y = y
        self.inventario = ["Poción"] 

    def atributos(self):
        print(f"📊 {self.nombre} | HP: {self.vida}/{self.max_vida} | Pos: ({self.x},{self.y}) | Inv: {self.inventario}")

    def mover(self, direccion):
        if direccion == 'w' and self.y > 0: self.y -= 1
        elif direccion == 's' and self.y < 9: self.y += 1
        elif direccion == 'a' and self.x > 0: self.x -= 1
        elif direccion == 'd' and self.x < 9: self.x += 1
        else: print("🚫 Muro.")

    def atacar(self, enemigo):
        print(f"⚔️ ¡{self.nombre} ataca a {enemigo.nombre}!")
        time.sleep(0.5) 
        
        es_critico = random.randint(1, 10) > 8 
        daño = self.fuerza - enemigo.defensa
        
        if es_critico:
            daño = int(daño * 1.5)
            print(f"🔥 ¡GOLPE CRÍTICO! 🔥")

        if daño > 0:
            enemigo.vida -= daño
            print(f"💥 ¡{enemigo.nombre} recibe {daño} de daño! (HP: {enemigo.vida})")
        else:
            print(f"🛡️ {enemigo.nombre} bloqueó el ataque.")

    def usar_pocion(self):
        if "Poción" in self.inventario:
            self.vida += 30
            if self.vida > self.max_vida: self.vida = self.max_vida
            self.inventario.remove("Poción")
            print(f"🧪 {self.nombre} se cura (+30 HP).")
        else:
            print("❌ No tienes pociones.")

    def esta_vivo(self):
        return self.vida > 0

# --- SISTEMA DE ITEMS ---
mapa_objetos = {} 

def generar_objetos(cantidad):
    tipos = ["🍎", "⭐", "🛡️"] 
    for _ in range(cantidad):
        rx = random.randint(0, 9)
        ry = random.randint(0, 9)
        mapa_objetos[(rx, ry)] = random.choice(tipos)

def verificar_suelo(jugador):
    coord = (jugador.x, jugador.y)
    item = mapa_objetos.get(coord) 
    
    if item:
        print(f"\n✨ ¡{jugador.nombre} encontró {item}!")
        time.sleep(1)
        
        if item == "🍎":
            jugador.vida += 20
            if jugador.vida > jugador.max_vida: jugador.vida = jugador.max_vida
            print("   ❤️ Vida recuperada!")
        elif item == "⭐":
            jugador.fuerza += 5
            print("   💪 ¡Fuerza aumentada!")
        elif item == "🛡️":
            jugador.defensa += 5
            print("   🛡️ ¡Defensa aumentada!")
            
        del mapa_objetos[coord] # Borramos el item del mapa

# --- MOTORES GRÁFICOS Y LÓGICOS ---
def dibujar_tablero(lista_jugadores):
    # Tablero vacío
    tablero = [[" . " for _ in range(10)] for _ in range(10)]
    
    # 1. FIX: Dibujamos los ITEMS primero
    for (x, y), item in mapa_objetos.items():
        tablero[y][x] = f" {item} "

    # 2. Dibujamos los JUGADORES encima
    for p in lista_jugadores:
        if p.esta_vivo():
            # Si hay alguien ahí, ponemos su inicial
            tablero[p.y][p.x] = f" {p.nombre[0]} " 
    
    print("\n   0  1  2  3  4  5  6  7  8  9")
    for i, fila in enumerate(tablero):
        print(f"{i} " + "".join(fila))

def configurar_partida():
    try:
        num = int(input("¿Cuántos jugadores (2-4)? "))
    except ValueError:
        num = 2 # Por defecto si fallan al escribir
        
    lista = []
    for i in range(num):
        nombre = input(f"Nombre del Jugador {i+1}: ")
        # Posición aleatoria
        nuevo = Personaje(nombre, 20, 5, random.randint(0,9), random.randint(0,9))
        lista.append(nuevo)
    return lista

# --- MAIN ---
if __name__ == "__main__":
    # FIX: Guardamos la lista que nos devuelve la función
    lista_jugadores = configurar_partida() 
    
    # FIX: ¡Hay que llamar a la función para crear las manzanas!
    generar_objetos(10) 
    
    juego_activo = True
    turno_global = 1

    while juego_activo:
        # FIX: Indentación corregida. Esto va DENTRO del while
        for jugador_actual in lista_jugadores:
            
            if not jugador_actual.esta_vivo():
                continue
            
            limpiar_pantalla()
            dibujar_tablero(lista_jugadores) 
            
            print(f"\n🎲 TURNO {turno_global}: {jugador_actual.nombre}")
            jugador_actual.atributos()
            
            accion = input("[W,A,S,D] Mover | [K] Atacar | [P] Poción: ").lower()
            
            if accion in ['w', 'a', 's', 'd']:
                jugador_actual.mover(accion)
                verificar_suelo(jugador_actual)
            
            elif accion == 'p':
                jugador_actual.usar_pocion()
            
            elif accion == 'k':
                # FIX: Lógica PvP (Buscar enemigos en mi casilla)
                enemigo_encontrado = None
                for otro in lista_jugadores:
                    # Si está en mi casilla, está vivo y NO SOY YO MISMO
                    if (otro != jugador_actual and 
                        otro.esta_vivo() and 
                        otro.x == jugador_actual.x and 
                        otro.y == jugador_actual.y):
                        enemigo_encontrado = otro
                        break # Atacamos al primero que veamos
                
                if enemigo_encontrado:
                    jugador_actual.atacar(enemigo_encontrado)
                else:
                    print("💨 Das un golpe al aire. No hay nadie aquí.")
                    time.sleep(0.5)

            # Comprobar victoria
            vivos = [p for p in lista_jugadores if p.esta_vivo()]
            if len(vivos) == 1:
                limpiar_pantalla()
                print("\n" + "⭐"*30)
                print(f"🏆 ¡VICTORIA REAL! {vivos[0].nombre} HA GANADO")
                print("⭐"*30)
                juego_activo = False
                break
        
        turno_global += 1