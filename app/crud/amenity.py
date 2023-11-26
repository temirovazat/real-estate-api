from typing import Any

from databases import Database

from app.crud.base import CRUDBase
from app.models import amenity
from app.schemas.unit import AmenityIn, AmenityUpdate


class CRUDAmenity(CRUDBase[type(amenity), AmenityIn, AmenityUpdate]):
    async def get_by_name(self, db: Database, *, name: str) -> Any:
        return await db.fetch_one(self.model.select().where(self.model.c.name == name))


amenity = CRUDAmenity(amenity)
