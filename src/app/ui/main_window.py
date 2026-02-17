from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.ui.login_widget import LoginWidget
from app.ui.products_widget import ProductsWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ERP Desktop Offline")
        self.resize(950, 650)

        self.stack = QStackedWidget()
        self.login_widget = LoginWidget(self._on_login_success)
        self.products_widget = ProductsWidget()

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.products_widget)
        self.setCentralWidget(self.stack)

    def _on_login_success(self) -> None:
        self.stack.setCurrentWidget(self.products_widget)
