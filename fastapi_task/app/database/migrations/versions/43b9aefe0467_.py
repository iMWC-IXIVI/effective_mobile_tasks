from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '43b9aefe0467'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('spimex_trading_results',
    sa.Column('id', sa.UUID(), nullable=False, comment='Уникальный идентификатор UUID'),
    sa.Column('date', sa.Date(), nullable=False, comment='Дата торгов'),
    sa.Column('oil_id', sa.String(length=50), nullable=False, comment='Идентификатор нефтяного продукта'),
    sa.Column('delivery_type_id', sa.String(length=255), nullable=False, comment='Тип поставки'),
    sa.Column('delivery_basis_id', sa.String(length=255), nullable=False, comment='Базис поставки'),
    sa.Column('volume', sa.DECIMAL(precision=18, scale=6), nullable=True, comment='Объем торгов'),
    sa.Column('total', sa.DECIMAL(precision=18, scale=6), nullable=True, comment='Общая сумма'),
    sa.Column('count', sa.Integer(), nullable=True, comment='Количество сделок'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_spimex_trading_results_date'), 'spimex_trading_results', ['date'], unique=False)
    op.create_index(op.f('ix_spimex_trading_results_delivery_basis_id'), 'spimex_trading_results', ['delivery_basis_id'], unique=False)
    op.create_index(op.f('ix_spimex_trading_results_delivery_type_id'), 'spimex_trading_results', ['delivery_type_id'], unique=False)
    op.create_index(op.f('ix_spimex_trading_results_oil_id'), 'spimex_trading_results', ['oil_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_spimex_trading_results_oil_id'), table_name='spimex_trading_results')
    op.drop_index(op.f('ix_spimex_trading_results_delivery_type_id'), table_name='spimex_trading_results')
    op.drop_index(op.f('ix_spimex_trading_results_delivery_basis_id'), table_name='spimex_trading_results')
    op.drop_index(op.f('ix_spimex_trading_results_date'), table_name='spimex_trading_results')
    op.drop_table('spimex_trading_results')
