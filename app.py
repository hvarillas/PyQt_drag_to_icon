"""Image to icon"""
# standard
import sys
# thirdparty
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# local


class ImageLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n")
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed white;
                color: white;
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(1000, 400, 400, 400)
        self.setWindowTitle("Drag And Drop")
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QWidget {
                background-color: #333;
            }
        """)

        self.converter = ImageConverter()

        self.photoViewer = ImageLabel()

        # Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.photoViewer)
        self.setLayout(self.mainLayout)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasImage:
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            url =  event.mimeData().urls()[0].toLocalFile()
            qpix = QPixmap(url)
            qpix = qpix.scaled(380, 380, Qt.AspectRatioMode.KeepAspectRatio)
            self.photoViewer.setPixmap(qpix)
            self.converter.to_icon(url)


class ImageConverter():

    def to_icon(self, path: str) -> None:
        img = Image.open(path)
        ico = '.'.join(path.split('.')[:-1])
        ico = f"{ico}.ico"
        sizes = [
            (16, 16),
            (24, 24),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (255, 255),
        ]
        img.save(
            ico,
            format = 'ICO',
            sizes=sizes
        )

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())