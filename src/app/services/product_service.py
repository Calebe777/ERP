from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from app.data.database import SessionLocal
from app.domain.models import Product


@dataclass
class ProductInput:
    code: str
    description: str
    price: float
    stock: int
    is_active: bool


class ProductValidationError(Exception):
    pass


class ProductService:
    @staticmethod
    def validate(payload: ProductInput) -> None:
        if not payload.code.strip():
            raise ProductValidationError("Código é obrigatório.")
        if not payload.description.strip():
            raise ProductValidationError("Descrição é obrigatória.")
        if payload.price < 0:
            raise ProductValidationError("Preço deve ser maior ou igual a zero.")
        if payload.stock < 0:
            raise ProductValidationError("Estoque deve ser maior ou igual a zero.")

    @staticmethod
    def list_products(search: str = "") -> list[Product]:
        with SessionLocal() as session:
            stmt = select(Product)
            if search.strip():
                term = f"%{search.strip()}%"
                stmt = stmt.where(or_(Product.code.like(term), Product.description.like(term)))
            stmt = stmt.order_by(Product.code.asc())
            return list(session.scalars(stmt))

    @staticmethod
    def create_product(payload: ProductInput) -> None:
        ProductService.validate(payload)
        with SessionLocal() as session:
            session.add(
                Product(
                    code=payload.code.strip(),
                    description=payload.description.strip(),
                    price=payload.price,
                    stock=payload.stock,
                    is_active=payload.is_active,
                )
            )
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise ProductValidationError("Código já cadastrado.") from exc

    @staticmethod
    def update_product(product_id: int, payload: ProductInput) -> None:
        ProductService.validate(payload)
        with SessionLocal() as session:
            product = session.get(Product, product_id)
            if not product:
                raise ProductValidationError("Produto não encontrado.")
            product.code = payload.code.strip()
            product.description = payload.description.strip()
            product.price = payload.price
            product.stock = payload.stock
            product.is_active = payload.is_active
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise ProductValidationError("Código já cadastrado.") from exc

    @staticmethod
    def delete_product(product_id: int) -> None:
        with SessionLocal() as session:
            product = session.get(Product, product_id)
            if not product:
                raise ProductValidationError("Produto não encontrado.")
            session.delete(product)
            session.commit()
