"""add measurements

Revision ID: b2f211ed78bd
Revises:
Create Date: 2024-02-14 23:24:51.280006

"""

# stdlib
from typing import Sequence, Union

# thirdparty
import sqlalchemy as sa

# project
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2f211ed78bd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "measurement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("temp", sa.Integer(), nullable=False),
        sa.Column("humidity", sa.Integer(), nullable=False),
        sa.Column("pressure", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("measurement")
    # ### end Alembic commands ###
