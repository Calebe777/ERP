from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
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

from app.services.nfe_service import NFeImportError, NFeService


class FiscalWidget(QWidget):
    def __init__(self, on_data_changed=None) -> None:
        super().__init__()
        self.on_data_changed = on_data_changed
        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        title = QLabel("Módulo Fiscal - Importação de NF-e XML")
        title.setStyleSheet("font-size: 20px; font-weight: 700;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por número, chave, emissor ou CNPJ")

        search_btn = QPushButton("Pesquisar")
        search_btn.clicked.connect(self.refresh_table)

        import_btn = QPushButton("Importar XML")
        import_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: 700;")
        import_btn.clicked.connect(self.import_xml)

        top_actions = QHBoxLayout()
        top_actions.addWidget(self.search_input)
        top_actions.addWidget(search_btn)
        top_actions.addWidget(import_btn)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["Número", "Série", "Emissão", "Emissor", "CNPJ", "Itens", "Total", "Chave"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(top_actions)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def import_xml(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar NF-e", "", "XML Files (*.xml)")
        if not file_path:
            return

        try:
            invoice = NFeService.import_xml(file_path)
        except NFeImportError as exc:
            QMessageBox.warning(self, "Falha na importação", str(exc))
            return

        QMessageBox.information(
            self,
            "Importação concluída",
            f"NF-e {invoice.number}/{invoice.series} importada com sucesso.",
        )
        self.refresh_table()
        if self.on_data_changed:
            self.on_data_changed()

    def refresh_table(self) -> None:
        invoices = NFeService.list_invoices(self.search_input.text())
        self.table.setRowCount(len(invoices))

        for row, invoice in enumerate(invoices):
            issued_at = invoice.issued_at.strftime("%d/%m/%Y %H:%M") if invoice.issued_at else "-"
            self.table.setItem(row, 0, QTableWidgetItem(invoice.number))
            self.table.setItem(row, 1, QTableWidgetItem(invoice.series))
            self.table.setItem(row, 2, QTableWidgetItem(issued_at))
            self.table.setItem(row, 3, QTableWidgetItem(invoice.emitter_name))
            self.table.setItem(row, 4, QTableWidgetItem(invoice.emitter_cnpj))

            item_count = QTableWidgetItem(str(invoice.item_count))
            item_count.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, item_count)

            total_value = QTableWidgetItem(f"R$ {invoice.total_value:.2f}")
            total_value.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 6, total_value)

            self.table.setItem(row, 7, QTableWidgetItem(invoice.invoice_key))

        self.table.resizeColumnsToContents()
