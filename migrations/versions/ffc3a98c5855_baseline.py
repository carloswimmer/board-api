"""baseline

Revision ID: ffc3a98c5855
Revises:
Create Date: 2026-04-25 11:43:42.009334

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = 'ffc3a98c5855'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
