import pygame
import random
import sys

# --- CONFIGURACIÓN ---
ANCHO = 800
ALTO = 600
TAMAÑO_CASILLA = 50
GRID_ANCHO = ANCHO // TAMAÑO_CASILLA
GRID_ALTO = ALTO // TAMAÑO_CASILLA

COLOR_FONDO = (30, 30, 30)
COLOR_GRID = (50, 50, 50)
FPS = 60

# Colores
ROJO = (200, 50, 50)
AZUL = (50, 50, 200)
VERDE = (50, 200, 50)
BLANCO = (255, 255, 255)
AMARILLO = (255, 215, 0)
GRIS_OSCURO = (100, 100, 100)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, nombre, color, x_inicial, y_inicial, controles):
        super().__init__()
        self.nombre = nombre
        self.color = color
        
        # El jugador ocupa casi toda la casilla
        self.image = pygame.Surface((TAMAÑO_CASILLA - 4, TAMAÑO_CASILLA - 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        # Posición lógica
        self.grid_x = x_inicial
        self.grid_y = y_inicial
        
        # ESTADÍSTICAS
        self.vida = 100
        self.fuerza = 20 # Daño base
        
        self.teclas = controles
        
        # Cooldowns
        self.ultimo_movimiento = 0
        self.cooldown_movimiento = 150 
        self.ultimo_ataque = 0
        self.cooldown_ataque = 500 

    def empujar(self, dx, dy):
        self.grid_x += dx
        self.grid_y += dy
        
        # Ring Out
        if self.grid_x < 0 or self.grid_x >= GRID_ANCHO or self.grid_y < 0 or self.grid_y >= GRID_ALTO:
            self.vida = 0
            print(f"💀 ¡{self.nombre} ha caído del mapa!")

    def atacar(self, enemigo, tiempo_actual):
        if tiempo_actual - self.ultimo_ataque < self.cooldown_ataque:
            return

        dx = enemigo.grid_x - self.grid_x
        dy = enemigo.grid_y - self.grid_y
        distancia = abs(dx) + abs(dy)

        if distancia == 1:
            self.ultimo_ataque = tiempo_actual
            
            # DAÑO DINÁMICO (Usa la fuerza actual)
            enemigo.vida -= self.fuerza
            print(f"⚔️ {self.nombre} pega por {self.fuerza} de daño!")
            
            # Efecto visual (Empuje)
            enemigo.empujar(dx, dy)

    def update(self, teclas_pulsadas, tiempo_actual, enemigo):
        # Movimiento
        if tiempo_actual - self.ultimo_movimiento > self.cooldown_movimiento:
            dx, dy = 0, 0
            if teclas_pulsadas[self.teclas['arriba']]: dy = -1
            elif teclas_pulsadas[self.teclas['abajo']]: dy = 1
            elif teclas_pulsadas[self.teclas['izq']]: dx = -1
            elif teclas_pulsadas[self.teclas['der']]: dx = 1
            
            if dx != 0 or dy != 0:
                nuevo_x = self.grid_x + dx
                nuevo_y = self.grid_y + dy

                # Límites y Colisión con enemigo
                if 0 <= nuevo_x < GRID_ANCHO and 0 <= nuevo_y < GRID_ALTO:
                    if not (nuevo_x == enemigo.grid_x and nuevo_y == enemigo.grid_y):
                        self.grid_x = nuevo_x
                        self.grid_y = nuevo_y
                        self.ultimo_movimiento = tiempo_actual

        # Ataque
        if teclas_pulsadas[self.teclas['atacar']]:
            self.atacar(enemigo, tiempo_actual)

        # Actualizar posición visual
        self.rect.x = self.grid_x * TAMAÑO_CASILLA + 2
        self.rect.y = self.grid_y * TAMAÑO_CASILLA + 2

class Item(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo 
        
        # CAMBIO 1: Tamaño más pequeño (Un tercio de la casilla)
        tamaño_item = TAMAÑO_CASILLA // 3
        self.image = pygame.Surface((tamaño_item, tamaño_item))
        
        if tipo == "vida":
            self.image.fill(VERDE)
        else:
            self.image.fill(AMARILLO)
            
        self.rect = self.image.get_rect()
        
        # Centrar el item en la casilla
        offset = (TAMAÑO_CASILLA - tamaño_item) // 2
        self.rect.x = x * TAMAÑO_CASILLA + offset
        self.rect.y = y * TAMAÑO_CASILLA + offset

def dibujar_grid(pantalla):
    for x in range(0, ANCHO, TAMAÑO_CASILLA):
        pygame.draw.line(pantalla, COLOR_GRID, (x, 0), (x, ALTO))
    for y in range(0, ALTO, TAMAÑO_CASILLA):
        pygame.draw.line(pantalla, COLOR_GRID, (0, y), (ANCHO, y))

def dibujar_texto(pantalla, texto, tamaño, x, y, color=BLANCO):
    fuente = pygame.font.SysFont("Arial", tamaño, bold=True)
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("🥊 Lucha Táctica: Items Dinámicos")
    reloj = pygame.time.Clock()

    controles_p1 = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d, 'atacar': pygame.K_k}
    controles_p2 = {'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN, 'izq': pygame.K_LEFT, 'der': pygame.K_RIGHT, 'atacar': pygame.K_l}

    todos_sprites = pygame.sprite.Group()
    items_grupo = pygame.sprite.Group()

    j1 = Jugador("ROJO", ROJO, 2, 6, controles_p1)
    j2 = Jugador("AZUL", AZUL, 13, 6, controles_p2)
    todos_sprites.add(j1)
    todos_sprites.add(j2)

    # Variables para generación de items
    ultimo_respawn_item = 0
    TIEMPO_RESPAWN = 3000 # 3 segundos (3000 ms)

    ejecutando = True
    ganador = None

    while ejecutando:
        tiempo_actual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        if ganador is None:
            teclas = pygame.key.get_pressed()
            j1.update(teclas, tiempo_actual, j2)
            j2.update(teclas, tiempo_actual, j1)

            # --- CAMBIO 4: Generación Dinámica de Items ---
            if tiempo_actual - ultimo_respawn_item > TIEMPO_RESPAWN:
                # Máximo 10 items en pantalla para no saturar
                if len(items_grupo) < 10:
                    tipo = random.choice(["vida", "fuerza"])
                    rx = random.randint(0, GRID_ANCHO - 1)
                    ry = random.randint(0, GRID_ALTO - 1)
                    
                    # Crear item
                    nuevo_item = Item(tipo, rx, ry)
                    items_grupo.add(nuevo_item)
                    todos_sprites.add(nuevo_item)
                    
                    ultimo_respawn_item = tiempo_actual

            # --- Recoger Items ---
            # Jugador 1
            lista_items_j1 = pygame.sprite.spritecollide(j1, items_grupo, True)
            for item in lista_items_j1:
                if item.tipo == "vida":
                    j1.vida = min(100, j1.vida + 20)
                elif item.tipo == "fuerza":
                    j1.fuerza += 5 # CAMBIO 2 y 3: Sube el daño
            
            # Jugador 2
            lista_items_j2 = pygame.sprite.spritecollide(j2, items_grupo, True)
            for item in lista_items_j2:
                if item.tipo == "vida":
                    j2.vida = min(100, j2.vida + 20)
                elif item.tipo == "fuerza":
                    j2.fuerza += 5

            # Muerte
            if j1.vida <= 0: ganador = j2.nombre
            if j2.vida <= 0: ganador = j1.nombre

        # Dibujar
        pantalla.fill(COLOR_FONDO)
        dibujar_grid(pantalla)
        items_grupo.draw(pantalla) # Dibujamos items abajo
        todos_sprites.draw(pantalla) # Jugadores encima

        # HUD Mejorado (Muestra Vida y Daño)
        texto_p1 = f"P1: {max(0, j1.vida)}% HP | Daño: {j1.fuerza}"
        texto_p2 = f"P2: {max(0, j2.vida)}% HP | Daño: {j2.fuerza}"
        
        dibujar_texto(pantalla, texto_p1, 20, 10, 10, ROJO)
        dibujar_texto(pantalla, texto_p2, 20, ANCHO - 250, 10, AZUL)

        if ganador:
            dibujar_texto(pantalla, f"🏆 ¡GANADOR: {ganador}!", 50, ANCHO//2 - 200, ALTO//2 - 50, AMARILLO)
            dibujar_texto(pantalla, "ESC para salir", 20, ANCHO//2 - 50, ALTO//2 + 20)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                ejecutando = False

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()