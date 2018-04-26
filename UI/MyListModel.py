from PyQt5.Qt import QAbstractListModel, QModelIndex, QVariant
from PyQt5.Qt import QAbstractTableModel
from PyQt5 import Qt


class MyListModel(QAbstractListModel):
    def __init__(self, datain, parnet=None):

        """数据：一列表中的每个项目是一个行"""
        #super(MyListModel,self).__init__(parnet)
        QAbstractListModel.__init__(self,parnet)
        self.listdata = datain

    # 这2个方法是规定好的

    def rowCount(self, parent=QModelIndex()):

        return len(self.listdata)

    def data(self, index, row):  # isValid()是否有效的

        if index.isValid() and row == Qt.DisplayRole:  # 关键数据以文本的形式呈现

            return QVariant(self.listdata[index.row()])  # QVariant类就像一个最常见的Qt联盟数据类型

        else:

            return QVariant()
