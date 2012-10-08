# -*- coding: utf-8 -*-

from qt_common          import *
from constants          import *
from gui.Ui_login_form  import *
from remote_functions   import remote_login
from cache              import getSavedLoginData, saveLoginData
from errors             import set_last_error

def loginAndSaveData(user_name, user_pass, check_state):
    user_id = 0
    try:
        user_id = remote_login(user_name, user_pass)
    except:
        pass
    if (user_id != 0) and (check_state == Qt.Checked):
        saveLoginData(user_name, user_pass)
    return user_id

def tryLogin():
    bShowDialog = False
    user_id = 0
    user_name = ''
    
    set_last_error(NO_ERROR)
    
    saved_login_data = getSavedLoginData()
    if saved_login_data is not None:
        user_name = saved_login_data[0]
        user_id = loginAndSaveData(user_name, saved_login_data[1], 0)
        if user_id == 0:
            bShowDialog = True
    else:
        bShowDialog = True
    
    if bShowDialog and get_last_error() != ERROR_CANT_CONNECT:
        frmLogin = QtGui.QDialog()
        ui = Ui_frmLogin()
        ui.setupUi(frmLogin)
        if user_name:
            ui.txtLogin.setText(user_name)
            ui.txtPass.setFocus()
            
        QObject.connect( ui.buttonBox, SIGNAL('rejected()'), frmLogin, SLOT('reject()') )
        QObject.connect( ui.buttonBox, SIGNAL('accepted()'), frmLogin, SLOT('accept()') )
        
        if frmLogin.exec_() == QtGui.QDialog.Accepted:
            user_id = loginAndSaveData(ui.txtLogin.text(), ui.txtPass.text(), ui.chkSavePass.checkState())
    
    return user_id 
