#!/usr/bin/env python3
import sys, os, subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QFrame, QMessageBox, QFileDialog,
                             QMenuBar, QAction, QMainWindow)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage, QPixmap, QColor
from core import WatermarkParams, apply_watermark
from core.watermark_element import WatermarkElement
from ui.adjustment_panel import AdjustmentPanel
from ui.preview_panel import PreviewPanel
from ui.footer_bar import FooterBar
from localization import set_language, tr
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QApplication.setStyle('macOS')
        self.original_image = None
        self.generated_path = None
        self.main_element = WatermarkElement()

        self.setWindowTitle(tr("app_title"))
        self.resize(900, 550)
        self.setup_menu()

        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)

        main_row = QHBoxLayout()
        main_row.setContentsMargins(0,0,0,0)

        self.adjust = AdjustmentPanel()
        self.preview_panel = PreviewPanel()
        self.preview = self.preview_panel.get_preview_widget()
        self.footer = FooterBar()

        main_row.addWidget(self.adjust, 1)
        main_row.addWidget(self.preview_panel, 2)
        outer.addLayout(main_row, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        outer.addWidget(line)
        outer.addWidget(self.footer)

        self.adjust.browse_clicked.connect(self.browse_image)
        self.adjust.generate_clicked.connect(self.generate)
        self.adjust.copy_clicked.connect(self.copy_to_clipboard)
        self.adjust.open_clicked.connect(self.open_folder)
        self.adjust.param_changed.connect(self.on_adjust_changed)
        self.preview.itemSelected.connect(self.on_item_selected)

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu(tr("menu_file"))
        open_action = QAction(tr("menu_open"), self)
        open_action.triggered.connect(self.browse_image)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        exit_action = QAction(tr("menu_exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        lang_menu = menubar.addMenu(tr("menu_language"))
        zh_action = QAction(tr("menu_lang_zh"), self)
        zh_action.triggered.connect(lambda: self.switch_language("zh"))
        lang_menu.addAction(zh_action)
        en_action = QAction(tr("menu_lang_en"), self)
        en_action.triggered.connect(lambda: self.switch_language("en"))
        lang_menu.addAction(en_action)

        help_menu = menubar.addMenu(tr("menu_help"))
        about_action = QAction(tr("menu_about"), self)
        about_action.triggered.connect(lambda: QMessageBox.about(self, tr("menu_about"), tr("about_text")))
        help_menu.addAction(about_action)

    def switch_language(self, lang):
        set_language(lang)
        self.setWindowTitle(tr("app_title"))
        self.menuBar().clear()
        self.setup_menu()
        self.adjust.retranslate_ui()
        self.footer.retranslate_ui()
        self.preview_panel.retranslate_ui()

    def browse_image(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("menu_open"), "",
                                              "图片 (*.jpg *.jpeg *.png *.bmp *.tiff *.webp)")
        if not path: return
        try:
            self.original_image = Image.open(path)
            self.adjust.set_img_path_text(os.path.basename(path))
            w, h = self.original_image.size
            self.adjust.suggest_font_size(w, h)

            pixmap = QPixmap(path)
            self.preview.set_background(pixmap)
            self.preview.clear_text_items()

            font_path = self.adjust.get_font_path()
            self.main_element = WatermarkElement(
                text=self.adjust.get_text(),
                font_path=font_path,
                font_size=self.adjust.get_font_size(),
                opacity=self.adjust.get_opacity(),
                rotation=self.adjust.get_rotation(),
                color=self.adjust.get_color(),
                pos_x=w/2,
                pos_y=h/2,
                scale=1.0
            )

            item = self.preview.add_text_item(
                self.main_element.text,
                pos=QPointF(self.main_element.pos_x, self.main_element.pos_y),
                font_size=self.main_element.font_size,
                color=QColor(*self.main_element.color),
                font_path=font_path
            )
            item.set_rotation(self.main_element.rotation)
            self.preview.apply_to_item(item,
                                       opacity=int(self.main_element.opacity*255/100),
                                       color=self.main_element.color)
        except Exception as e:
            QMessageBox.critical(self, "错误", tr("status_open_fail", e))

    def on_adjust_changed(self):
        if not self.original_image: return
        font_path = self.adjust.get_font_path()
        item = self.preview.get_selected_item()
        if not item:
            items = self.preview._text_items
            if items: item = items[0]
        if item:
            item.set_text(self.adjust.get_text())
            item.set_font_size(self.adjust.get_font_size())
            item.set_rotation(self.adjust.get_rotation())
            self.preview.apply_to_item(item,
                                       opacity=int(self.adjust.get_opacity()*255/100),
                                       color=self.adjust.get_color(),
                                       font_path=font_path)

    def on_item_selected(self, item):
        params = self.preview.get_current_item_params()
        if not params: return
        self.adjust.set_text(params["text"])
        self.adjust.set_font_size(params["font_size"])
        self.adjust.set_rotation(params["rotation"])
        self.adjust.set_opacity(int(params["opacity"]*100/255))
        self.adjust.set_color_button(params["color_rgb"])

    def generate(self):
        if self.original_image is None:
            QMessageBox.critical(self, "错误", tr("status_invalid"))
            return
        font_path = self.adjust.get_font_path()
        item = self.preview.get_selected_item()
        if not item:
            items = self.preview._text_items
            if items: item = items[0]
        if not item:
            QMessageBox.critical(self, "错误", "没有水印文本项")
            return

        text = item.text()
        font_size = item.font().pointSizeF()
        opacity = int(item.brush().color().alpha() * 100 / 255)
        rotation = item.rotation()
        scale = self.adjust.get_scale()
        color_rgb = (
            item.brush().color().red(),
            item.brush().color().green(),
            item.brush().color().blue()
        )
        pos_x = item.x() + item.boundingRect().width() / 2
        pos_y = item.y() + item.boundingRect().height() / 2

        params = WatermarkParams(
            text=text,
            font_path=font_path,
            font_size=font_size,
            opacity=opacity,
            rotation=rotation,
            mode="single",
            scale=scale,
            pos_x=pos_x,
            pos_y=pos_y,
            color=color_rgb
        )
        try:
            watermarked = apply_watermark(self.original_image.copy(), params)
            out = "preview.jpg"
            watermarked.save(out, format="JPEG", quality=85)
            self.generated_path = out
            self.adjust.set_status(tr("status_saved", out))
        except Exception as e:
            QMessageBox.critical(self, "错误", tr("status_gen_fail", e))

    def copy_to_clipboard(self):
        if not self.generated_path: return
        subprocess.run(["osascript", "-e",
            f'set the clipboard to (read (POSIX file "{os.path.abspath(self.generated_path)}") as JPEG picture)'])
        self.adjust.set_status(tr("status_copied"))

    def open_folder(self):
        folder = os.path.dirname(self.generated_path) if self.generated_path else os.getcwd()
        subprocess.Popen(["open", folder])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
