from particle import Particle
from coordinates import Coordinates
import pygame as pg

from sectors import Sectors



class BrownianMotion:
    class Parameters:
        # WINDOW
        CAPTION = "Brownian motion"
        SIDE    = 900
        ICON    = "icon.ico"
        FILL    = (255, 255, 255)

        # APP
        N = 3

        # PHYSICS
        V    = 5
        MASS = 5
        SIZE = 10


    def __init__(self):
        pg.init()

        self.screen: pg.Surface = pg.display.set_mode((self.Parameters.SIDE, self.Parameters.SIDE))

        pg.display.set_caption(self.Parameters.CAPTION)
        pg.display.set_icon(pg.image.load(self.Parameters.ICON))

        self.particles: list[Particle] = []
        self.sectors  : Sectors        = Sectors(self.Parameters.N, self.Parameters.SIDE)

    def run(self):
        running = True
        clock   = pg.time.Clock()
    #     sources: list[Source] = []

        while running:
            self.screen.fill(self.Parameters.FILL)

    #         for source in sources:
    #             if not source.reflected:
    #                 pg.draw.circle(
    #                     self.screen,
    #                     (0, 255, 255),
    #                     source.center,
    #                     10
    #                 )
    #             source.draw()

            for event in (event for event in pg.event.get() if event.type in (pg.QUIT, pg.MOUSEBUTTONUP)):
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    coordinates = Coordinates(*pg.mouse.get_pos())
                    self.particles.append(
                        Particle(
                            self.Parameters.SIZE,
                            self.Parameters.MASS,
                            self.Parameters.V,
                            self.sectors.where(coordinates),
                            coordinates
                        )
                    )

            for particle in self.particles:
                pg.draw.circle(self.screen, *particle.get)

            pg.display.update()
            clock.tick(75)
        pg.quit()


if __name__ == "__main__":
    bm = BrownianMotion()
    bm.run()