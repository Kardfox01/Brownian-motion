import pygame as pg
from particle import Particle
from coordinates import Coordinates
from threading import Thread
from random import randint as rd


class BrownianMotion:
    class Parameters:
        # Окно
        CAPTION = "Brownian motion"
        SIDE    = 900
        ICON    = "icon.ico"
        FILL    = (255, 255, 255)

        # Физика
        V      = 10
        MASS   = 100
        RADIUS = 20


    def __init__(self):
        pg.init()

        self.screen: pg.Surface = pg.display.set_mode((self.Parameters.SIDE, self.Parameters.SIDE))
        self.particles: list[Particle] = []
        self.running = True

        pg.display.set_caption(self.Parameters.CAPTION)
        pg.display.set_icon(pg.image.load(self.Parameters.ICON))

    def run(self):
        clock = pg.time.Clock()

        while self.running:
            self.screen.fill(self.Parameters.FILL)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.stop()

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    coordinates = Coordinates(*pg.mouse.get_pos())
                    self.add(1, coordinates)

            for particle in self.particles:
                particle.check_collision(self.particles, self.Parameters.SIDE)
                pg.draw.circle(self.screen, *particle.figure())

            pg.display.update()
            clock.tick(75)
        pg.quit()

    def add(self, N: int, coordinates: Coordinates | None = None):
        for _ in range(N):
            self.particles.append(
                Particle(
                    self.Parameters.RADIUS,
                    self.Parameters.MASS,
                    rd(-self.Parameters.V, self.Parameters.V),
                    rd(-self.Parameters.V, self.Parameters.V),
                    coordinates or Coordinates(
                        rd(0, self.Parameters.SIDE - self.Parameters.RADIUS*2),
                        rd(0, self.Parameters.SIDE - self.Parameters.RADIUS*2)
                    )
                )
            )

    def create(
        self,
        radius : int,
        mass   : int,
        Vx     : int,
        Vy     : int,
        color_r: int,
        color_g: int,
        color_b: int,
        x      : int | None = None,
        y      : int | None = None,
    ):
        self.particles.append(
            Particle(
                radius,
                mass,
                Vx or rd(-self.Parameters.V, self.Parameters.V),
                Vy or rd(-self.Parameters.V, self.Parameters.V),
                Coordinates(
                    x or rd(0, self.Parameters.SIDE - self.Parameters.RADIUS*2),
                    y or rd(0, self.Parameters.SIDE - self.Parameters.RADIUS*2)
                ),
                (color_r, color_g, color_b)
            )
        )

    def stop(self):
        self.running = False

    def command_center(self):
        commands = {
            "добавить": self.add,                           # добавить N                          - добавляет N обычных частиц
            "создать" : self.create,                        # создать RADIUS MASS VX VY R G B X Y - добавляет 1 частицу с заданными параметрами
            "очистить": self.particles.clear,               # очистить                            - удаляет все частицы
            "кол-во"  : lambda: print(len(self.particles)), # кол-во                              - выводит кол-во частиц на экране
            "стоп"    : self.stop                           # стоп                                - останавливает приложение
        }

        while self.running:
            promt = input().split()
            command, args = promt[0], (int(arg) for arg in promt[1:])
            try:
                commands[command](*args)
            except KeyError:
                print("Такой команды не существует")
            except Exception as e:
                print(e)
        print("Выход...")


if __name__ == "__main__":
    bm = BrownianMotion()
    Thread(target=bm.command_center).start()
    bm.run()