from os import environ, system
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg
import parameters as ps

from threading import Thread
from random import randint as rd
from time import time, sleep
from colorama import Fore, Style, just_fix_windows_console
from particle import Particle
from coordinates import Coordinates, TrajectoryPoint


class BrownianMotionApp:
    def __init__(self):
        pg.init()

        self.__screen   : pg.Surface = pg.display.set_mode((ps.WIDTH, ps.HEIGHT), pg.RESIZABLE)
        self.__particles: list[Particle] = []

        self.__running = True
        self.__pause   = False
        self.__cmd     = False

        pg.display.set_caption(ps.CAPTION)
        pg.display.set_icon(pg.image.load(ps.ICON))

    def run(self):
        clock = pg.time.Clock()

        while self.__running:
            self.__screen.fill(ps.FILL)

            for event in pg.event.get():
                if event.type == pg.QUIT and not self.__cmd:
                    self.exit()
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

            thread1 = Thread(target=move, args=(self.__particles[half_count:],))
            thread1.start()
            thread1.join()

            thread2 = Thread(target=move, args=(self.__particles[:half_count],))
            thread2.start()
            thread2.join()

            pg.display.update()
            clock.tick(75)
        pg.quit()

    def create(self, *args: int):
        N = args[0]
        radius, mass, Vx, Vy, r, g, b = ps.RADIUS, ps.MASS, None, None, *ps.COLOR

        if len(args) > 1:
            N = 1
            radius, mass, Vx, Vy, r, g, b = args

        for _ in range(N):
            self.__particles.append(
                Particle(
                    len(self.__particles),
                    radius,
                    mass,
                    Vx if Vx != None else rd(-ps.V, ps.V),
                    Vy if Vy != None else rd(-ps.V, ps.V),
                    Coordinates(
                        rd(radius, ps.WIDTH - radius*2),
                        rd(radius, ps.HEIGHT - radius*2)
                    ),
                    (r, g, b)
                )
            )

        if N == 1:
            return f"UID: {len(self.__particles) - 1}"
    def count(self):
        return len(self.__particles)

    def highlight(self, uid: int):
        for particle in self.__particles:
            if particle.uid != uid:
                particle.show = False

    def track(self, seconds: int, uid: int):
        self.highlight(uid)
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

        self.stop()
    def reset(self):
        for particle in self.__particles:
            particle.show = True
            particle.trajectory.clear()
        self.__pause = True

    def stop(self):
        self.__pause = not self.__pause

    def exit(self):
        self.__running = False

    def cli(self):
        HELP = f"""
        {Fore.CYAN}создать{Fore.WHITE} {Fore.GREEN}RADIUS MASS VX VY R G B{Fore.WHITE} - добавляет 1 частицу с заданными параметрами
        {Fore.CYAN}создать{Fore.WHITE} {Fore.GREEN}N{Fore.WHITE}                       - создаёт {Fore.GREEN}N{Fore.WHITE} частиц с параметрами по-умолчанию
        {Fore.CYAN}очистить{Fore.WHITE}                        - удаляет все частицы
        {Fore.CYAN}кол-во{Fore.WHITE}                          - выводит кол-во частиц на экране
        {Fore.CYAN}выделить{Fore.WHITE} {Fore.GREEN}UIDS{Fore.WHITE}                   - прячет все частицы, кроме {Fore.GREEN}UIDS{Fore.WHITE}
        {Fore.CYAN}отслеживать{Fore.WHITE} {Fore.GREEN}SECONDS UID{Fore.WHITE}         - рисует траекторию частицы {Fore.GREEN}UID SECONDS{Fore.WHITE} секунд
        {Fore.CYAN}стоп{Fore.WHITE}                            - останавливает движение
        {Fore.CYAN}выход{Fore.WHITE}                           - выход из приложения
        {Fore.CYAN}сброс{Fore.WHITE}                           - сбрасывает изменения после {Fore.CYAN}выделить{Fore.WHITE} или {Fore.CYAN}следить{Fore.WHITE}
        {Fore.CYAN}помощь{Fore.WHITE}                          - вывод справки
        """

        PROMT = f"{Style.NORMAL}{Fore.CYAN}>>> {Fore.RESET}{Style.BRIGHT}"

        if self.__cmd:
            commands = {
                "создать" : self.create,
                "очистить": self.__particles.clear,
                "кол-во"  : self.count,
                "выделить": self.highlight,
                "следить" : self.track,
                "стоп"    : self.stop,
                "выход"   : self.exit,
                "сброс"   : self.reset,
                "помощь"  : lambda: HELP
            }

            while self.__running:
                promt = input(PROMT).split()
                try:
                    command, args = promt[0], (int(arg) for arg in promt[1:])
                    result = commands[command](*args)
                    if result: print(result)
                except KeyError:
                    print("Такой команды не существует")
                except Exception as e:
                    print(e)
            print(f"Выход...{Style.RESET_ALL}")
            return

        just_fix_windows_console()
        system("cls")
        self.__cmd = True
        Thread(target=self.cli).start()


if __name__ == "__main__":
    bm = BrownianMotionApp()
    bm.cli()
    bm.run()