"""Initial migration

Revision ID: 001
Revises:
Create Date: 2026-01-09 23:59:00

"""
from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the tasks table
    op.create_table(
        'task',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for user_id, created_at, and status columns (T037 from tasks)
    op.create_index('idx_task_user_id', 'task', ['user_id'])
    op.create_index('idx_task_created_at', 'task', ['created_at'])
    op.create_index('idx_task_status', 'task', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_task_user_id', table_name='task')
    op.drop_index('idx_task_created_at', table_name='task')
    op.drop_index('idx_task_status', table_name='task')

    # Drop the tasks table
    op.drop_table('task')