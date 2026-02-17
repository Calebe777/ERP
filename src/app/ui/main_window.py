from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app.ui.dashboard_widget import DashboardWidget
from app.ui.fiscal_widget import FiscalWidget
from app.ui.login_widget import LoginWidget
from app.ui.products_widget import ProductsWidget


class ErpWorkspace(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.pages = QStackedWidget()
        self.dashboard = DashboardWidget()
        self.products = ProductsWidget(on_data_changed=self.dashboard.refresh_metrics)
        self.fiscal = FiscalWidget(on_data_changed=self.dashboard.refresh_metrics)

        self.pages.addWidget(self.dashboard)
        self.pages.addWidget(self.products)
        self.pages.addWidget(self.fiscal)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(self.pages)
        self.setLayout(layout)

    def show_dashboard(self) -> None:
        self.dashboard.refresh_metrics()
        self.pages.setCurrentWidget(self.dashboard)

    def show_products(self) -> None:
        self.products.refresh_table()
        self.pages.setCurrentWidget(self.products)

    def show_fiscal(self) -> None:
        self.fiscal.refresh_table()
        self.pages.setCurrentWidget(self.fiscal)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ERP Pro - Gestão Empresarial")
        self.resize(1280, 760)

        self.stack = QStackedWidget()
        self.login_widget = LoginWidget(self._on_login_success)
        self.workspace = ErpWorkspace()

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.workspace)
        self.setCentralWidget(self.stack)

        self._build_toolbar()
        self._build_status_bar()
        self._set_logged_out_mode()

    def _build_toolbar(self) -> None:
        self.toolbar = QToolBar("Módulos")
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; padding: 8px; }")

        self.dashboard_action = QAction("Painel", self)
        self.dashboard_action.triggered.connect(self.workspace.show_dashboard)

        self.products_action = QAction("Produtos", self)
        self.products_action.triggered.connect(self.workspace.show_products)

        self.fiscal_action = QAction("Fiscal (NF-e)", self)
        self.fiscal_action.triggered.connect(self.workspace.show_fiscal)

        self.report_action = QAction("Resumo", self)
        self.report_action.triggered.connect(self._show_summary)

        self.toolbar.addAction(self.dashboard_action)
        self.toolbar.addAction(self.products_action)
        self.toolbar.addAction(self.fiscal_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.report_action)

        self.addToolBar(self.toolbar)

    def _build_status_bar(self) -> None:
        status = QStatusBar()
        status.addPermanentWidget(QLabel("Versão 1.0.0"))
        self.setStatusBar(status)

    def _set_logged_out_mode(self) -> None:
        self.toolbar.hide()
        self.statusBar().showMessage("Faça login para acessar os módulos")

    def _set_logged_in_mode(self) -> None:
        self.toolbar.show()
        self.statusBar().showMessage("Usuário autenticado")

    def _on_login_success(self) -> None:
        self.stack.setCurrentWidget(self.workspace)
        self.workspace.show_dashboard()
        self._set_logged_in_mode()

    def _show_summary(self) -> None:
        report = self.workspace.dashboard
        report.refresh_metrics()
        self.workspace.show_dashboard()
        QMessageBox.information(self, "Resumo", "Painel atualizado com os indicadores mais recentes.")
