from os import environ, system
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg

from threading import Thread
from random import randint as rd
from time import time, sleep
from colorama import just_fix_windows_console, Fore

import parameters as ps
from particle import Particle
from coordinates import Coordinates, TrajectoryPoint


class BrownianMotionApp:
    def __init__(self):
        pg.init()

        self.__screen    : pg.Surface = pg.display.set_mode((ps.WIDTH, ps.HEIGHT), pg.RESIZABLE)
        self.__particles : list[Particle] = []

        self.__running    = True
        self.__pause      = False
        self.__cmd        = False

        pg.display.set_caption(ps.CAPTION)
        pg.display.set_icon(pg.image.load(ps.ICON))

    def run(self):
        clock = pg.time.Clock()

        while self.__running:
            self.__screen.fill(ps.FILL)

            for event in pg.event.get():
                if (
                    (event.type == pg.QUIT  or
                    (event.type == pg.KEYUP and event.key == pg.K_ESCAPE)) and
                    not self.__cmd
                ):
                    self.stop()
                elif event.type == pg.VIDEORESIZE:
                    ps.WIDTH, ps.HEIGHT = event.w, event.h
                    self.__screen = pg.display.set_mode((ps.WIDTH, ps.HEIGHT), pg.RESIZABLE)

            def move(particles: list[Particle]):
                for particle in particles:
                    if not self.__pause:
                        particle.check_collision(self.__particles)
                        particle.movement()

                    if particle.show:
                        pg.draw.circle(
                            self.__screen,
                            particle.color,
                            particle.coords.get,
                            particle.radius
                        )

                    if particle.trajectory:
                        for point in particle.trajectory:
                            pg.draw.line(
                                self.__screen,
                                point.color,
                                point.coords_start,
                                point.coords_end,
                                4
                            )

                        pg.draw.circle(
                            self.__screen,
                            (0, 255, 0),
                            particle.trajectory[0].coords_start,
                            10
                        )

            half_count = len(self.__particles) // 2

            Thread(target=move, args=(self.__particles[half_count:],)).start()

            thread2 = Thread(target=move, args=(self.__particles[:half_count],))
            thread2.start()
            thread2.join()

            pg.display.update()
            clock.tick(75)
        pg.quit()

    def add(self, N: int):
        for _ in range(N):
            self.create(
                ps.RADIUS,
                ps.MASS,
                rd(-ps.V, ps.V),
                rd(-ps.V, ps.V),
                *ps.COLOR
            )

    def create(
        self,
        radius : int,
        mass   : int,
        Vx     : int,
        Vy     : int,
        r: int,
        g: int,
        b: int
    ):
        self.__particles.append(
            Particle(
                len(self.__particles),
                radius,
                mass,
                Vx,
                Vy,
                Coordinates(
                    rd(radius, ps.WIDTH - radius*2),
                    rd(radius, ps.HEIGHT - radius*2)
                ),
                (r, g, b)
            )
        )

        return f"UID: {len(self.__particles) - 1}"

    def count(self):
        return len(self.__particles)

    def highlight(self, *uid: int):
        for particle in self.__particles:
            if not particle.uid in uid:
                particle.show = False

    def track(self, seconds: int, uid: int):
        self.__pause = False

        particle = self.__particles[uid]
        start = time()

        while time() - start < seconds:
            speed = (particle.Vx**2 + particle.Vy**2)**.5
            color = (
                particle.color[0] * speed // ps.V // 1.5,
                particle.color[1] * speed // ps.V // 1.5,
                particle.color[2] * speed // ps.V // 1.5
            )

            coords_start = particle.coords.get
            sleep(.05)
            coords_end = particle.coords.get

            particle.trajectory.append(
                TrajectoryPoint(
                    coords_start,
                    coords_end,
                    (
                        color[0] if color[0] <= 255 else 255,
                        color[1] if color[1] <= 255 else 255,
                        color[2] if color[2] <= 255 else 255
                    )
                )
            )

        self.pause()

    def reset(self):
        for particle in self.__particles:
            particle.show = True
            particle.trajectory.clear()

    def pause(self):
        self.__pause = not self.__pause

    def stop(self):
        self.__running = False

    def cli(self):
        if self.__cmd:
            commands = {
                "создать" : self.create,            # создать RADIUS MASS VX VY R G B - добавляет 1 частицу с заданными параметрами
                "добавить": self.add,               # создатьмн N                     - добавляет N обычных частиц
                "очистить": self.__particles.clear, # очистить                        - удаляет все частицы
                "кол-во"  : self.count,             # кол-во                          - выводит кол-во частиц на экране
                "выделить": self.highlight,         # выделить UIDS                   - прячет все частицы, кроме указанных
                "следить" : self.track,             # отслеживать SECONDS UID         - рисует траекторию указанной частицы SECONDS секунд
                "пауза"   : self.pause,             # пауза                           - останавливает движение
                "стоп"    : self.stop,              # стоп                            - останавливает приложение
                "сброс"   : self.reset              # сброс                           - сбрасывает изменения после / выделить / или / следить /
            }

            while self.__running:
                promt = input(Fore.LIGHTCYAN_EX + ">>> ").split()
                try:
                    command, args = promt[0], (int(arg) for arg in promt[1:])
                    result = commands[command](*args)
                    if result: print(result)
                except KeyError:
                    print("Такой команды не существует")
                except Exception as e:
                    print(e)
            print(f"Выход...{Fore.RESET}")
            return

        just_fix_windows_console()
        system("cls")
        self.__cmd = True
        Thread(target=self.cli).start()


if __name__ == "__main__":
    bm = BrownianMotionApp()
    bm.cli()
    bm.run()