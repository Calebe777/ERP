from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.product_service import ProductInput, ProductService, ProductValidationError


class ProductsWidget(QWidget):
    def __init__(self, on_data_changed=None) -> None:
        super().__init__()
        self.on_data_changed = on_data_changed
        self.current_product_id: int | None = None
        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        title = QLabel("Produtos")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por código ou descrição")

        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.refresh_table)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        self.code_input = QLineEdit()
        self.description_input = QLineEdit()
        self.price_input = QLineEdit("0.00")
        self.stock_input = QLineEdit("0")
        self.active_input = QCheckBox("Ativo")
        self.active_input.setChecked(True)

        form = QFormLayout()
        form.addRow("Código", self.code_input)
        form.addRow("Descrição", self.description_input)
        form.addRow("Preço", self.price_input)
        form.addRow("Estoque", self.stock_input)
        form.addRow("Status", self.active_input)

        form_box = QGroupBox("Cadastro")
        form_box.setLayout(form)

        save_btn = QPushButton("Salvar")
        save_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: 700;")
        save_btn.clicked.connect(self.save_product)

        new_btn = QPushButton("Novo")
        new_btn.clicked.connect(self.clear_form)

        delete_btn = QPushButton("Excluir")
        delete_btn.setStyleSheet("background-color: #b91c1c; color: white;")
        delete_btn.clicked.connect(self.delete_product)

        action_layout = QHBoxLayout()
        action_layout.addWidget(save_btn)
        action_layout.addWidget(new_btn)
        action_layout.addWidget(delete_btn)
        action_layout.addStretch()

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Código", "Descrição", "Preço", "Estoque", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.load_selected_product)

        card = QFrame()
        card.setStyleSheet("QFrame { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }")
        card_layout = QVBoxLayout()
        card_layout.addLayout(search_layout)
        card_layout.addWidget(form_box)
        card_layout.addLayout(action_layout)
        card.setLayout(card_layout)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(card)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def _payload_from_form(self) -> ProductInput:
        try:
            price = float(self.price_input.text().replace(",", "."))
        except ValueError as exc:
            raise ProductValidationError("Preço inválido.") from exc
        try:
            stock = int(self.stock_input.text())
        except ValueError as exc:
            raise ProductValidationError("Estoque inválido.") from exc

        return ProductInput(
            code=self.code_input.text(),
            description=self.description_input.text(),
            price=price,
            stock=stock,
            is_active=self.active_input.isChecked(),
        )

    def save_product(self) -> None:
        try:
            payload = self._payload_from_form()
            if self.current_product_id is None:
                ProductService.create_product(payload)
            else:
                ProductService.update_product(self.current_product_id, payload)
        except ProductValidationError as exc:
            QMessageBox.warning(self, "Validação", str(exc))
            return

        self.clear_form()
        self.refresh_table()
        if self.on_data_changed:
            self.on_data_changed()

    def refresh_table(self) -> None:
        products = ProductService.list_products(self.search_input.text())
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            code_item = QTableWidgetItem(product.code)
            code_item.setData(Qt.ItemDataRole.UserRole, product.id)
            self.table.setItem(row, 0, code_item)
            self.table.setItem(row, 1, QTableWidgetItem(product.description))

            price_item = QTableWidgetItem(f"{product.price:.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 2, price_item)

            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, stock_item)

            self.table.setItem(row, 4, QTableWidgetItem("Ativo" if product.is_active else "Inativo"))

        self.table.resizeColumnsToContents()

    def load_selected_product(self) -> None:
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        code_item = self.table.item(row, 0)
        self.current_product_id = code_item.data(Qt.ItemDataRole.UserRole)

        self.code_input.setText(self.table.item(row, 0).text())
        self.description_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text())
        self.stock_input.setText(self.table.item(row, 3).text())
        self.active_input.setChecked(self.table.item(row, 4).text() == "Ativo")

    def clear_form(self) -> None:
        self.current_product_id = None
        self.code_input.clear()
        self.description_input.clear()
        self.price_input.setText("0.00")
        self.stock_input.setText("0")
        self.active_input.setChecked(True)

    def delete_product(self) -> None:
        if self.current_product_id is None:
            QMessageBox.warning(self, "Excluir", "Selecione um produto para excluir.")
            return

        answer = QMessageBox.question(self, "Excluir", "Deseja realmente excluir este produto?")
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            ProductService.delete_product(self.current_product_id)
        except ProductValidationError as exc:
            QMessageBox.warning(self, "Erro", str(exc))
            return

        self.clear_form()
        self.refresh_table()
        if self.on_data_changed:
            self.on_data_changed()
