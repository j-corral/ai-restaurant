from sqlmodel import SQLModel, Field
from typing import Optional

class MenuItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    price: float
    category: str = "pizza"
    available: bool = True
    image_url: Optional[str] = None
