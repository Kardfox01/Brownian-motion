import pygame as pg

from threading import Thread
from random import randint as rd
from time import time, sleep

from parameters import*
from particle import Particle
from coordinates import Coordinates, TrajectoryPoint


class BrownianMotionApp:
    def __init__(self):
        pg.init()

        self._screen    : pg.Surface = pg.display.set_mode((SIDE, SIDE))
        self._particles : list[Particle] = []

        self._running = True
        self._pause   = False

        pg.display.set_caption(CAPTION)
        pg.display.set_icon(pg.image.load(ICON))

    def run(self):
        clock = pg.time.Clock()

        while self._running:
            pg.event.get()
            self._screen.fill(FILL)

            for particle in self._particles:
                if not self._pause:
                    particle.check_collision(self._particles)
                    particle.movement()

                pg.draw.circle(
                    self._screen,
                    particle.color,
                    particle.coords.get,
                    particle.radius
                )
                for point in particle.trajectory:
                    pg.draw.circle(self._screen, point.color, point.coords, 5)

            pg.display.update()
            clock.tick(75)
        pg.quit()

    def track(self, uid: int, seconds: int):
        particle = self._particles[uid]
        start = time()

        while time() - start < seconds:
            speed = (particle.Vᵪ**2 + particle.Vᵧ**2)**.5
            particle.trajectory.append(
                TrajectoryPoint(
                    particle.coords.get,
                    (int(255 * speed / V / 2), 0, 0)
                )
            )
            sleep(.03)
        self.pause()

    def add(self, N: int):
        for _ in range(N):
            self._particles.append(
                Particle(
                    len(self._particles),
                    RADIUS,
                    MASS,
                    rd(-V, V),
                    rd(-V, V),
                    Coordinates(
                        rd(0, SIDE - RADIUS*2),
                        rd(0, SIDE - RADIUS*2)
                    ),
                    COLOR
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
    ):
        self._particles.append(
            Particle(
                len(self._particles),
                radius,
                mass,
                Vx or rd(-V, V),
                Vy or rd(-V, V),
                Coordinates(
                    rd(0, SIDE - RADIUS*2),
                    rd(0, SIDE - RADIUS*2)
                ),
                (color_r, color_g, color_b)
            )
        )
        print("UID: ", len(self._particles) - 1)

    def highlight(self, uid: int):
        for particle in self._particles:
            if particle.uid != uid:
                particle.color = FILL

    def clear(self):
        self._particles.clear()

    def count(self):
        print(len(self._particles))

    def pause(self):
        self._pause = not self._pause

    def stop(self):
        self._running = False

    def cmd(self):
        commands = {
            "добавить": self.add,       # добавить N                      - добавляет N обычных частиц
            "очистить": self.clear,     # очистить                        - удаляет все частицы
            "создать" : self.create,    # создать RADIUS MASS VX VY R G B - добавляет 1 частицу с заданными параметрами
            "кол-во"  : self.count,     # кол-во                          - выводит кол-во частиц на экране
            "выделить": self.highlight, # выделить UID                    - прячет все частицы, кроме указанной
            "следить" : self.track,     # отслеживать UID SECONDS         - рисует траекторию указанной частицы
            "пауза"   : self.pause,     # пауза                           - останавливает движение
            "стоп"    : self.stop       # стоп                            - останавливает приложение
        }

        while self._running:
            promt = input().split()
            try:
                command, args = promt[0], (int(arg) for arg in promt[1:])
                commands[command](*args)
            except KeyError:
                print("Такой команды не существует")
            except Exception as e:
                print(e)
        print("Выход...")


if __name__ == "__main__":
    bm = BrownianMotionApp()
    Thread(target=bm.cmd).start()
    bm.run()