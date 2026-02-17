from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
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
        title = QLabel("ERP Pro")
        title.setStyleSheet("font-size: 32px; font-weight: 700;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Gestão empresarial offline com módulo fiscal integrado")
        subtitle.setStyleSheet("font-size: 14px; color: #475569;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("admin123")

        form = QFormLayout()
        form.addRow("Usuário", self.username_input)
        form.addRow("Senha", self.password_input)

        login_btn = QPushButton("Entrar no sistema")
        login_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: 700; padding: 8px;")
        login_btn.clicked.connect(self._handle_login)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(login_btn)

        card = QFrame()
        card.setMaximumWidth(460)
        card.setStyleSheet("QFrame { background-color: #f8fafc; border-radius: 12px; border: 1px solid #cbd5e1; padding: 14px;}")

        card_layout = QVBoxLayout()
        card_layout.addLayout(form)
        card_layout.addLayout(buttons)
        card.setLayout(card_layout)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        self.setLayout(layout)

    def _handle_login(self) -> None:
        if AuthService.authenticate(self.username_input.text(), self.password_input.text()):
            self.on_login_success()
            return

        QMessageBox.warning(self, "Falha no login", "Usuário ou senha inválidos.")
