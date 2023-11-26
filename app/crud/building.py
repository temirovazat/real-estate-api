from typing import Any

from databases import Database

from app.crud.base import CRUDBase
from app.models import building
from app.schemas.building import BuildingIn, BuildingUpdate


class CRUDBuilding(CRUDBase[type(building), BuildingIn, BuildingUpdate]):
    async def get_by_name(self, db: Database, *, name: str) -> Any:
        return await db.fetch_one(self.model.select().where(self.model.c.name == name))


building = CRUDBuilding(building)
