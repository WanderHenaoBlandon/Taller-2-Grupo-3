import tkinter as tk


def saludar(nombre):
    return f"Hola, {nombre}"


class JuegoPlataformas:
    ANCHO = 900
    ALTO = 520
    GRAVEDAD = 1
    VELOCIDAD = 5
    SALTO = -15

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Aventura de Plataformas")
        self.ventana.resizable(False, False)
        self.canvas = tk.Canvas(ventana, width=self.ANCHO, height=self.ALTO, highlightthickness=0)
        self.canvas.pack()

        self.teclas = set()
        self.puntuacion = 0
        self.juego_terminado = False
        self.jugador = {"x": 80, "y": 380, "ancho": 32, "alto": 42, "velocidad_y": 0}
        self.plataformas = [
            (0, 470, 900, 520),
            (100, 390, 260, 410),
            (410, 330, 590, 350),
            (660, 250, 850, 270),
            (250, 210, 420, 230),
        ]
        self.monedas = [
            {"x": 180, "y": 350, "tomada": False},
            {"x": 475, "y": 290, "tomada": False},
            {"x": 730, "y": 210, "tomada": False},
            {"x": 320, "y": 170, "tomada": False},
        ]

        ventana.bind("<KeyPress>", self.tecla_presionada)
        ventana.bind("<KeyRelease>", self.tecla_liberada)
        self.dibujar()
        self.actualizar()

    def tecla_presionada(self, evento):
        self.teclas.add(evento.keysym.lower())
        if evento.keysym.lower() == "r" and self.juego_terminado:
            self.reiniciar()

    def tecla_liberada(self, evento):
        self.teclas.discard(evento.keysym.lower())

    def reiniciar(self):
        self.jugador.update({"x": 80, "y": 380, "velocidad_y": 0})
        for moneda in self.monedas:
            moneda["tomada"] = False
        self.puntuacion = 0
        self.juego_terminado = False

    def esta_sobre_plataforma(self):
        jugador = self.jugador
        parte_inferior = jugador["y"] + jugador["alto"]
        for izquierda, arriba, derecha, abajo in self.plataformas:
            toca_horizontal = jugador["x"] + jugador["ancho"] > izquierda and jugador["x"] < derecha
            cerca_del_piso = parte_inferior >= arriba and parte_inferior <= arriba + 8
            if toca_horizontal and cerca_del_piso and jugador["velocidad_y"] >= 0:
                jugador["y"] = arriba - jugador["alto"]
                jugador["velocidad_y"] = 0
                return True
        return False

    def actualizar(self):
        if not self.juego_terminado:
            if "left" in self.teclas or "a" in self.teclas:
                self.jugador["x"] -= self.VELOCIDAD
            if "right" in self.teclas or "d" in self.teclas:
                self.jugador["x"] += self.VELOCIDAD

            en_plataforma = self.esta_sobre_plataforma()
            if ("up" in self.teclas or "w" in self.teclas or "space" in self.teclas) and en_plataforma:
                self.jugador["velocidad_y"] = self.SALTO

            self.jugador["velocidad_y"] += self.GRAVEDAD
            self.jugador["y"] += self.jugador["velocidad_y"]
            self.esta_sobre_plataforma()
            self.jugador["x"] = max(0, min(self.ANCHO - self.jugador["ancho"], self.jugador["x"]))

            for moneda in self.monedas:
                distancia_x = abs(self.jugador["x"] + 16 - moneda["x"])
                distancia_y = abs(self.jugador["y"] + 21 - moneda["y"])
                if not moneda["tomada"] and distancia_x < 28 and distancia_y < 35:
                    moneda["tomada"] = True
                    self.puntuacion += 10

            if self.jugador["y"] > self.ALTO:
                self.juego_terminado = True

            if all(moneda["tomada"] for moneda in self.monedas):
                self.juego_terminado = True

        self.dibujar()
        self.ventana.after(30, self.actualizar)

    def dibujar(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.ANCHO, self.ALTO, fill="#9bdcf5", outline="")
        self.canvas.create_oval(720, 35, 800, 115, fill="#ffe18a", outline="")
        self.canvas.create_text(20, 20, anchor="nw", text=f"Monedas: {self.puntuacion}", font=("Arial", 16, "bold"), fill="#17324d")
        self.canvas.create_text(20, 48, anchor="nw", text="Mover: A/D o flechas | Saltar: W, flecha arriba o espacio", font=("Arial", 11), fill="#17324d")

        for izquierda, arriba, derecha, abajo in self.plataformas:
            self.canvas.create_rectangle(izquierda, arriba, derecha, abajo, fill="#4d9a51", outline="#286331", width=2)
            self.canvas.create_rectangle(izquierda, arriba, derecha, arriba + 7, fill="#a6d96a", outline="")

        for moneda in self.monedas:
            if not moneda["tomada"]:
                self.canvas.create_oval(moneda["x"] - 10, moneda["y"] - 10, moneda["x"] + 10, moneda["y"] + 10, fill="#ffd447", outline="#b87800", width=2)

        jugador = self.jugador
        self.canvas.create_rectangle(jugador["x"], jugador["y"], jugador["x"] + jugador["ancho"], jugador["y"] + jugador["alto"], fill="#e84d4d", outline="#8f2525", width=2)
        self.canvas.create_rectangle(jugador["x"] + 5, jugador["y"] + 8, jugador["x"] + 27, jugador["y"] + 18, fill="#ffd2a6", outline="")

        if self.juego_terminado:
            mensaje = "¡Ganaste! Presiona R para jugar otra vez" if all(moneda["tomada"] for moneda in self.monedas) else "Fin del juego. Presiona R para reiniciar"
            self.canvas.create_rectangle(220, 200, 680, 300, fill="#17324d", outline="#ffffff", width=2)
            self.canvas.create_text(450, 250, text=mensaje, fill="white", font=("Arial", 18, "bold"))


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    JuegoPlataformas(ventana_principal)
    ventana_principal.mainloop()