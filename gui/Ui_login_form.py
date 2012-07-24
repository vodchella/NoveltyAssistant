# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/twister/Dropbox/novelty_assistant/gui/login_form.ui'
#
# Created: Tue Jul 17 23:27:45 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmLogin(object):
    def setupUi(self, frmLogin):
        frmLogin.setObjectName(_fromUtf8("frmLogin"))
        frmLogin.resize(356, 168)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pass_64.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmLogin.setWindowIcon(icon)
        frmLogin.setSizeGripEnabled(True)
        frmLogin.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(frmLogin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(frmLogin)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(65, 16777215))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/pass_64.ico")))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.widget1 = QtGui.QWidget(self.widget)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.widget1)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.txtLogin = QtGui.QLineEdit(self.widget1)
        self.txtLogin.setObjectName(_fromUtf8("txtLogin"))
        self.verticalLayout_2.addWidget(self.txtLogin)
        self.label_3 = QtGui.QLabel(self.widget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.txtPass = QtGui.QLineEdit(self.widget1)
        self.txtPass.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPass.setObjectName(_fromUtf8("txtPass"))
        self.verticalLayout_2.addWidget(self.txtPass)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.widget1)
        self.verticalLayout.addWidget(self.widget)
        self.widget2 = QtGui.QWidget(frmLogin)
        self.widget2.setMaximumSize(QtCore.QSize(16777215, 35))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chkSavePass = QtGui.QCheckBox(self.widget2)
        self.chkSavePass.setChecked(True)
        self.chkSavePass.setObjectName(_fromUtf8("chkSavePass"))
        self.horizontalLayout.addWidget(self.chkSavePass)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget2)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addWidget(self.widget2)

        self.retranslateUi(frmLogin)
        QtCore.QMetaObject.connectSlotsByName(frmLogin)

    def retranslateUi(self, frmLogin):
        frmLogin.setWindowTitle(QtGui.QApplication.translate("frmLogin", "Авторизация", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmLogin", "Логин:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmLogin", "Пароль:", None, QtGui.QApplication.UnicodeUTF8))
        self.chkSavePass.setText(QtGui.QApplication.translate("frmLogin", "Сохранить пароль", None, QtGui.QApplication.UnicodeUTF8))

import novelty_assistant_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmLogin = QtGui.QDialog()
    ui = Ui_frmLogin()
    ui.setupUi(frmLogin)
    frmLogin.show()
    sys.exit(app.exec_())

