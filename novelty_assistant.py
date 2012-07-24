# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from gui.Ui_main_form import *
from gui.Ui_login_form import *

from task_list import *
from remote_functions import *
from cache import *
from errors import *

def loginAndSaveData(user_name, user_pass, check_state):
    user_id = 0
    try:
        user_id = remoteLogin(user_name, user_pass)
    except:
        pass
    if (user_id != 0) and (check_state == Qt.Checked):
        saveLoginData(user_name, user_pass)
    return user_id

def tryLogin():
    bShowDialog = False
    user_id = 0
    user_name = ''
    
    saved_login_data = getSavedLoginData()
    if saved_login_data is not None:
        user_name = saved_login_data[0]
        user_id = loginAndSaveData(user_name, saved_login_data[1], 0)
        if user_id == 0:
            bShowDialog = True
    else:
        bShowDialog = True
    
    if bShowDialog:
        frmLogin = QtGui.QDialog()
        ui = Ui_frmLogin()
        ui.setupUi(frmLogin)
        if len(user_name) != 0:
            ui.txtLogin.setText(user_name)
            ui.txtPass.setFocus()
            
        QtCore.QObject.connect( ui.buttonBox, QtCore.SIGNAL('rejected()'), frmLogin, QtCore.SLOT('reject()') )
        QtCore.QObject.connect( ui.buttonBox, QtCore.SIGNAL('accepted()'), frmLogin, QtCore.SLOT('accept()') )
        
        if frmLogin.exec_() == QtGui.QDialog.Accepted:
            user_id = loginAndSaveData(ui.txtLogin.text(), ui.txtPass.text(), ui.chkSavePass.checkState())
    
    return user_id

class main_form(QtGui.QDialog):
    ui = None
    tl = None
    
    def __init__(self):
        super(main_form,  self).__init__()
    
    @QtCore.pyqtSlot()
    def refreshTaskList(self):
        self.tl.updateOnDate(self.ui.dt.date())
    
    @QtCore.pyqtSlot()
    def addTask(self):
        if self.ui.dt.date() != QtCore.QDate.currentDate():
            raise GuiException('Новая задача может быть создана только сегодняшним числом')
        self.tl.newItem()

def main():
    app = QtGui.QApplication( sys.argv )
#    QtGui.QApplication.setQuitOnLastWindowClosed( False )

    initCache()

    user_id = tryLogin()
    if user_id == 0:
        sys.exit(0)
    else:
        staff_id = getStaffByUser(user_id)
        
        fillCache()
        
        frmMain = main_form()
        frmMain.ui = Ui_frmMain()
        frmMain.ui.setupUi(frmMain)
        frmMain.show()
        
        frmMain.tl = task_list(frmMain.ui.tabTasks)
        frmMain.tl.staff_id = staff_id
        frmMain.ui.gridLayout_2.addWidget(frmMain.tl, 2, 0, 1, 1)

        QtCore.QObject.connect( frmMain.ui.cmdNew, QtCore.SIGNAL('clicked()'), frmMain.addTask )
        QtCore.QObject.connect( frmMain.ui.cmdRefresh, QtCore.SIGNAL('clicked()'), frmMain.refreshTaskList )
        QtCore.QObject.connect( frmMain.ui.dt, QtCore.SIGNAL('dateChanged(QDate)'), frmMain.tl.updateOnDate )
        frmMain.ui.dt.setDate(QtCore.QDate.currentDate())
#        frmMain.ui.dt.setDate(QtCore.QDate(2012, 07, 20))
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
