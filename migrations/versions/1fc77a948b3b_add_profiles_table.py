"""add profiles table

Revision ID: 1fc77a948b3b
Revises: 34ec93dccf1a
Create Date: 2024-10-01 16:52:36.652782

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import HSTORE

# revision identifiers, used by Alembic.
revision: str = "1fc77a948b3b"
down_revision: Union[str, None] = "34ec93dccf1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("profile", HSTORE, nullable=True),
    )

    # user에 새로운 데이터가 생성되면 profile도 함께 생성
    op.execute("""
    CREATE OR REPLACE FUNCTION create_profile_on_user_insert()
    RETURNS TRIGGER AS $$
    DECLARE
        random_number TEXT;
    BEGIN
        -- 8자리 랜덤 숫자 생성 
        random_number := (floor(random() * 100000000)::int)::text;
        INSERT INTO profiles (user_id, profile)
        VALUES (NEW.id, hstore('nickname', '감귤' || random_number));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER user_insert_create_profile_trigger
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_profile_on_user_insert();
    """)


def downgrade() -> None:
    pass
