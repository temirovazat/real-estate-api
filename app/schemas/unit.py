from typing import List, Optional

from app.schemas import BaseSchema


class AmenityIn(BaseSchema):
    name: str


class AmenityUpdate(AmenityIn):
    ...


class AmenityOut(AmenityIn):
    id: int
    name: str


class UnitIn(BaseSchema):
    description: Optional[str]
    price: float
    square: float
    bedrooms: int
    bathrooms: int
    building_id: int

    amenities: Optional[List[int]]


class UnitUpdate(UnitIn):
    price: Optional[float]
    square: Optional[float]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    building_id: Optional[int]


class UnitForm(BaseSchema):
    min_price: Optional[float] = 0
    max_price: Optional[float] = 10_000_000_000

    min_square: Optional[float] = 0
    max_square: Optional[float] = 100_000

    min_bedrooms: Optional[int] = 0
    max_bedrooms: Optional[int] = 100_000

    min_bathrooms: Optional[int] = 0
    max_bathrooms: Optional[int] = 100_000

    amenities: Optional[List[int]]


class UnitOut(UnitIn):
    id: int

    amenities: Optional[List[AmenityOut]]
