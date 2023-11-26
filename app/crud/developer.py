from typing import Any, List, Optional

from databases import Database

from app.crud.base import CRUDBase
from app.models import agent, developer
from app.schemas.developer import DeveloperIn, DeveloperUpdate


class CRUDDeveloper(CRUDBase[type(developer), DeveloperIn, DeveloperUpdate]):
    async def get_by_international_name(
        self, db: Database, *, international_name: str
    ) -> Optional[Any]:
        return await db.fetch_one(
            self.model.select().where(
                self.model.c.international_name == international_name
            )
        )

    async def get_agents(
        self, db: Database, *, model_id: int, skip: int = 0, limit: int = 100
    ) -> List[Any]:
        return await db.fetch_all(
            agent.select()
            .where(agent.c.developer_id == model_id)
            .offset(skip)
            .limit(limit)
        )


developer = CRUDDeveloper(developer)
