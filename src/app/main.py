import sys

from PySide6.QtWidgets import QApplication

from app.data.database import Base, engine
from app.services.auth_service import AuthService
from app.ui.main_window import MainWindow


def bootstrap() -> None:
    Base.metadata.create_all(bind=engine)
    AuthService.ensure_default_admin()


def main() -> int:
    bootstrap()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
