from typing import Any, Optional

from databases import Database

from app.crud.base import CRUDBase
from app.models import agent
from app.schemas.developer import AgentIn, AgentUpdate


class CRUDAgent(CRUDBase[type(agent), AgentIn, AgentUpdate]):
    async def get_by_user_id(self, db: Database, *, user_id: int) -> Optional[Any]:
        return await db.fetch_one(
            self.model.select().where(self.model.c.user_id == user_id)
        )


agent = CRUDAgent(agent)
