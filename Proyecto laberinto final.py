import os
import random
import tkinter as tk

ANCHO = 12
ALTO = 12

# Historia por niveles
HISTORIA_NIVELES = [
    "Capítulo 1: Te despiertas en un laberinto oscuro. Debes encontrar una salida...",
    "Capítulo 2: Sientes que algo te sigue. Debes avanzar más profundo...",
    "Capítulo 3: Luces misteriosas iluminan el camino. ¿Es una trampa o ayuda?",
    "Capítulo 4: Casi llegas. El corazón late más rápido...",
    "Capítulo Final: La luz de la libertad brilla a lo lejos. ¡Escapa!"
]

NUM_NIVELES = len(HISTORIA_NIVELES)
nivel_actual = 0

def generar_laberinto():
    laberinto = [["#" for _ in range(ANCHO)] for _ in range(ALTO)]
    laberinto[1][1] = " "
    
    def dfs(x, y):
        direcciones = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 1 <= nx < ALTO - 1 and 1 <= ny < ANCHO - 1 and laberinto[nx][ny] == "#":
                laberinto[nx][ny] = " "
                laberinto[x + dx // 2][y + dy // 2] = " "
                dfs(nx, ny)
    dfs(1, 1)
    
    celdas_vacias = [(i, j) for i in range(ALTO) for j in range(ANCHO) if laberinto[i][j] == " "]
    salida_x, salida_y = random.choice(celdas_vacias)
    laberinto[salida_x][salida_y] = "S"
    
    return laberinto, salida_x, salida_y

laberinto, salida_x, salida_y = generar_laberinto()
pos_x, pos_y = 1, 1

movimientos = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}

def cargar_progreso():
    global pos_x, pos_y
    if os.path.exists("progreso.txt"):
        with open("progreso.txt", "r") as archivo:
            try:
                datos = archivo.read().split(",")
                pos_x, pos_y = int(datos[0]), int(datos[1])
            except:
                pos_x, pos_y = 1, 1

def guardar_progreso():
    with open("progreso.txt", "w") as archivo:
        archivo.write(f"{pos_x},{pos_y}")

class LaberintoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aventura en el Laberinto")
        self.canvas = tk.Canvas(root, width=ANCHO * 50, height=ALTO * 50 + 80)
        self.canvas.pack()
        self.texto_historia = self.canvas.create_text(ANCHO * 25, ALTO * 50 + 40, text="", font=("Arial", 14), fill="red")
        self.dibujar_laberinto()
        self.mostrar_historia()
        self.root.bind("<KeyPress>", self.mover_jugador)

    def mostrar_historia(self):
        if nivel_actual < NUM_NIVELES:
            self.canvas.itemconfig(self.texto_historia, text=HISTORIA_NIVELES[nivel_actual])

    def dibujar_laberinto(self):
        self.canvas.delete("all")
        for i in range(ALTO):
            for j in range(ANCHO):
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                if laberinto[i][j] == "#":
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                elif laberinto[i][j] == "S":
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
        self.canvas.create_oval(pos_y * 50 + 10, pos_x * 50 + 10, pos_y * 50 + 40, pos_x * 50 + 40, fill="blue")
        self.texto_historia = self.canvas.create_text(ANCHO * 25, ALTO * 50 + 40, text="", font=("Arial", 14), fill="red")
        self.mostrar_historia()

    def mover_jugador(self, event):
        global pos_x, pos_y
        if event.char in movimientos:
            dx, dy = movimientos[event.char]
            nuevo_x, nuevo_y = pos_x + dx, pos_y + dy
            if 0 <= nuevo_x < ALTO and 0 <= nuevo_y < ANCHO and laberinto[nuevo_x][nuevo_y] != "#":
                pos_x, pos_y = nuevo_x, nuevo_y
                self.dibujar_laberinto()
                if (pos_x, pos_y) == (salida_x, salida_y):
                    self.nivel_completado()

    def nivel_completado(self):
        global nivel_actual, laberinto, salida_x, salida_y, pos_x, pos_y
        nivel_actual += 1
        if nivel_actual >= NUM_NIVELES:
            self.canvas.create_rectangle(50, 50, ANCHO * 50 - 50, ALTO * 50 - 50, fill="red")
            self.canvas.create_text(ANCHO * 25, ALTO * 25, text="¡Has completado la aventura!", font=("Arial", 24), fill="white")
            os.remove("progreso.txt")
        else:
            laberinto, salida_x, salida_y = generar_laberinto()
            pos_x, pos_y = 1, 1
            self.dibujar_laberinto()

if __name__ == "__main__":
    cargar_progreso()
    root = tk.Tk()
    app = LaberintoApp(root)
    root.mainloop()
