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
        CREATE OR REPLACE FUNCTION "public"._pgtrigger_should_ignore(
            trigger_name NAME
        )
        RETURNS BOOLEAN AS $$
            DECLARE
                _pgtrigger_ignore TEXT[];
                _result BOOLEAN;
            BEGIN
                BEGIN
                    SELECT INTO _pgtrigger_ignore
                        CURRENT_SETTING('pgtrigger.ignore');
                    EXCEPTION WHEN OTHERS THEN
                END;
                IF _pgtrigger_ignore IS NOT NULL THEN
                    SELECT trigger_name = ANY(_pgtrigger_ignore)
                    INTO _result;
                    RETURN _result;
                ELSE
                    RETURN FALSE;
                END IF;
            END;
        $$ LANGUAGE plpgsql;
        """)

    # 활성화된 사용자에 대해서만 트리거가 실행되도록 함
    op.execute("""
        CREATE OR REPLACE FUNCTION pgtrigger_soft_delete_78625()
        RETURNS TRIGGER AS $$
            BEGIN
                IF ("public"._pgtrigger_should_ignore(TG_NAME) IS TRUE) THEN
                    IF (TG_OP = 'DELETE') THEN
                        RETURN OLD;
                    ELSE
                        RETURN NEW;
                    END IF;
                END IF;
                IF (OLD.is_removable IS TRUE) THEN
                    RETURN OLD;  
                END IF;
                UPDATE "users" SET is_active = FALSE, is_removable = TRUE, deleted_at = now()  WHERE "id" = OLD."id" AND is_removable = FALSE; RETURN NULL;
            END;
        $$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS pgtrigger_soft_delete_78625 ON "users";
        CREATE TRIGGER pgtrigger_soft_delete_78625
            BEFORE DELETE ON "users"
            
            FOR EACH ROW 
            EXECUTE PROCEDURE pgtrigger_soft_delete_78625();

        COMMENT ON TRIGGER pgtrigger_soft_delete_78625 ON "users" IS '6f7f1bbad00e7d3167219959189d38b83e5f7668';
        """)


def downgrade() -> None:
    op.drop_table("users")
    op.execute("DROP FUNCTION soft_delete_user")
    op.execute("DROP FUNCTION hard_delete_user")
    op.execute("DROP TRIGGER soft_delete_trigger ON users")
    op.execute("DROP TRIGGER hard_delete_trigger ON users")


# TODO: 트리거 문제부터 해결하면 됨
