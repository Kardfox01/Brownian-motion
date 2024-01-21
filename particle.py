from __future__ import annotations
from dataclasses import dataclass, field

from coordinates import Coordinates, TrajectoryPoint
from parameters import SIDE


@dataclass
class Particle:
    uid       : int
    radius    : int
    m         : int
    Vᵪ        : int
    Vᵧ        : int
    coords    : Coordinates
    color     : tuple[int, int, int]
    trajectory: list[TrajectoryPoint] = field(default_factory=list)

    collided: bool = False

    def movement(self):
        self.coords.x += int(self.Vᵪ)
        self.coords.y -= int(self.Vᵧ)

        self.collided = False

    def check_collision(self, particles: list[Particle]):
        if (
            self.coords.x - self.radius < 0    and self.Vᵪ < 0 or
            self.coords.x + self.radius > SIDE and self.Vᵪ > 0
        ):
            self.Vᵪ *= -1
            self.coords.x += int(self.Vᵪ * 1.2)

        if (
            self.coords.y - self.radius < 0    and self.Vᵧ > 0 or
            self.coords.y + self.radius > SIDE and self.Vᵧ < 0
        ):
            self.Vᵧ *= -1
            self.coords.y -= int(self.Vᵧ * 1.2)

        for another in particles:
            if (
                self >> another <= self.radius + another.radius and
                not self is another and
                not self.collided
            ):
                _Vᵪ = self.Vᵪ
                _Vᵧ = self.Vᵧ

                self.Vᵪ = (2*another.m*another.Vᵪ + self.Vᵪ*(self.m - another.m)) // (self.m + another.m)
                self.Vᵧ = (2*another.m*another.Vᵧ + self.Vᵧ*(self.m - another.m)) // (self.m + another.m)

                another.Vᵪ = (2*self.m*_Vᵪ + _Vᵪ*(another.m - self.m)) // (self.m + another.m)
                another.Vᵧ = (2*self.m*_Vᵧ + _Vᵧ*(another.m - self.m)) // (self.m + another.m)

                self.coords.x += int(self.Vᵪ * 1.2)
                self.coords.y -= int(self.Vᵧ * 1.2)

                another.collided = True

    def __rshift__(self, another: Particle) -> float:
        distance = (
            (another.coords.x - self.coords.x)**2 + 
            (another.coords.y - self.coords.y)**2
        )**.5

        if type(distance) != complex:
            return distance
        return 0