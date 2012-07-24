# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication

class GuiException(Exception):
    def __init__(self, value):
        QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.critical( None, u'Ошибка', QtCore.QString.fromUtf8(value), QtGui.QMessageBox.Ok )
        super(GuiException, self).__init__(value)
