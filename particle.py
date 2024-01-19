from dataclasses import dataclass
from coordinates import Coordinates
from sectors import Sector


@dataclass
class Particle:
    size       : int
    mass       : int
    v          : int
    sector     : Sector
    coordinates: Coordinates
    color      : tuple[int, int, int] = (0, 0, 0)

    @property
    def get(self) -> tuple[tuple[int, int, int], tuple[int, int], int]:
        return self.color, self.coordinates.get, self.size