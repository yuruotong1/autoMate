from typing import ClassVar

from pydantic import BaseModel


class TmpBaseModel(BaseModel):
    name: ClassVar[str] = "abc"
    description: str = "hello"


def test_model():
    t = TmpBaseModel(description="ddd")
    print(t.dict)
