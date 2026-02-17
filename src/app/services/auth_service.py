from sqlalchemy import select

from app.data.database import SessionLocal
from app.domain.models import User


class AuthService:
    @staticmethod
    def ensure_default_admin() -> None:
        with SessionLocal() as session:
            existing = session.scalar(select(User).where(User.username == "admin"))
            if existing:
                return
            session.add(User(username="admin", password="admin123", is_active=True))
            session.commit()

    @staticmethod
    def authenticate(username: str, password: str) -> bool:
        username = username.strip()
        password = password.strip()
        if not username or not password:
            return False

        with SessionLocal() as session:
            user = session.scalar(
                select(User).where(
                    User.username == username,
                    User.password == password,
                    User.is_active.is_(True),
                )
            )
            return user is not None
