from __future__ import annotations
from dataclasses import dataclass, field

from coordinates import Coordinates, TrajectoryPoint
import parameters as ps


@dataclass
class Particle:
    uid       : int
    radius    : int
    m         : int
    Vx        : int
    Vy        : int
    coords    : Coordinates
    color     : tuple[int, int, int]
    trajectory: list[TrajectoryPoint] = field(default_factory=list)

    collided: bool = False
    show    : bool = True

    def movement(self):
        self.coords.x += int(self.Vx)
        self.coords.y -= int(self.Vy)

        self.collided = False

    def check_collision(self, particles: list[Particle]):
        if (
            self.coords.x - self.radius < 0        and self.Vx < 0 or
            self.coords.x + self.radius > ps.WIDTH and self.Vx > 0
        ):
            self.Vx *= -1
            return

        if (
            self.coords.y - self.radius < 0         and self.Vy > 0 or
            self.coords.y + self.radius > ps.HEIGHT and self.Vy < 0
        ):
            self.Vy *= -1
            return

        if not self.collided:
            for another in particles:
                if not self is another and self >> another:
                    _Vx = self.Vx
                    _Vy = self.Vy

                    self.Vx = (2*another.m*another.Vx + self.Vx*(self.m - another.m)) // (self.m + another.m)
                    self.Vy = (2*another.m*another.Vy + self.Vy*(self.m - another.m)) // (self.m + another.m)

                    another.Vx = (2*self.m*_Vx + _Vx*(another.m - self.m)) // (self.m + another.m)
                    another.Vy = (2*self.m*_Vy + _Vy*(another.m - self.m)) // (self.m + another.m)

                    self.coords.x += int(self.Vx * 1.1)
                    self.coords.y -= int(self.Vy * 1.1)

                    another.collided = True
                    break

    def __rshift__(self, another: Particle) -> float:
        distance = (
            (another.coords.x - self.coords.x)**2 +
            (another.coords.y - self.coords.y)**2
        )**.5

        if type(distance) != complex:
            if distance <= self.radius + another.radius:
                return True
            return False
        return True