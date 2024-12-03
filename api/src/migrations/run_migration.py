import os

from alembic import command
from alembic.config import Config

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def apply_head_migration() -> None:
    """Run head migration."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    apply_head_migration()
