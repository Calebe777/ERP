from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from app.services.nfe_service import NFeService
from app.services.product_service import ProductService


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, color: str) -> None:
        super().__init__()
        self.setObjectName("metricCard")
        self.setStyleSheet(
            f"""
            QFrame#metricCard {{
                border-radius: 10px;
                background-color: {color};
                color: white;
                padding: 12px;
            }}
            """
        )

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; font-weight: 600;")

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 28px; font-weight: 700;")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        self.setLayout(layout)


class DashboardWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.cards_layout = QGridLayout()
        self._build_ui()
        self.refresh_metrics()

    def _build_ui(self) -> None:
        title = QLabel("Painel de Gestão")
        title.setStyleSheet("font-size: 26px; font-weight: 700;")

        subtitle = QLabel("Visão rápida das operações de produtos e notas fiscais eletrônicas")
        subtitle.setStyleSheet("font-size: 14px; color: #4b5563;")

        container = QVBoxLayout()
        container.addWidget(title)
        container.addWidget(subtitle)
        container.addSpacing(12)
        container.addLayout(self.cards_layout)
        container.addStretch()

        self.setLayout(container)

    def refresh_metrics(self) -> None:
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        products = ProductService.list_products()
        report = NFeService.report_summary()

        cards = [
            MetricCard("Produtos cadastrados", str(len(products)), "#2563eb"),
            MetricCard("Produtos ativos", str(sum(1 for item in products if item.is_active)), "#059669"),
            MetricCard("NF-e importadas", str(report["total_notes"]), "#7c3aed"),
            MetricCard("Itens em NF-e", str(report["total_items"]), "#ea580c"),
            MetricCard("Valor total NF-e", f"R$ {report['total_value']:.2f}", "#be123c"),
        ]

        for index, card in enumerate(cards):
            row = index // 3
            column = index % 3
            self.cards_layout.addWidget(card, row, column, Qt.AlignmentFlag.AlignTop)
