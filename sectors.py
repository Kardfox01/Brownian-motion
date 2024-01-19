from typing import Self
from coordinates import Coordinates


class Sector:
    def __init__(
        self,
        bottom_corner: Coordinates,
        top_corner   : Coordinates,
        uid          : int
    ):
        self.bottom_corner: Coordinates = bottom_corner
        self.top_corner   : Coordinates = top_corner
        self.uid          : int         = uid

    def __eq__(self, other_sector: Self) -> bool:
        return self.uid == other_sector.uid

    def __contains__(self, coordinates: Coordinates) -> bool:
        x, y = coordinates.get
        if self.bottom_corner.x <= x and self.bottom_corner.y <= y:
            if self.top_corner.x >= x and self.top_corner.y >= y:
                return True
        return False

    def __repr__(self):
        return f"Sector(uid={self.uid})"


class Sectors:
    def __init__(self, N: int, side: int):
        self.sectors: list[Sector] = []

        shift = side // N
        uid = 0
        for i in range(N):
            for ii in range(N):
                self.sectors.append(
                    Sector(
                        Coordinates(i * shift, ii * shift),
                        Coordinates(i * shift + shift, ii * shift + shift),
                        uid
                    )
                )
                uid += 1

    def where(self, coordinates: Coordinates) -> Sector:
        for sector in self.sectors:
            if coordinates in sector:
                return sector
        raise Exception(f"Я не знаю, где эта частица с координатами {coordinates}")