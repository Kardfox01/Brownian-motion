from os import environ, system
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg

from threading import Thread
from random import randint as rd
from time import time, sleep
from colorama import just_fix_windows_console, Style

import parameters as prms
from particle import Particle
from coordinates import Coordinates, TrajectoryPoint


class BrownianMotionApp:
    def __init__(self):
        pg.init()

        self._screen    : pg.Surface = pg.display.set_mode((prms.WIDTH, prms.HEIGHT), pg.RESIZABLE)
        self._particles : list[Particle] = []

        self._default_width, self._default_height = prms.WIDTH, prms.HEIGHT

        self._running    = True
        self._pause      = False
        self._cmd        = False
        self._fullscreen = False

        pg.display.set_caption(prms.CAPTION)
        pg.display.set_icon(pg.image.load(prms.ICON))

    def run(self):
        clock = pg.time.Clock()

        while self._running:
            self._screen.fill(prms.FILL)

            for event in pg.event.get():
                if (
                    (event.type == pg.QUIT or
                    (event.type == pg.KEYUP and event.key == pg.K_ESCAPE)) and
                    not self._cmd
                ):
                    self.stop()
                elif event.type == pg.VIDEORESIZE:
                    prms.WIDTH, prms.HEIGHT = event.w, event.h
                    self._screen = pg.display.set_mode((prms.WIDTH, prms.HEIGHT), pg.RESIZABLE)
                elif event.type == pg.KEYUP and event.key == pg.K_F11:
                    self._fullscreen = not self._fullscreen
                    self.fullscreen(mode=self._fullscreen)

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
                    (int(255 * speed / prms.V / 2), 0, 0)
                )
            )
            sleep(.03)
        self.pause()

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
                Vx or rd(-prms.V, prms.V),
                Vy or rd(-prms.V, prms.V),
                Coordinates(
                    rd(radius, prms.WIDTH - radius*2),
                    rd(radius, prms.HEIGHT - radius*2)
                ),
                (color_r, color_g, color_b)
            )
        )
        print("UID:", len(self._particles) - 1)

    def create_many(self, N: int):
        for _ in range(N):
            self.create(
                prms.RADIUS,
                prms.MASS,
                rd(-prms.V, prms.V),
                rd(-prms.V, prms.V),
                *prms.COLOR
            )

    def highlight(self, uid: int):
        for particle in self._particles:
            if particle.uid != uid:
                particle.color = prms.FILL
    
    def fullscreen(self, mode):
        if mode:
            self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            prms.WIDTH, prms.HEIGHT = self._screen.get_width(), self._screen.get_height()
        else:
            self._screen = pg.display.set_mode((self._default_width, self._default_height), pg.RESIZABLE)
            prms.WIDTH, prms.HEIGHT = self._default_width, self._default_height

    def clear(self):
        self._particles.clear()

    def count(self):
        print(len(self._particles))

    def pause(self):
        self._pause = not self._pause

    def stop(self):
        self._running = False

    def interpret(self):
        commands = {
            "добавить": self.create_many, # добавить N                      - добавляет N обычных частиц
            "очистить": self.clear,       # очистить                        - удаляет все частицы
            "создать" : self.create,      # создать RADIUS MASS VX VY R G B - добавляет 1 частицу с заданными параметрами
            "кол-во"  : self.count,       # кол-во                          - выводит кол-во частиц на экране
            "выделить": self.highlight,   # выделить UID                    - прячет все частицы, кроме указанной
            "следить" : self.track,       # отслеживать UID SECONDS         - рисует траекторию указанной частицы
            "пауза"   : self.pause,       # пауза                           - останавливает движение
            "стоп"    : self.stop         # стоп                            - останавливает приложение
        }

        while self._running:
            promt = input(Style.BRIGHT + ">>> ").split()
            try:
                command, args = promt[0], (int(arg) for arg in promt[1:])
                commands[command](*args)
            except KeyError:
                print("Такой команды не существует")
            except Exception as e:
                print(e)
        print("Выход..." + Style.NORMAL)

    def cmd(self):
        just_fix_windows_console()
        system("cls")
        self._cmd = True
        Thread(target=self.interpret).start()


if __name__ == "__main__":
    bm = BrownianMotionApp()
    bm.fullscreen(True)
    # bm.cmd()
    bm.create_many(250)
    bm.run()