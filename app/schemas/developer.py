from typing import Optional

from app.schemas import BaseSchema


class DeveloperIn(BaseSchema):
    international_name: str
    website: Optional[str] = ""
    phone_number: Optional[str] = ""


class DeveloperOut(DeveloperIn):
    id: int


class DeveloperUpdate(DeveloperIn):
    international_name: Optional[str]


class AgentIn(BaseSchema):
    developer_id: int
    user_id: int


class AgentOut(AgentIn):
    id: int


class AgentUpdate(BaseSchema):
    developer_id: Optional[int]
