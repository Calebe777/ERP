"""add invoices table

Revision ID: 0002_add_invoices
Revises: 0001_initial
Create Date: 2026-02-17 00:30:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_add_invoices"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_key", sa.String(length=44), nullable=False),
        sa.Column("number", sa.String(length=20), nullable=False),
        sa.Column("series", sa.String(length=10), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=True),
        sa.Column("emitter_name", sa.String(length=255), nullable=False),
        sa.Column("emitter_cnpj", sa.String(length=18), nullable=False),
        sa.Column("total_value", sa.Float(), nullable=False),
        sa.Column("item_count", sa.Integer(), nullable=False),
        sa.Column("source_xml_path", sa.String(length=1024), nullable=False),
        sa.Column("imported_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_invoices_id"), "invoices", ["id"], unique=False)
    op.create_index(op.f("ix_invoices_invoice_key"), "invoices", ["invoice_key"], unique=False)
    op.create_index(op.f("ix_invoices_number"), "invoices", ["number"], unique=False)
    op.create_unique_constraint("uq_invoices_invoice_key", "invoices", ["invoice_key"])


def downgrade() -> None:
    op.drop_constraint("uq_invoices_invoice_key", "invoices", type_="unique")
    op.drop_index(op.f("ix_invoices_number"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_invoice_key"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_id"), table_name="invoices")
    op.drop_table("invoices")
