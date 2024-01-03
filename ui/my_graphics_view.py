from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView


class MyGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super(MyGraphicsView, self).__init__(scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor

        self.scale(factor, factor)
