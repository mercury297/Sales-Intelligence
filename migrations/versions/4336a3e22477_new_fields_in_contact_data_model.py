"""new fields in contact data model

Revision ID: 4336a3e22477
Revises: 9950342e4d0d
Create Date: 2019-06-27 15:58:24.194724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4336a3e22477'
down_revision = '9950342e4d0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('Campaigns_targetted', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Contact_Status', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Email_Valid', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Last_Targetted', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Linkedin_URL', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Mailing_City', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Mailing_Country', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Mailing_State', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('New_Lead_Source', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Phone', sa.Integer(), nullable=True))
    op.add_column('data', sa.Column('Products', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Region', sa.String(length=64), nullable=True))
    op.add_column('data', sa.Column('Services', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'Services')
    op.drop_column('data', 'Region')
    op.drop_column('data', 'Products')
    op.drop_column('data', 'Phone')
    op.drop_column('data', 'New_Lead_Source')
    op.drop_column('data', 'Mailing_State')
    op.drop_column('data', 'Mailing_Country')
    op.drop_column('data', 'Mailing_City')
    op.drop_column('data', 'Linkedin_URL')
    op.drop_column('data', 'Last_Targetted')
    op.drop_column('data', 'Email_Valid')
    op.drop_column('data', 'Contact_Status')
    op.drop_column('data', 'Campaigns_targetted')
    # ### end Alembic commands ###