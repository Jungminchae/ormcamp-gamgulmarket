"""enable pg_trgm extension

Revision ID: 5ce89968916e
Revises: 61debac3fb49
Create Date: 2024-10-08 15:01:00.889348

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5ce89968916e"
down_revision: Union[str, None] = "61debac3fb49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.create_index(
        "ix_products_name_trgm", "products", ["name"], postgresql_using="gin", postgresql_ops={"name": "gin_trgm_ops"}
    )

    op.create_index(
        "ix_products_description_trgm",
        "products",
        ["description"],
        postgresql_using="gin",
        postgresql_ops={"description": "gin_trgm_ops"},
    )


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
    op.drop_index("ix_products_name_trgm", table_name="products")
    op.drop_index("ix_products_description_trgm", table_name="products")
