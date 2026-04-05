"""
Screenshot viewer widget for displaying live screen previews.
"""
from PIL import Image
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage


class ScreenshotViewer(QWidget):
    """Widget that displays live screenshots with bounding boxes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for large screenshots
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label to display the screenshot
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
            }
        """)
        self.image_label.setMinimumSize(640, 480)

        scroll.setWidget(self.image_label)
        layout.addWidget(scroll)

        self.current_image = None

    def update_screenshot(self, parsed_screen: dict):
        """
        Update the displayed screenshot.

        Args:
            parsed_screen: dict with 'image' (PIL Image) and optionally 'base64_image'
        """
        pil_image = parsed_screen.get('image')
        if pil_image is None:
            return

        self.current_image = pil_image

        # Convert PIL Image to QPixmap
        qt_image = self._pil_to_qimage(pil_image)
        pixmap = QPixmap.fromImage(qt_image)

        # Scale to fit label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

    def _pil_to_qimage(self, pil_image: Image) -> QImage:
        """Convert PIL Image to QImage."""
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        data = pil_image.tobytes("raw", "RGB")
        width, height = pil_image.size
        return QImage(data, width, height, QImage.Format_RGB888).copy()

    def clear(self):
        """Clear the displayed screenshot."""
        self.image_label.clear()
        self.current_image = None
