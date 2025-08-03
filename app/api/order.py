from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select
from app.model.order import Order, OrderItem
from app.model.menu import MenuItem
from app.model.user import User
from app.schema.order import OrderCreate, OrderRead
from app.db.session import async_session
from app.core.security import get_current_admin

router = APIRouter()


# === ROUTES PUBLIQUES ===

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """Passer une commande - accessible à tous"""
    async with async_session() as session:
        # Vérifier que tous les items existent et sont disponibles
        total_amount = 0
        order_items_data = []

        for item_data in order_data.items:
            query = select(MenuItem).where(MenuItem.id == item_data.menu_item_id)
            result = await session.execute(query)
            menu_item = result.scalar_one_or_none()

            if not menu_item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Menu item {item_data.menu_item_id} not found"
                )

            if not menu_item.available:
                raise HTTPException(
                    status_code=400,
                    detail=f"Menu item '{menu_item.name}' is not available"
                )

            item_total = menu_item.price * item_data.quantity
            total_amount += item_total

            order_items_data.append({
                "menu_item_id": item_data.menu_item_id,
                "quantity": item_data.quantity,
                "unit_price": menu_item.price
            })

        # Créer la commande
        db_order = Order(
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            customer_email=order_data.customer_email,
            total_amount=total_amount
        )
        session.add(db_order)
        await session.flush()  # Pour obtenir l'ID

        # Créer les items de commande
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=db_order.id,
                **item_data
            )
            session.add(order_item)

        await session.commit()
        await session.refresh(db_order)

        # Recharger avec les items
        query = select(Order).where(Order.id == db_order.id)
        result = await session.execute(query)
        order_with_items = result.scalar_one()

        return order_with_items


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int):
    """Récupérer une commande par son ID - accessible à tous"""
    async with async_session() as session:
        query = select(Order).where(Order.id == order_id)
        result = await session.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order


# === ROUTES ADMIN ===

@router.get("/admin/all", response_model=List[OrderRead])
async def get_all_orders(current_admin: User = Depends(get_current_admin)):
    """Voir toutes les commandes - Admin seulement"""
    async with async_session() as session:
        query = select(Order).order_by(Order.created_at.desc())
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/admin/status/{status}", response_model=List[OrderRead])
async def get_orders_by_status(
        status: str,
        current_admin: User = Depends(get_current_admin)
):
    """Filtrer les commandes par statut - Admin seulement"""
    async with async_session() as session:
        query = select(Order).where(Order.status == status).order_by(Order.created_at.desc())
        result = await session.execute(query)
        return result.scalars().all()


@router.patch("/admin/{order_id}/status")
async def update_order_status(
        order_id: int,
        new_status: str,
        current_admin: User = Depends(get_current_admin)
):
    """Modifier le statut d'une commande - Admin seulement"""
    valid_statuses = ["pending", "confirmed", "preparing", "ready", "delivered", "cancelled"]

    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Valid statuses: {valid_statuses}"
        )

    async with async_session() as session:
        query = select(Order).where(Order.id == order_id)
        result = await session.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = new_status
        session.add(order)
        await session.commit()

        return {"message": f"Order status updated to {new_status}", "status": new_status}
