from PyQt5.QtWidgets import QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class PreviewWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.label)
        self.setWidgetResizable(True)
        self.setStyleSheet("border:1px solid #ccc; background:#f9f9f9;")
    def set_image(self, path):
        pix = QPixmap(path)
        if not pix.isNull():
            self.set_pixmap(pix)
    def set_pixmap(self, pixmap):
        if pixmap.isNull():
            return
        scaled = pixmap.scaled(self.viewport().size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled)
    def resizeEvent(self, event):
        if self.label.pixmap():
            pix = self.label.pixmap()
            scaled = pix.scaled(self.viewport().size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled)
        super().resizeEvent(event)
