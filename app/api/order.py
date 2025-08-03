from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select
from app.model.order import Order, OrderItem
from app.model.menu import MenuItem
from app.model.user import User
from app.schema.order import OrderCreate, OrderRead, OrderItemRead
from app.db.session import async_session
from app.core.security import get_current_admin

router = APIRouter()


# === ROUTES PUBLIQUES ===

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
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

        db_order = Order(
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            customer_email=order_data.customer_email,
            total_amount=total_amount
        )
        session.add(db_order)
        await session.flush()

        created_items = []
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=db_order.id,
                **item_data
            )
            session.add(order_item)
            created_items.append(order_item)

        await session.commit()

        return OrderRead(
            id=db_order.id,
            customer_name=db_order.customer_name,
            customer_phone=db_order.customer_phone,
            customer_email=db_order.customer_email,
            total_amount=db_order.total_amount,
            status=db_order.status,
            created_at=db_order.created_at,
            items=[
                OrderItemRead(
                    id=item.id,
                    menu_item_id=item.menu_item_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price
                ) for item in created_items
            ]
        )


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int):
    """Récupérer une commande par son ID"""
    async with async_session() as session:
        # Récupérer la commande
        order_query = select(Order).where(Order.id == order_id)
        order_result = await session.execute(order_query)
        order = order_result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Récupérer les items
        items_query = select(OrderItem).where(OrderItem.order_id == order_id)
        items_result = await session.execute(items_query)
        items = items_result.scalars().all()

        # Construire la réponse
        return OrderRead(
            id=order.id,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            customer_email=order.customer_email,
            total_amount=order.total_amount,
            status=order.status,
            created_at=order.created_at,
            items=[
                OrderItemRead(
                    id=item.id,
                    menu_item_id=item.menu_item_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price
                ) for item in items
            ]
        )


# === ROUTES ADMIN ===

@router.get("/admin/all", response_model=List[OrderRead])
async def get_all_orders(current_admin: User = Depends(get_current_admin)):
    """Voir toutes les commandes - Admin seulement"""
    async with async_session() as session:
        orders_query = select(Order).order_by(Order.created_at.desc())
        orders_result = await session.execute(orders_query)
        orders = orders_result.scalars().all()

        if not orders:
            return []

        order_ids = [order.id for order in orders]
        items_query = select(OrderItem).where(OrderItem.order_id.in_(order_ids))
        items_result = await session.execute(items_query)
        all_items = items_result.scalars().all()

        items_by_order = {}
        for item in all_items:
            if item.order_id not in items_by_order:
                items_by_order[item.order_id] = []
            items_by_order[item.order_id].append(item)

        orders_read = []
        for order in orders:
            order_items = items_by_order.get(order.id, [])
            orders_read.append(OrderRead(
                id=order.id,
                customer_name=order.customer_name,
                customer_phone=order.customer_phone,
                customer_email=order.customer_email,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                items=[
                    OrderItemRead(
                        id=item.id,
                        menu_item_id=item.menu_item_id,
                        quantity=item.quantity,
                        unit_price=item.unit_price
                    ) for item in order_items
                ]
            ))

        return orders_read


@router.get("/admin/status/{status}", response_model=List[OrderRead])
async def get_orders_by_status(
        status: str,
        current_admin: User = Depends(get_current_admin)
):
    """Filtrer les commandes par statut - Admin seulement"""
    async with async_session() as session:
        # Récupérer les commandes par statut
        orders_query = select(Order).where(Order.status == status).order_by(Order.created_at.desc())
        orders_result = await session.execute(orders_query)
        orders = orders_result.scalars().all()

        if not orders:
            return []

        order_ids = [order.id for order in orders]
        items_query = select(OrderItem).where(OrderItem.order_id.in_(order_ids))
        items_result = await session.execute(items_query)
        all_items = items_result.scalars().all()

        items_by_order = {}
        for item in all_items:
            if item.order_id not in items_by_order:
                items_by_order[item.order_id] = []
            items_by_order[item.order_id].append(item)

        orders_read = []
        for order in orders:
            order_items = items_by_order.get(order.id, [])
            orders_read.append(OrderRead(
                id=order.id,
                customer_name=order.customer_name,
                customer_phone=order.customer_phone,
                customer_email=order.customer_email,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                items=[
                    OrderItemRead(
                        id=item.id,
                        menu_item_id=item.menu_item_id,
                        quantity=item.quantity,
                        unit_price=item.unit_price
                    ) for item in order_items
                ]
            ))

        return orders_read


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
