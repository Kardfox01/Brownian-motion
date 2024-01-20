from __future__ import annotations

from coordinates import Coordinates, dataclass


@dataclass
class Particle:
    radius  : int
    m       : int
    Vᵪ      : int
    Vᵧ      : int
    coords  : Coordinates
    color   : tuple[int, int, int] = (0, 0, 0)
    collided: bool                 = False

    def figure(self) -> tuple[tuple[int, int, int], tuple[int, int], int]:
        self.coords.x += int(self.Vᵪ)
        self.coords.y -= int(self.Vᵧ)

        self.collided = False

        return self.color, self.coords.get, self.radius

    def check_collision(self, particles: list[Particle], side: int):
        if (
            self.coords.x - self.radius < 0    and self.Vᵪ < 0 or
            self.coords.x + self.radius > side and self.Vᵪ > 0
        ):
            self.Vᵪ *= -1

        if (
            self.coords.y - self.radius < 0    and self.Vᵧ > 0 or
            self.coords.y + self.radius > side and self.Vᵧ < 0
        ):
            self.Vᵧ *= -1

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

                self.coords.x += int(self.Vᵪ)
                self.coords.y -= int(self.Vᵧ)

                another.collided = True

    def __rshift__(self, another: Particle) -> float:
        distance = (
            (another.coords.x - self.coords.x)**2 + 
            (another.coords.y - self.coords.y)**2
        )**.5

        if type(distance) != complex:
            return distance
        return 0