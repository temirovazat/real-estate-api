# flake8: noqa
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


from .building import *
from .developer import *
from .message import *
from .token import *
from .unit import *
from .user import *
