"""relationship user-category

Revision ID: cb7abe0663ae
Revises: e79efa67a678
Create Date: 2025-06-24 13:33:36.584155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb7abe0663ae'
down_revision = 'e79efa67a678'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_categories')
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_categories_user_id_users'), 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_categories_user_id_users'), type_='foreignkey')
        batch_op.drop_column('user_id')

    op.create_table('_alembic_tmp_categories',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type_category', sa.VARCHAR(length=50), nullable=False),
    sa.Column('user_login', sa.VARCHAR(length=50), nullable=False),
    sa.ForeignKeyConstraint(['user_login'], ['users.login'], name=op.f('fk_categories_user_login_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories')),
    sa.UniqueConstraint('type_category', name=op.f('uq_categories_type_category'))
    )
    # ### end Alembic commands ###
