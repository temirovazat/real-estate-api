from typing import Optional

from app.schemas import BaseSchema


class BuildingIn(BaseSchema):
    name: Optional[str]
    description: Optional[str]
    latitude: float
    longitude: float
    building_class: str
    postcode: str
    number_of_units: int
    number_of_floors: int
    year_built: str


class BuildingUpdate(BuildingIn):
    latitude: Optional[float]
    longitude: Optional[float]
    building_class: Optional[str]
    postcode: Optional[str]
    longitude: Optional[str]
    number_of_units: Optional[int]
    number_of_floors: Optional[int]
    year_built: Optional[str]


class BuildingOut(BuildingIn):
    id: int
