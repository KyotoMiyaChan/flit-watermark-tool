from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from localization import tr

REPO_URL = "https://github.com/KyotoMiyaChan/cover-preview-generator"

class FooterBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(4)
        self.copyright_lbl = QLabel(tr("footer_copyright"))
        self.copyright_lbl.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.copyright_lbl)
        self.repo_link = QLabel(f"<a href='{REPO_URL}' style='color: #2a7ae2; text-decoration: none;'>{tr('footer_repo')}</a>")
        self.repo_link.setOpenExternalLinks(True)
        self.repo_link.setStyleSheet("font-size: 11px;")
        layout.addWidget(self.repo_link)
        layout.addStretch()
        self.star_lbl = QLabel(tr("footer_star"))
        self.star_lbl.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.star_lbl)
    def retranslate_ui(self):
        self.copyright_lbl.setText(tr("footer_copyright"))
        self.repo_link.setText(f"<a href='{REPO_URL}' style='color: #2a7ae2; text-decoration: none;'>{tr('footer_repo')}</a>")
        self.star_lbl.setText(tr("footer_star"))
