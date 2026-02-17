from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.auth_service import AuthService


class LoginWidget(QWidget):
    def __init__(self, on_login_success) -> None:
        super().__init__()
        self.on_login_success = on_login_success
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("ERP - Login")

        title = QLabel("Login ERP Offline")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("admin123")

        form = QFormLayout()
        form.addRow("Usuário", self.username_input)
        form.addRow("Senha", self.password_input)

        login_btn = QPushButton("Entrar")
        login_btn.clicked.connect(self._handle_login)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(login_btn)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addStretch()

        self.setLayout(layout)

    def _handle_login(self) -> None:
        if AuthService.authenticate(self.username_input.text(), self.password_input.text()):
            self.on_login_success()
            return

        QMessageBox.warning(self, "Falha no login", "Usuário ou senha inválidos.")
