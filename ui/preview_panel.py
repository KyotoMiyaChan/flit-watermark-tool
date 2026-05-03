from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from .interactive_preview import InteractivePreviewWidget
from localization import tr

class PreviewPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.title_label = QLabel(tr("label_preview"))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        self.preview = InteractivePreviewWidget()
        layout.addWidget(self.preview)
    def retranslate_ui(self):
        self.title_label.setText(tr("label_preview"))
    def set_image(self, path):
        from PyQt5.QtGui import QPixmap
        self.preview.set_background(QPixmap(path))
    def set_pixmap(self, pixmap):
        self.preview.set_background(pixmap)
    def get_preview_widget(self):
        return self.preview
