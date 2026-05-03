from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                             QGraphicsSimpleTextItem, QGraphicsTextItem, QGraphicsItem)
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt5.QtGui import QPixmap, QFont, QColor, QBrush, QFontDatabase

class WatermarkSimpleItem(QGraphicsSimpleTextItem):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFlags(QGraphicsItem.ItemIsMovable |
                     QGraphicsItem.ItemIsSelectable |
                     QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(QBrush(Qt.white))
        self.setFont(QFont("Helvetica", 36))
        self._font_id = -1

    def set_text(self, text):
        self.setText(text)

    def set_font_size(self, size):
        font = self.font()
        font.setPointSizeF(size)
        self.setFont(font)

    def set_rotation(self, angle):
        self.setRotation(angle)

    def set_scale(self, scale):
        self.setScale(scale)

    def set_font_path(self, font_path):
        if not font_path:
            return
        prev_font = self.font()
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                family = families[0]
                new_font = QFont(family)
                new_font.setPointSizeF(prev_font.pointSizeF())
                self.setFont(new_font)
                if self._font_id != -1:
                    QFontDatabase.removeApplicationFont(self._font_id)
                self._font_id = font_id

    def itemChange(self, change, value):
        if change == self.ItemPositionHasChanged:
            scenerect = self.scene().sceneRect() if self.scene() else QRectF()
            if not scenerect.isNull():
                br = self.boundingRect()
                new_x = value.x() if isinstance(value, QPointF) else value.toPointF().x()
                new_y = value.y() if isinstance(value, QPointF) else value.toPointF().y()
                new_x = max(scenerect.left(), new_x)
                new_y = max(scenerect.top(), new_y)
                right_limit = scenerect.right() - br.width() * self.scale()
                bottom_limit = scenerect.bottom() - br.height() * self.scale()
                new_x = min(new_x, right_limit)
                new_y = min(new_y, bottom_limit)
                return QPointF(new_x, new_y)
        return super().itemChange(change, value)


class InteractivePreviewWidget(QGraphicsView):
    itemSelected = pyqtSignal(object)
    itemDeselected = pyqtSignal()
    requestUpdateAdjustment = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(self.renderHints())
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(0)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._bg_item = QGraphicsPixmapItem()
        self._scene.addItem(self._bg_item)
        self._text_items = []
        self._current_item = None
        self._editing_item = None

        self._scene.selectionChanged.connect(self._on_scene_selection_changed)
        self._scene.focusItemChanged.connect(self._on_focus_item_changed)

    def set_background(self, pixmap: QPixmap):
        if pixmap.isNull():
            return
        self._bg_item.setPixmap(pixmap)
        rect = QRectF(pixmap.rect())
        self._scene.setSceneRect(rect)
        self.fitInView(rect, Qt.KeepAspectRatio)

    def add_text_item(self, text="Text", pos=QPointF(100,100), font_size=36, color=Qt.white, font_path=None):
        item = WatermarkSimpleItem(text)
        item.setPos(pos)
        item.set_font_size(font_size)
        item.setBrush(QBrush(QColor(*color) if isinstance(color, tuple) else color))
        if font_path:
            item.set_font_path(font_path)
        self._scene.addItem(item)
        self._text_items.append(item)
        return item

    def get_selected_item(self):
        sel = self._scene.selectedItems()
        for it in sel:
            if isinstance(it, WatermarkSimpleItem):
                return it
        return None

    def _on_scene_selection_changed(self):
        sel = self._scene.selectedItems()
        item = None
        for it in sel:
            if isinstance(it, WatermarkSimpleItem):
                item = it
                break
        if item:
            self._current_item = item
            self.itemSelected.emit(item)
            self.requestUpdateAdjustment.emit(item)
        else:
            self._current_item = None
            self.itemDeselected.emit()

    def clear_text_items(self):
        for item in self._text_items:
            self._scene.removeItem(item)
        self._text_items.clear()
        self._current_item = None

    def get_current_item_params(self):
        item = self.get_selected_item()
        if not item:
            return None
        brush = item.brush()
        color = brush.color()
        return {
            "text": item.text(),
            "x": item.x(),
            "y": item.y(),
            "font_size": item.font().pointSizeF(),
            "rotation": item.rotation(),
            "scale": item.scale(),
            "opacity": color.alpha(),
            "color_rgb": (color.red(), color.green(), color.blue())
        }

    def apply_to_item(self, item, text=None, font_size=None, rotation=None, scale=None, opacity=None, color=None, font_path=None):
        if not item:
            return
        if text is not None:
            item.set_text(text)
        if font_size is not None:
            item.set_font_size(font_size)
        if rotation is not None:
            item.set_rotation(rotation)
        if scale is not None:
            item.set_scale(scale)
        if font_path is not None:
            item.set_font_path(font_path)
        if opacity is not None or color is not None:
            current_color = item.brush().color()
            r, g, b = color if color else (current_color.red(), current_color.green(), current_color.blue())
            a = opacity if opacity is not None else current_color.alpha()
            item.setBrush(QBrush(QColor(r, g, b, a)))

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, WatermarkSimpleItem):
            self._start_editing(item)
        else:
            super().mouseDoubleClickEvent(event)

    def _start_editing(self, simple_item):
        if self._editing_item:
            self._finish_editing()
        edit = QGraphicsTextItem(simple_item.text())
        edit.setPos(simple_item.pos())
        edit.setRotation(simple_item.rotation())
        edit.setScale(simple_item.scale())
        edit.setFont(simple_item.font())
        color = simple_item.brush().color()
        edit.setDefaultTextColor(color)
        self._scene.addItem(edit)
        simple_item.setVisible(False)
        self._editing_item = edit
        edit.setTextInteractionFlags(Qt.TextEditorInteraction)
        edit.setFocus()

    def _on_focus_item_changed(self, new_item, old_item, reason):
        if old_item and old_item == self._editing_item:
            self._finish_editing()

    def _finish_editing(self):
        if not self._editing_item:
            return
        edit = self._editing_item
        self._editing_item = None
        simple = None
        for item in self._text_items:
            if isinstance(item, WatermarkSimpleItem) and not item.isVisible():
                simple = item
                break
        if simple and edit:
            simple.set_text(edit.toPlainText())
            simple.setPos(edit.pos())
            simple.setRotation(edit.rotation())
            simple.setScale(edit.scale())
            color = edit.defaultTextColor()
            simple.setBrush(QBrush(color))
            simple.setVisible(True)
            simple.setSelected(True)
        self._scene.removeItem(edit)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self._editing_item:
                self._finish_editing()
                return
        super().keyPressEvent(event)
