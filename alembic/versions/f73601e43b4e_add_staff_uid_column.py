"""Add staff.uid column safely"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f73601e43b4e'
down_revision = None  # <-- set this to the previous migration ID in your project
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Just add the uid column
    op.add_column('staff', sa.Column('uid', sa.String(), unique=True, nullable=True))

def downgrade() -> None:
    # Remove uid if rolling back
    op.drop_column('staff', 'uid')
