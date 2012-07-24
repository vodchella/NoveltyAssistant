# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.Qt import *

from gui.Ui_login_form import *
from remote_functions import *
from cache import *

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
