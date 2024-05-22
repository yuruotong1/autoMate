from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QColor, QPolygon
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle


class StyledItemDelegate(QStyledItemDelegate):
    # 等腰三角形直角边长
    POLYGON = 6
    # 分割符粗细的一半
    HEIGHT = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        # 画原始的 item
        QStyledItemDelegate.paint(self, painter, option, index)
        drag_widget = option.styleObject
        from actions.action_list import ActionList
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
            painter.drawRect(0, rect.topLeft().y(), 6, rect.height())
            
        # 开始拖拽
        if is_drag:
            if index.row() == drag_widget.the_highlighted_row:
                painter.setBrush(QColor(66, 133, 244))
                # 绘制矩形
                q_rec = QRect(rect.bottomLeft().x(), rect.bottomLeft().y(),
                              rect.width(), self.HEIGHT)
                painter.drawRect(q_rec)
                # 绘制左上三角
                triangle_top_left = QPolygon([
                    QPoint(q_rec.topLeft().x(), q_rec.topLeft().y() + 1),
                    QPoint(q_rec.topLeft().x(), q_rec.topLeft().y() - self.POLYGON + 1),
                    QPoint(q_rec.topLeft().x() + self.POLYGON, q_rec.topLeft().y() + 1)
                ])
                # 绘制右上三角
                triangle_top_right = QPolygon([
                    QPoint(q_rec.topRight().x() + 1, q_rec.topRight().y() + 1),
                    QPoint(q_rec.topRight().x() + 1, q_rec.topRight().y() + 1 - self.POLYGON),
                    QPoint(q_rec.topRight().x() + 1 - self.POLYGON, q_rec.topRight().y() + 1)
                ])
                painter.drawPolygon(triangle_top_left)
                painter.drawPolygon(triangle_top_right)
            elif index.row() == drag_widget.the_highlighted_row + 1:
                painter.setBrush(QColor(66, 133, 244))
                # 绘制矩形
                q_rec = QRect(rect.topLeft().x(), rect.topLeft().y() - self.HEIGHT,
                              rect.width(), self.HEIGHT)
                painter.drawRect(q_rec)
                # 组装左下部分三角形
                triangle_bottom_left = QPolygon([
                    QPoint(q_rec.bottomLeft().x(), q_rec.bottomLeft().y()),
                    QPoint(q_rec.bottomLeft().x(), q_rec.bottomLeft().y() + self.POLYGON),
                    QPoint(q_rec.bottomLeft().x() + self.POLYGON, q_rec.bottomLeft().y())
                ])
                # 组装右下部分三角形
                triangle_bottom_right = QPolygon([
                    QPoint(q_rec.bottomRight().x() + 1, q_rec.bottomRight().y()),
                    QPoint(q_rec.bottomRight().x() + 1 - self.POLYGON, q_rec.bottomRight().y()),
                    QPoint(q_rec.bottomRight().x() + 1, q_rec.bottomRight().y() + self.POLYGON)
                ])
                painter.drawPolygon(triangle_bottom_left)
                painter.drawPolygon(triangle_bottom_right)
