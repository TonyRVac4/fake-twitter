from alembic import command
from alembic.config import Config


def apply_head_migration() -> None:
    """Run head migration."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
