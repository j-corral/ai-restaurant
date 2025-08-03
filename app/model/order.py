from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    menu_item_id: int = Field(foreign_key="menuitem.id")
    quantity: int
    unit_price: float  # Prix au moment de la commande

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: float
    status: str = "pending"  # pending, confirmed, preparing, ready, delivered
    created_at: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem] = Relationship(back_populates="order")
