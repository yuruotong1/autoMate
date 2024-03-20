from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QColor, QPolygon
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle


class StyledItemDelegate(QStyledItemDelegate):
    # 等腰三角形直角边长
    POLYGON = 4
    # 分割符粗细的一半
    HEIGHT = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        # 画原始的 item
        QStyledItemDelegate.paint(self, painter, option, index)
        drag_widget = option.styleObject
        from pages.edit_action_list_view import ActionList
        if not isinstance(drag_widget, ActionList):
            raise TypeError("option.styleObject must be an instance of ActionListView")
        is_drag = drag_widget.is_drag
        # 被选中 item 的边框
        rect = option.rect
        # 画背景
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        # 选中时的样式
        if option.state & QStyle.StateFlag.State_Selected:
            # 选中时，最左边会出现小块块
            painter.setBrush(QColor(0, 0, 255))
            painter.drawRect(rect.topLeft().x() - 3, rect.topLeft().y(), 8, rect.height())
        # 开始拖拽
        if is_drag and index.row() == drag_widget.the_highlighted_row:
            # 组装上部分
            painter.setBrush(QColor(66, 133, 244))
            # 绘制三角
            triangle_polygon_bottom_left = QPolygon([
                QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - (self.POLYGON + self.HEIGHT) + 1),
                QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - self.HEIGHT),
                QPoint(rect.bottomLeft().x() + self.POLYGON, rect.bottomLeft().y() - self.HEIGHT + 1)
            ])

            triangle_polygon_bottom_right = QPolygon([
                QPoint(rect.bottomRight().x() + 1,
                       rect.bottomRight().y() - (self.POLYGON + self.HEIGHT) + 1),
                QPoint(rect.bottomRight().x() + 1, rect.bottomRight().y() - self.HEIGHT + 1),
                QPoint(rect.bottomRight().x() - self.POLYGON + 1,
                       rect.bottomRight().y() - self.HEIGHT + 1)
            ])
            painter.drawPolygon(triangle_polygon_bottom_left)
            painter.drawPolygon(triangle_polygon_bottom_right)
            q_rec = QRect(rect.bottomLeft().x(), rect.bottomLeft().y(),
                          rect.width(), self.HEIGHT + 3)
            # 绘制矩形
            painter.drawRect(q_rec)
            # 组装下部分三角形
            triangle_polygon_top_left = QPolygon([
                QPoint(q_rec.bottomLeft().x(), q_rec.bottomLeft().y()),
                QPoint(q_rec.bottomLeft().x(), q_rec.bottomLeft().y() + self.HEIGHT),
                QPoint(q_rec.bottomLeft().x() + self.POLYGON, q_rec.bottomLeft().y())
            ])

            triangle_polygon_top_right = QPolygon([
                QPoint(q_rec.bottomRight().x(), q_rec.bottomRight().y()),
                QPoint(q_rec.bottomRight().x() - self.POLYGON, q_rec.topRight().y()),
                QPoint(q_rec.topRight().x(), q_rec.topRight().y() + self.HEIGHT)
            ])
            painter.drawPolygon(triangle_polygon_top_left)
            painter.drawPolygon(triangle_polygon_top_right)
