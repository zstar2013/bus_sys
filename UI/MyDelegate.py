from PyQt5.QtWidgets import QItemDelegate
from PyQt5.Qt import QPen,QStyle,QBrush
from PyQt5 import Qt

class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        painter.save()

        # set background color
        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.red))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        # set text color
        painter.setPen(QPen(Qt.black))
        value = index.data(Qt.DisplayRole)
        if value.isValid():
            text = value.toString()
            painter.drawText(option.rect, Qt.AlignLeft, text)

        painter.restore()