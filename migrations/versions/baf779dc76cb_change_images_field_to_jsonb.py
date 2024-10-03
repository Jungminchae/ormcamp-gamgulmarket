"""change images field to JSONB[]

Revision ID: baf779dc76cb
Revises: af5fae973efb
Create Date: 2024-10-03 22:00:51.086676

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, ARRAY


# revision identifiers, used by Alembic.
revision: str = "baf779dc76cb"
down_revision: Union[str, None] = "af5fae973efb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "products", "images", new_column_name="image_urls", type_=ARRAY(JSONB), postgresql_using="ARRAY[images]::jsonb[]"
    )


def downgrade() -> None:
    op.alter_column("products", "image_urls", new_column_name="images", type_=JSONB, postgresql_using="image_urls::jsonb")
