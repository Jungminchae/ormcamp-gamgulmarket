"""change image field to JSONB

Revision ID: af5fae973efb
Revises: 4c1bdb2e7c96
Create Date: 2024-10-03 21:02:51.945038

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "af5fae973efb"
down_revision: Union[str, None] = "4c1bdb2e7c96"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("products", "image", new_column_name="images", type_=JSONB, postgresql_using="image::jsonb")


def downgrade() -> None:
    op.alter_column("products", "images", new_column_name="image", type_=sa.String(255), postgresql_using="images::text")
