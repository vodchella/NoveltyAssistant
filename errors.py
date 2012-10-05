# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
from constants import *

last_error_code = ERROR_SUCCESS

def set_last_error(err_code):
    global last_error_code
    last_error_code = err_code

def get_last_error():
    return last_error_code

class GuiException(Exception):
    def __init__(self, value):
        QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.critical( None, u'Ошибка', QtCore.QString.fromUtf8(value), QtGui.QMessageBox.Ok )
        super(GuiException, self).__init__(value)
