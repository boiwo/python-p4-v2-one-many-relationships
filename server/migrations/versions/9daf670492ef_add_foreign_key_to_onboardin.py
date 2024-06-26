"""add foreign key to onboardin

Revision ID: 9daf670492ef
Revises: adc17ca6bbd4
Create Date: 2024-06-26 19:59:36.187051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9daf670492ef'
down_revision = 'adc17ca6bbd4'
branch_labels = None
depends_on = None


tmp_onboardings = "tmp_onboardings"
tmp_reviews = "tmp_reviews"

def upgrade():
    # Add new columns to onboardings table

    # Create a new reviews table with the employee_id foreign key constraint
    op.create_table(
        tmp_reviews,
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fk_reviews_employee_id_employees')
    )

    # Migrate data from old reviews table to new reviews table
    op.execute(f"INSERT INTO {tmp_reviews} (id, employee_id) SELECT id, employee_id FROM reviews")

    # Drop the old reviews table
    op.drop_table('reviews')

    # Rename the new reviews table to the original name
    op.rename_table(tmp_reviews, 'reviews')

def downgrade():
    # Create a temporary reviews table for the downgrade
    op.create_table(
        tmp_reviews,
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('employee_id', sa.Integer(), nullable=True),
    )

    # Migrate data from new reviews table back to old reviews table
    op.execute(f"INSERT INTO {tmp_reviews} (id, employee_id) SELECT id, employee_id FROM reviews")

    # Drop the new reviews table
    op.drop_table('reviews')

    # Rename the temporary reviews table to the original name
    op.rename_table(tmp_reviews, 'reviews')



    # ### end Alembic commands ###
