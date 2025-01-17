"""nodes

Revision ID: 37692c1c9715
Revises: 97dd9311ab93
Create Date: 2023-03-27 02:49:00.118903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37692c1c9715'
down_revision = '97dd9311ab93'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256, collation='NOCASE'), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('api_port', sa.Integer(), nullable=False),
    sa.Column('certificate', sa.String(length=2048), nullable=False),
    sa.Column('status', sa.Enum('connected','connecting','error','disabled', name='nodestatus'), nullable=False),
    sa.Column('last_status_change', sa.DateTime(), nullable=True),
    sa.Column('message', sa.String(length=1024), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('uplink', sa.BigInteger(), nullable=True),
    sa.Column('downlink', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_nodes_id'), 'nodes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_nodes_id'), table_name='nodes')
    op.drop_table('nodes')
    # ### end Alembic commands ###
