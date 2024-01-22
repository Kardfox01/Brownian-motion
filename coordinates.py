from dataclasses import dataclass


@dataclass
class Coordinates:
    x: int
    y: int

    @property
    def get(self) -> tuple[int, int]:
        return self.x, self.y


@dataclass
class TrajectoryPoint:
    coords_start: tuple[int, int]
    coords_end  : tuple[int, int]
    color       : tuple[int, int, int]