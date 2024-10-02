"""add product table

Revision ID: 4c1bdb2e7c96
Revises: 1fc77a948b3b
Create Date: 2024-10-02 23:21:58.960094

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c1bdb2e7c96"
down_revision: Union[str, None] = "1fc77a948b3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("image", sa.String(255), nullable=True),
        sa.Column("citrus_variety", sa.String(255), nullable=True),
        sa.Column("cultivation_region", sa.String(50), nullable=True),
        sa.Column("harvest_time", sa.String(50), nullable=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("products")
