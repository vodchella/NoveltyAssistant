# -*- coding: utf-8 -*- 

from PyQt4 import QtGui
from gui.Ui_input_date_time import *

def GetDateTime(caption=u'Введите дату и время', enable_date_input=False):
    frm = QtGui.QDialog()
    ui = Ui_frmInputDateTime()
    ui.setupUi(frm)
    
    frm.setWindowTitle(caption)
    ui.dateEdit.setEnabled(enable_date_input)
    
    ui.dateEdit.setDate(QtCore.QDate.currentDate())
    ui.timeEdit.setTime(QtCore.QTime.currentTime())
    
    QtCore.QObject.connect( ui.buttonBox, QtCore.SIGNAL('rejected()'), frm, QtCore.SLOT('reject()') )
    QtCore.QObject.connect( ui.buttonBox, QtCore.SIGNAL('accepted()'), frm, QtCore.SLOT('accept()') )
    
    if frm.exec_() == QtGui.QDialog.Accepted:
        return ui.dateEdit.date().toString('dd.MM.yyyy') + ' ' + ui.timeEdit.time().toString('hh:mm:ss')
