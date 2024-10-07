"""add resignation_reason to users

Revision ID: 61debac3fb49
Revises: baf779dc76cb
Create Date: 2024-10-04 23:22:56.901655

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "61debac3fb49"
down_revision: Union[str, None] = "baf779dc76cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("resignation_reason", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "resignation_reason")
