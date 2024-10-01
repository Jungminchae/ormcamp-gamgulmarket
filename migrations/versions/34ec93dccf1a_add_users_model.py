"""add users model

Revision ID: 34ec93dccf1a
Revises:
Create Date: 2024-10-01 16:00:02.517834

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "34ec93dccf1a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    User 모델 생성
    id, email, password, is_active, is_superuser, created_at, updated_at, deleted_at 필드 생성
    : id는 자동으로 1씩 증가
    : email이 username 대신 사용됨
    : password는 bcrypt로 암호화하여 저장 될 것임
    : deleted_at은 soft delete를 위한 필드로 삭제 시간을 저장함
    : is_removable 필드는 완전 hard delete가 가능한지 여부를 결정함
    : 삭제 요청이 오면 is_active를 False로 변경하고 deleted_at에 삭제 시간을 업데이트하는 PostgreSQL 트리거를 생성
    """
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_superuser", sa.Boolean, default=False),
        sa.Column("is_removable", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION soft_delete_user()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.is_active := FALSE;
        NEW.deleted_at := now();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # 활성화된 사용자에 대해서만 트리거가 실행되도록 함
    op.execute("""
    CREATE TRIGGER soft_delete_trigger
    BEFORE DELETE ON users
    FOR EACH ROW
    WHEN (OLD.is_active = TRUE)  
    EXECUTE FUNCTION soft_delete_user();
    """)

    # 하드 딜리트가 가능한 사용자에 대해서만 작동 가능한 트리거
    op.execute("""
    CREATE OR REPLACE FUNCTION hard_delete_user()
    RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM users WHERE id = OLD.id;
        RETURN NULL;  
    END;
    $$ LANGUAGE plpgsql;
    """)

    # is_active가 False이고 is_removable이 True인 사용자에 대해서만 트리거가 실행되도록 함
    op.execute("""
    CREATE TRIGGER hard_delete_trigger
    BEFORE DELETE ON users
    FOR EACH ROW
    WHEN (OLD.is_active = FALSE and OLD.is_removable = TRUE)  
    EXECUTE FUNCTION hard_delete_user();
    """)


def downgrade() -> None:
    op.drop_table("users")
    op.execute("DROP FUNCTION soft_delete_user")
    op.execute("DROP FUNCTION hard_delete_user")
    op.execute("DROP TRIGGER soft_delete_trigger ON users")
    op.execute("DROP TRIGGER hard_delete_trigger ON users")
