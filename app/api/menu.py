from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select
from app.model.menu import MenuItem
from app.model.user import User
from app.schema.menu import MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.db.session import async_session
from app.core.security import get_current_admin

router = APIRouter()


# === ROUTES PUBLIQUES ===

@router.get("/", response_model=List[MenuItemRead])
async def get_menu():
    """Voir le menu - accessible à tous"""
    async with async_session() as session:
        query = select(MenuItem).where(MenuItem.available == True)
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/categories")
async def get_categories():
    """Obtenir les catégories disponibles"""
    async with async_session() as session:
        query = select(MenuItem.category).distinct()
        result = await session.execute(query)
        categories = result.scalars().all()
        return {"categories": categories}


@router.get("/category/{category}", response_model=List[MenuItemRead])
async def get_menu_by_category(category: str):
    """Voir le menu par catégorie"""
    async with async_session() as session:
        query = select(MenuItem).where(
            MenuItem.category == category,
            MenuItem.available == True
        )
        result = await session.execute(query)
        return result.scalars().all()


# === ROUTES ADMIN ===

@router.get("/admin/all", response_model=List[MenuItemRead])
async def get_all_menu_items(current_admin: User = Depends(get_current_admin)):
    """Voir tous les items du menu (y compris non disponibles) - Admin seulement"""
    async with async_session() as session:
        query = select(MenuItem)
        result = await session.execute(query)
        return result.scalars().all()


@router.post("/admin/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
async def create_menu_item(
        item: MenuItemCreate,
        current_admin: User = Depends(get_current_admin)
):
    """Créer un nouvel item du menu - Admin seulement"""
    async with async_session() as session:
        db_item = MenuItem(**item.dict())
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item


@router.get("/admin/{item_id}", response_model=MenuItemRead)
async def get_menu_item(
        item_id: int,
        current_admin: User = Depends(get_current_admin)
):
    """Récupérer un item spécifique - Admin seulement"""
    async with async_session() as session:
        query = select(MenuItem).where(MenuItem.id == item_id)
        result = await session.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item


@router.put("/admin/{item_id}", response_model=MenuItemRead)
async def update_menu_item(
        item_id: int,
        item_update: MenuItemUpdate,
        current_admin: User = Depends(get_current_admin)
):
    """Modifier un item du menu - Admin seulement"""
    async with async_session() as session:
        query = select(MenuItem).where(MenuItem.id == item_id)
        result = await session.execute(query)
        db_item = result.scalar_one_or_none()

        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Mise à jour uniquement des champs fournis
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item


@router.delete("/admin/{item_id}")
async def delete_menu_item(
        item_id: int,
        current_admin: User = Depends(get_current_admin)
):
    """Supprimer un item du menu - Admin seulement"""
    async with async_session() as session:
        query = select(MenuItem).where(MenuItem.id == item_id)
        result = await session.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        await session.delete(item)
        await session.commit()
        return {"message": "Item deleted successfully"}


@router.patch("/admin/{item_id}/toggle-availability")
async def toggle_item_availability(
        item_id: int,
        current_admin: User = Depends(get_current_admin)
):
    """Activer/désactiver la disponibilité d'un item - Admin seulement"""
    async with async_session() as session:
        query = select(MenuItem).where(MenuItem.id == item_id)
        result = await session.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        item.available = not item.available
        session.add(item)
        await session.commit()
        await session.refresh(item)

        status_text = "disponible" if item.available else "indisponible"
        return {"message": f"Item maintenant {status_text}", "available": item.available}
