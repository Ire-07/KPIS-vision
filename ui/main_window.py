# interfaz gráfica KPI Vision
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QFileDialog,
    QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QTabWidget
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


# ==================================================
# Ventana Principal
# ==================================================
class KPIVision(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KPI Vision – Dashboard Profesional de KPIs")
        self.setMinimumSize(1300, 850)

        self.df = None
        self.crear_interfaz()

    # ==================================================
    # Crear Interfaz Gráfica
    # ==================================================
    def crear_interfaz(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QHBoxLayout(widget_central)

        # -------------------------
        # Panel lateral
        # -------------------------
        panel_lateral = QVBoxLayout()

        titulo = QLabel("📊 KPI Vision")
        titulo.setStyleSheet("font-size:22px; font-weight:bold;")

        subtitulo = QLabel("Dashboard automático de Ventas y Leads")
        subtitulo.setStyleSheet("color: gray;")

        self.btn_cargar = QPushButton("📂 Cargar CSV")
        self.btn_cargar.clicked.connect(self.cargar_csv)

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Ventas", "Leads"])

        self.btn_generar = QPushButton("🚀 Generar Dashboard")
        self.btn_generar.clicked.connect(self.generar_dashboard)

        panel_lateral.addWidget(titulo)
        panel_lateral.addWidget(subtitulo)
        panel_lateral.addSpacing(20)
        panel_lateral.addWidget(self.btn_cargar)
        panel_lateral.addWidget(QLabel("Tipo de datos"))
        panel_lateral.addWidget(self.combo_tipo)
        panel_lateral.addSpacing(10)
        panel_lateral.addWidget(self.btn_generar)
        panel_lateral.addStretch()

        # -------------------------
        # Tabs de Dashboard
        # -------------------------
        self.tabs = QTabWidget()

        self.tab_kpis = QWebEngineView()
        self.tab_graficos = QWebEngineView()

        self.tabs.addTab(self.tab_kpis, "📊 KPIs")
        self.tabs.addTab(self.tab_graficos, "📈 Gráficos")

        layout_principal.addLayout(panel_lateral, 1)
        layout_principal.addWidget(self.tabs, 4)

    # ==================================================
    # Cargar CSV
    # ==================================================
    def cargar_csv(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo CSV", "", "CSV (*.csv)"
        )
        if archivo:
            try:
                self.df = pd.read_csv(archivo, encoding="latin-1")

                # Normalizar columnas
                self.df.columns = (
                    self.df.columns.str.lower()
                    .str.strip()
                    .str.replace(" ", "_")
                )

                QMessageBox.information(self, "OK", "CSV cargado correctamente")

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    # ==================================================
    # Generar Dashboard
    # ==================================================
    def generar_dashboard(self):
        if self.df is None:
            QMessageBox.warning(self, "Atención", "Primero cargue un CSV")
            return

        tipo = self.combo_tipo.currentText()

        try:
            if tipo == "Ventas":
                fig_kpis = self.kpis_ventas()
                fig_graficos = self.graficos_ventas()
            else:
                fig_kpis = self.kpis_leads()
                fig_graficos = self.graficos_leads()

            self.tab_kpis.setHtml(
                fig_kpis.to_html(include_plotlyjs="cdn"),
                QUrl("")
            )
            self.tab_graficos.setHtml(
                fig_graficos.to_html(include_plotlyjs="cdn"),
                QUrl("")
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ==================================================
    # KPIs Ventas
    # ==================================================
    def kpis_ventas(self):
        total = self.df["monto"].sum()
        promedio = self.df["monto"].mean()
        cantidad = len(self.df)

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number",
            value=total,
            title={"text": "💰 Total Ventas"},
            domain={"row": 0, "column": 0}
        ))

        fig.add_trace(go.Indicator(
            mode="number",
            value=round(promedio, 2),
            title={"text": "🎯 Ticket Promedio"},
            domain={"row": 0, "column": 1}
        ))

        fig.add_trace(go.Indicator(
            mode="number",
            value=cantidad,
            title={"text": "📦 Cantidad Ventas"},
            domain={"row": 0, "column": 2}
        ))

        fig.update_layout(
            grid={"rows": 1, "columns": 3, "pattern": "independent"},
            height=300
        )

        return fig

    # ==================================================
    # KPIs Leads
    # ==================================================
    def kpis_leads(self):
        total = len(self.df)
        ganados = len(self.df[self.df["estado"] == "ganado"])
        conversion = (ganados / total) * 100 if total > 0 else 0

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number",
            value=total,
            title={"text": "👥 Total Leads"},
            domain={"row": 0, "column": 0}
        ))

        fig.add_trace(go.Indicator(
            mode="number",
            value=ganados,
            title={"text": "✅ Leads Ganados"},
            domain={"row": 0, "column": 1}
        ))

        fig.add_trace(go.Indicator(
            mode="number",
            value=round(conversion, 2),
            title={"text": "% Conversión"},
            domain={"row": 0, "column": 2}
        ))

        fig.update_layout(
            grid={"rows": 1, "columns": 3, "pattern": "independent"},
            height=300
        )

        return fig

    # ==================================================
    # Gráficos Ventas
    # ==================================================
    def graficos_ventas(self):
        fig = px.line(
            self.df,
            x="fecha",
            y="monto",
            title="📈 Evolución de Ventas"
        )
        return fig

    # ==================================================
    # Gráficos Leads
    # ==================================================
    def graficos_leads(self):
        fig = px.pie(
            self.df,
            names="estado",
            title="🎯 Distribución de Leads"
        )
        return fig


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = KPIVision()
    ventana.show()
    sys.exit(app.exec())
