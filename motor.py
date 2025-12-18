# arranca la app
from ui.main_window import KPIVision

from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
ventana = KPIVision()
ventana.show()
sys.exit(app.exec())
