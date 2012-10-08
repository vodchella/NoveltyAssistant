# -*- coding: utf-8 -*- 

from qt_common import *

class service_delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(service_delegate, self).__init__(parent)
    
    def createEditor(self, parent, option, index):
        return QPushButton(parent)


class service_model(QAbstractListModel):
    def __init__(self, parent=None, *args):
        super(service_model, self).__init__(parent, *args)
    
    def rowCount(self, parent=QModelIndex()): 
        return 2
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant('hello %i' % index.row())
        else: 
            return QVariant()
    
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


class service_list(QListView):
    def __init__(self, parent):
        super(service_list, self).__init__(parent)
        self.setItemDelegate(service_delegate(self))
        self.setEditTriggers(QAbstractItemView.CurrentChanged | QAbstractItemView.SelectedClicked)
        self.setModel(service_model())
