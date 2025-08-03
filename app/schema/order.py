from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    items: List[OrderItemCreate]

class OrderRead(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str]
    customer_email: Optional[str]
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemRead]
