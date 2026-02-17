from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
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
    def __init__(self) -> None:
        super().__init__()
        self.current_product_id: int | None = None
        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        title = QLabel("Cadastro de Produtos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

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

        form_box = QGroupBox("Dados do Produto")
        form_box.setLayout(form)

        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.save_product)
        new_btn = QPushButton("Novo")
        new_btn.clicked.connect(self.clear_form)
        delete_btn = QPushButton("Excluir")
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
        self.table.itemSelectionChanged.connect(self.load_selected_product)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(search_layout)
        layout.addWidget(form_box)
        layout.addLayout(action_layout)
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

    def refresh_table(self) -> None:
        products = ProductService.list_products(self.search_input.text())
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            code_item = QTableWidgetItem(product.code)
            code_item.setData(Qt.ItemDataRole.UserRole, product.id)
            self.table.setItem(row, 0, code_item)
            self.table.setItem(row, 1, QTableWidgetItem(product.description))
            self.table.setItem(row, 2, QTableWidgetItem(f"{product.price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(product.stock)))
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
