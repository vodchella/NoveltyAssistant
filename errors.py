# -*- coding: utf-8 -*-

import sys
import traceback
from qt_common import *
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
        QMessageBox.critical( None, u'Ошибка', QString.fromUtf8(value), QMessageBox.Ok )
        super(GuiException, self).__init__(value)

class RaisedGuiException(GuiException):
    def __init__(self, raised_err):
        super(RaisedGuiException, self).__init__('%s: %s\n%s' % (raised_err.__class__.__name__, raised_err.__str__(), traceback.format_exception(*sys.exc_info())[1]))
