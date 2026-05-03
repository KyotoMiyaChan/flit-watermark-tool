from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox,
                             QSpinBox, QDoubleSpinBox, QGridLayout,
                             QColorDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from localization import tr
from core.font_manager import scan_fonts

class AdjustmentPanel(QWidget):
    param_changed = pyqtSignal()
    browse_clicked = pyqtSignal()
    generate_clicked = pyqtSignal()
    copy_clicked = pyqtSignal()
    open_clicked = pyqtSignal()
    color_changed = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fonts = scan_fonts()
        self.font_names = sorted(self.fonts.keys())
        self._updating = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12,12,12,12)
        layout.setSpacing(8)

        img_row = QHBoxLayout()
        self.img_edit = QLineEdit()
        self.img_edit.setReadOnly(True)
        self.img_edit.setPlaceholderText(tr("placeholder_img"))
        self.img_edit.setMaximumWidth(180)
        self.btn_browse = QPushButton(tr("btn_browse"))
        self.btn_browse.clicked.connect(self.browse_clicked.emit)
        img_row.addWidget(self.img_edit, 0)
        img_row.addWidget(self.btn_browse)
        img_row.addStretch()
        layout.addLayout(img_row)

        grid = QGridLayout()
        grid.setVerticalSpacing(8)
        grid.setHorizontalSpacing(10)

        self.lbl_text = QLabel(tr("label_text"))
        self.lbl_text.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_font = QLabel(tr("label_font"))
        self.lbl_font.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_scale = QLabel(tr("label_scale"))
        self.lbl_scale.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_size = QLabel(tr("label_size"))
        self.lbl_size.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_opacity = QLabel(tr("label_opacity"))
        self.lbl_opacity.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_rotation = QLabel(tr("label_rotation"))
        self.lbl_rotation.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.text_edit = QLineEdit("PREVIEW")
        self.text_edit.setMaximumWidth(160)
        self.text_edit.textChanged.connect(self.emit_param_changed)

        self.font_combo = QComboBox()
        self.font_combo.addItems(self.font_names)
        if self.font_names:
            default = "Helvetica" if "Helvetica" in self.font_names else self.font_names[0]
            self.font_combo.setCurrentText(default)
        self.font_combo.setMaximumWidth(160)
        self.font_combo.currentTextChanged.connect(self.emit_param_changed)

        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["100%", "50%", "20%"])
        self.scale_combo.setMaximumWidth(100)
        self.scale_combo.currentIndexChanged.connect(self.emit_param_changed)

        self.size_spin = QDoubleSpinBox()
        self.size_spin.setRange(4, 800)
        self.size_spin.setDecimals(1)
        self.size_spin.setSingleStep(0.5)
        self.size_spin.setValue(36)
        self.size_spin.setSuffix(" pt")
        self.size_spin.setMaximumWidth(90)
        self.size_spin.valueChanged.connect(self.emit_param_changed)

        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(0, 100)
        self.opacity_spin.setValue(50)
        self.opacity_spin.setSuffix(" %")
        self.opacity_spin.setMaximumWidth(90)
        self.opacity_spin.valueChanged.connect(self.emit_param_changed)

        self.rot_spin = QSpinBox()
        self.rot_spin.setRange(-180, 180)
        self.rot_spin.setValue(0)
        self.rot_spin.setSuffix(" °")
        self.rot_spin.setMaximumWidth(90)
        self.rot_spin.valueChanged.connect(self.emit_param_changed)

        self.btn_color = QPushButton("")
        self.btn_color.setMaximumWidth(40)
        self.btn_color.setToolTip(tr("tooltip_pick_color"))
        self.btn_color.clicked.connect(self.pick_color)
        self.btn_color.setStyleSheet("background-color: rgb(255,255,255); border:1px solid #555;")
        self.current_color = (255, 255, 255)

        grid.addWidget(self.lbl_text, 0, 0)
        grid.addWidget(self.text_edit, 0, 1)
        grid.addWidget(self.lbl_font, 0, 2)
        grid.addWidget(self.font_combo, 0, 3)

        grid.addWidget(self.lbl_scale, 1, 0)
        grid.addWidget(self.scale_combo, 1, 1)
        grid.addWidget(self.lbl_size, 1, 2)
        grid.addWidget(self.size_spin, 1, 3)

        grid.addWidget(self.lbl_opacity, 2, 0)
        grid.addWidget(self.opacity_spin, 2, 1)
        grid.addWidget(self.lbl_rotation, 2, 2)
        grid.addWidget(self.rot_spin, 2, 3)

        color_row = QHBoxLayout()
        color_row.addWidget(QLabel(tr("label_color")))
        color_row.addWidget(self.btn_color)
        color_row.addStretch()
        grid.addLayout(color_row, 3, 0, 1, 4)

        layout.addLayout(grid)

        btn_bar = QHBoxLayout()
        btn_bar.setSpacing(8)
        self.btn_gen = QPushButton(tr("btn_generate"))
        self.btn_gen.setStyleSheet("background:#4CAF50; color:white; font-weight:bold;")
        self.btn_gen.clicked.connect(self.generate_clicked.emit)
        self.btn_copy = QPushButton(tr("btn_copy"))
        self.btn_copy.clicked.connect(self.copy_clicked.emit)
        self.btn_open = QPushButton(tr("btn_open"))
        self.btn_open.clicked.connect(self.open_clicked.emit)
        btn_bar.addWidget(self.btn_gen)
        btn_bar.addWidget(self.btn_copy)
        btn_bar.addWidget(self.btn_open)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.status_label = QLabel(tr("status_ready"))
        layout.addWidget(self.status_label)
        layout.addStretch()

    def emit_param_changed(self):
        if not self._updating:
            self.param_changed.emit()

    def pick_color(self):
        col = QColorDialog.getColor(initial=QColor(*self.current_color), parent=self, title=tr("dialog_pick_color"))
        if col.isValid():
            self.current_color = (col.red(), col.green(), col.blue())
            self.btn_color.setStyleSheet(f"background-color: rgb({self.current_color[0]},{self.current_color[1]},{self.current_color[2]}); border:1px solid #555;")
            self.color_changed.emit(self.current_color)
            self.emit_param_changed()

    def retranslate_ui(self):
        self.img_edit.setPlaceholderText(tr("placeholder_img"))
        self.btn_browse.setText(tr("btn_browse"))
        self.lbl_text.setText(tr("label_text"))
        self.lbl_font.setText(tr("label_font"))
        self.lbl_scale.setText(tr("label_scale"))
        self.lbl_size.setText(tr("label_size"))
        self.lbl_opacity.setText(tr("label_opacity"))
        self.lbl_rotation.setText(tr("label_rotation"))
        self.btn_gen.setText(tr("btn_generate"))
        self.btn_copy.setText(tr("btn_copy"))
        self.btn_open.setText(tr("btn_open"))
        self.btn_color.setToolTip(tr("tooltip_pick_color"))

    def set_text(self, text):
        self._updating = True
        self.text_edit.setText(text)
        self._updating = False

    def set_font_size(self, size):
        self._updating = True
        self.size_spin.setValue(size)
        self._updating = False

    def set_rotation(self, angle):
        self._updating = True
        self.rot_spin.setValue(int(angle))
        self._updating = False

    def set_opacity(self, opacity):
        self._updating = True
        self.opacity_spin.setValue(opacity)
        self._updating = False

    def set_color_button(self, rgb):
        self.current_color = rgb
        self.btn_color.setStyleSheet(f"background-color: rgb({rgb[0]},{rgb[1]},{rgb[2]}); border:1px solid #555;")

    def set_img_path_text(self, text): self.img_edit.setText(text)
    def set_status(self, text): self.status_label.setText(text)

    def get_text(self): return self.text_edit.text().strip() or "PREVIEW"
    def get_font_path(self):
        name = self.font_combo.currentText()
        return self.fonts.get(name, "/System/Library/Fonts/Helvetica.ttc")
    def get_scale(self):
        scale_map = {"100%": 1.0, "50%": 0.5, "20%": 0.2}
        return scale_map[self.scale_combo.currentText()]
    def get_font_size(self): return self.size_spin.value()
    def get_opacity(self): return self.opacity_spin.value()
    def get_rotation(self): return self.rot_spin.value()
    def get_color(self): return self.current_color
    def suggest_font_size(self, img_width, img_height):
        suggested = max(8, min(200, int(min(img_width, img_height) * 0.05)))
        self.size_spin.setValue(suggested)
