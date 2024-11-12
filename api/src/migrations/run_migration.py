import os
from alembic.config import Config
from alembic import command

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def apply_head_migration() -> None:
    """Run head migration."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
