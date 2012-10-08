# -*- coding: utf-8 -*- 

from qt_common              import *
from gui.Ui_input_date_time import *

def GetDateTime(caption=u'Введите дату и время', enable_date_input=False):
    frm = QDialog()
    ui = Ui_frmInputDateTime()
    ui.setupUi(frm)
    
    frm.setWindowTitle(caption)
    ui.dateEdit.setEnabled(enable_date_input)
    
    ui.dateEdit.setDate(QDate.currentDate())
    ui.timeEdit.setTime(QTime.currentTime())
    
    QObject.connect( ui.buttonBox, SIGNAL('rejected()'), frm, SLOT('reject()') )
    QObject.connect( ui.buttonBox, SIGNAL('accepted()'), frm, SLOT('accept()') )
    
    if frm.exec_() == QtGui.QDialog.Accepted:
        return ui.dateEdit.date().toString('dd.MM.yyyy') + ' ' + ui.timeEdit.time().toString('hh:mm:ss')
