from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPolygon
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem


class StyledItemDelegate(QStyledItemDelegate):
    # 等腰三角形直角边长
    POLYGON = 4
    # 分割符粗细的一半
    WIDTH = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        drag_view = option.styleObject
        from pages.edit_page import ActionListView
        if not isinstance(drag_view, ActionListView):
            raise TypeError("option.styleObject must be an instance of ActionListView")
        is_drag = drag_view.is_drag
        rect = option.rect
        # 画背景
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        if option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver):
            # list_model = drag_view.model()
            # item = list_model.itemFromIndex(index)
            if option.state & QStyle.StateFlag.State_Selected:
                painter.setBrush(QColor(180, 0, 0))
                painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), 4, rect.height())
                painter.setBrush(QColor(230, 231, 234))
                painter.drawRect(rect.topLeft().x() + 4, rect.topLeft().y(), rect.width() - 4, rect.height())
            else:
                pass
                # list_model = drag_view.model()
                # item = list_model.itemFromIndex(index)


        else:
            painter.setBrush(Qt.GlobalColor.white)
        # 开始拖拽
        if is_drag:
            the_drag_row = drag_view.the_drag_row
            the_selected_row = drag_view.the_selected_row
            up_row = drag_view.the_highlighted_row
            down_row = up_row + 1
            row_count = drag_view.model().rowCount() - 1
            # 绘制空隙，当拖拽行非选中行时，需要在选中行绘制空隙，显示DropIndicator
            if index.row() == the_selected_row and the_drag_row != the_selected_row:
                # 画上半部分
                if index.row() == up_row and index.row() != the_drag_row - 1:
                    offset = 3
                    triangle_polygon_bottom_left = QPolygon([
                        QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - (offset + self.WIDTH) + 1),
                        QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - (offset + self.WIDTH + self.POLYGON) + 1),
                        QPoint(rect.bottomLeft().x() + self.POLYGON, rect.bottomLeft().y() - (offset + self.WIDTH) + 1)
                    ])

                    triangle_polygon_bottom_right = QPolygon([
                        QPoint(rect.bottomRight().x() + 1, rect.bottomRight().y() - (offset + self.WIDTH) + 1),
                        QPoint(rect.bottomRight().x() + 1,
                               rect.bottomRight().y() - (offset + self.WIDTH + self.POLYGON) + 1),
                        QPoint(rect.bottomRight().x() - self.POLYGON + 1,
                               rect.bottomRight().y() - (offset + self.WIDTH) + 1)
                    ])

                    painter = QPainter()
                    painter.setBrush(QColor(245, 245, 247))
                    painter.drawPolygon(triangle_polygon_bottom_left)
                    painter.drawPolygon(triangle_polygon_bottom_right)
                    painter.drawRect(rect.bottomLeft().x(), rect.bottomLeft().y() - (offset + self.WIDTH) + 1,
                                     rect.width(),
                                     offset + self.WIDTH)
                    painter.drawRect(rect.bottomLeft().x(), rect.bottomLeft().y() - (offset + self.WIDTH) + 1,
                                     rect.width(),
                                     offset + self.WIDTH)
                # 画下半部分
                elif index.row() == down_row and index.row() != the_drag_row + 1:
                    offset = 3
                    triangle_polygon_top_left = QPolygon([
                        QPoint(rect.topLeft().x(), rect.topLeft().y() + offset + self.WIDTH),
                        QPoint(rect.topLeft().x(), rect.topLeft().y() + offset + self.WIDTH + self.POLYGON),
                        QPoint(rect.topLeft().x() + self.POLYGON, rect.topLeft().y() + offset + self.WIDTH)
                    ])
                    triangle_polygon_top_right = QPolygon([
                        QPoint(rect.topRight().x() + 1, rect.topRight().y() + offset + self.WIDTH),
                        QPoint(rect.topRight().x() + 1, rect.topRight().y() + offset + self.WIDTH + self.POLYGON),
                        QPoint(rect.topRight().x() - self.POLYGON + 1, rect.topRight().y() + offset + self.WIDTH)
                    ])
                    painter = QPainter()
                    painter.setBrush(QColor(245, 245, 247))
                    painter.drawPolygon(triangle_polygon_top_left)
                    painter.drawPolygon(triangle_polygon_top_right)
                    painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), offset + self.WIDTH)
            # 绘制DropIndicator
            if index.row() == up_row and index.row() != the_drag_row - 1 and index.row() != the_drag_row:
                painter.setBrush(QColor(66, 133, 244))
                if up_row == row_count:
                    triangle_polygon_bottom_left = QPolygon([
                        QPoint(rect.bottomLeft().x(),
                               rect.bottomLeft().y() - (self.POLYGON + self.WIDTH) + 1 - self.WIDTH),
                        QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - self.WIDTH + 1 - self.WIDTH),
                        QPoint(rect.bottomLeft().x() + self.POLYGON,
                               rect.bottomLeft().y() - self.WIDTH + 1 - self.WIDTH)
                    ])

                    triangle_polygon_bottom_right = QPolygon([
                        QPoint(rect.bottomRight().x() + 1,
                               rect.bottomRight().y() - (self.POLYGON + self.WIDTH) + 1 - self.WIDTH),
                        QPoint(rect.bottomRight().x() + 1, rect.bottomRight().y() - self.WIDTH + 1 - self.WIDTH),
                        QPoint(rect.bottomRight().x() - self.POLYGON + 1,
                               rect.bottomRight().y() - self.WIDTH + 1 - self.WIDTH)
                    ])

                    painter = QPainter()
                    painter.setBrush(QColor(245, 245, 247))
                    painter.drawRect(rect.bottomLeft().x(), rect.bottomLeft().y() - 2 * self.WIDTH + 1, rect.width(),
                                     2 * self.WIDTH)
                    painter.drawPolygon(triangle_polygon_bottom_left)
                    painter.drawPolygon(triangle_polygon_bottom_right)
                # 正常情况,组成上半部分(+1是根据实际情况修正)
                else:
                    triangle_polygon_bottom_left = QPolygon([
                        QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - (self.POLYGON + self.WIDTH) + 1),
                        QPoint(rect.bottomLeft().x(), rect.bottomLeft().y() - self.WIDTH + 1),
                        QPoint(rect.bottomLeft().x() + self.POLYGON, rect.bottomLeft().y() - self.WIDTH + 1)
                    ])

                    triangle_polygon_bottom_right = QPolygon([
                        QPoint(rect.bottomRight().x() + 1, rect.bottomRight().y() - (self.POLYGON + self.WIDTH) + 1),
                        QPoint(rect.bottomRight().x() + 1, rect.bottomRight().y() - self.WIDTH + 1),
                        QPoint(rect.bottomRight().x() - self.POLYGON + 1, rect.bottomRight().y() - self.WIDTH + 1)
                    ])

                    painter = QPainter()
                    painter.setBrush(QColor(245, 245, 247))
                    painter.drawRect(rect.bottomLeft().x(), rect.bottomLeft().y() - self.WIDTH + 1, rect.width(),
                                     self.WIDTH)
                    painter.drawPolygon(triangle_polygon_bottom_left)
                    painter.drawPolygon(triangle_polygon_bottom_right)

            elif index.row() == down_row and index.row() != the_drag_row + 1 and index.row() != the_drag_row:
                painter.setBrush(QColor(66, 133, 244))
                if down_row == 0:
                    triangle_polygon_top_left = QPolygon([
                        QPoint(rect.topLeft().x(), rect.topLeft().y() + (self.POLYGON + self.WIDTH) + self.WIDTH),
                        QPoint(rect.topLeft().x(), rect.topLeft().y() + self.WIDTH + self.WIDTH),
                        QPoint(rect.topLeft().x() + self.POLYGON, rect.topLeft().y() + self.WIDTH + self.WIDTH)
                    ])

                    triangle_polygon_top_right = QPolygon([
                        QPoint(rect.topRight().x() + 1, rect.topRight().y() + (self.POLYGON + self.WIDTH) + self.WIDTH),
                        QPoint(rect.topRight().x() + 1, rect.topRight().y() + self.WIDTH + self.WIDTH),
                        QPoint(rect.topRight().x() - self.POLYGON + 1, rect.topRight().y() + self.WIDTH + self.WIDTH)
                    ])

                    painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), 2 * self.WIDTH)
                    painter.drawPolygon(triangle_polygon_top_left)
                    painter.drawPolygon(triangle_polygon_top_right)
                else:
                    # normal
                    triangle_polygon_top_left = QPolygon([
                        QPoint(rect.topLeft().x(), rect.topLeft().y() + (self.POLYGON + self.WIDTH)),
                        QPoint(rect.topLeft().x(), rect.topLeft().y() + self.WIDTH),
                        QPoint(rect.topLeft().x() + self.POLYGON, rect.topLeft().y() + self.WIDTH)
                    ])

                    triangle_polygon_top_right = QPolygon([
                        QPoint(rect.topRight().x() + 1, rect.topRight().y() + (self.POLYGON + self.WIDTH)),
                        QPoint(rect.topRight().x() + 1, rect.topRight().y() + self.WIDTH),
                        QPoint(rect.topRight().x() - self.POLYGON + 1, rect.topRight().y() + self.WIDTH)
                    ])

                    painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), self.WIDTH)
                    painter.drawPolygon(triangle_polygon_top_left)
                    painter.drawPolygon(triangle_polygon_top_right)
            # 高亮拖拽行(使拖拽行的样式和选中相同)
            if index.row() == the_drag_row and the_drag_row != the_selected_row:
                painter.setBrush(QColor(180, 0, 0))
                painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), 4, rect.height())

                painter.setBrush(QColor(230, 231, 234))
                painter.drawRect(rect.topLeft().x() + 4, rect.topLeft().y(), rect.width() - 4, rect.height())

                opt = QStyleOptionViewItem()
                opt.state |= QStyle.StateFlag.State_Selected
                QStyledItemDelegate.paint(self, painter, opt, index)
                return
            QStyledItemDelegate.paint(self, painter, option, index)
            return
        QStyledItemDelegate.paint(self, painter, option, index)
