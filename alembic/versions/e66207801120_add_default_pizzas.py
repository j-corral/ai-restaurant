"""Add default pizzas

Revision ID: e66207801120
Revises: f793e5b7ebc9
Create Date: 2025-08-03 14:34:23.284238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Float, Boolean


# revision identifiers, used by Alembic.
revision: str = 'e66207801120'
down_revision: Union[str, Sequence[str], None] = 'f793e5b7ebc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    menu_table = table(
        'menuitem',
        column('name', String),
        column('description', String),
        column('price', Float),
        column('category', String),
        column('available', Boolean),
        column('image_url', String),
    )

    # Insérer plusieurs items par défaut
    op.bulk_insert(
        menu_table,
        [
            {
                'name': 'Pizza Margherita',
                'description': 'Tomate, mozzarella, basilic frais',
                'price': 10.50,
                'category': 'pizza',
                'available': True,
                'image_url': None,
            },
            {
                'name': 'Pizza Marinara',
                'description': 'Tomate, huile d\'olive, origan',
                'price': 8.00,
                'category': 'pizza',
                'available': True,
                'image_url': None,
            },
            {
                'name': 'Coca-Cola',
                'description': 'Boisson gazeuse 33cl',
                'price': 2.50,
                'category': 'boisson',
                'available': True,
                'image_url': None,
            }
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
            DELETE FROM menuitem 
            WHERE name IN ('Pizza Margherita', 'Pizza Marinara', 'Coca-Cola')
            AND price IN (10.50, 8.00, 2.50)
        """)
