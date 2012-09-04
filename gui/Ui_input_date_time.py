# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/twister/Dropbox/novelty_assistant/gui/input_date_time.ui'
#
# Created: Tue Sep  4 22:13:19 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmInputDateTime(object):
    def setupUi(self, frmInputDateTime):
        frmInputDateTime.setObjectName(_fromUtf8("frmInputDateTime"))
        frmInputDateTime.resize(323, 136)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/date_time_64.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmInputDateTime.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(frmInputDateTime)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(frmInputDateTime)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setMaximumSize(QtCore.QSize(65, 16777215))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/date_time_64.ico")))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.widget = QtGui.QWidget(self.widget_2)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dateEdit = QtGui.QDateEdit(self.widget)
        self.dateEdit.setEnabled(True)
        self.dateEdit.setReadOnly(False)
        self.dateEdit.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dateEdit.setMinimumDate(QtCore.QDate(2012, 1, 1))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.horizontalLayout.addWidget(self.dateEdit)
        self.timeEdit = QtGui.QTimeEdit(self.widget)
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.horizontalLayout.addWidget(self.timeEdit)
        self.horizontalLayout_2.addWidget(self.widget)
        self.verticalLayout.addWidget(self.widget_2)
        self.buttonBox = QtGui.QDialogButtonBox(frmInputDateTime)
        self.buttonBox.setMaximumSize(QtCore.QSize(16777215, 35))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(frmInputDateTime)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), frmInputDateTime.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), frmInputDateTime.reject)
        QtCore.QMetaObject.connectSlotsByName(frmInputDateTime)

    def retranslateUi(self, frmInputDateTime):
        frmInputDateTime.setWindowTitle(QtGui.QApplication.translate("frmInputDateTime", "Дата/время", None, QtGui.QApplication.UnicodeUTF8))

import novelty_assistant_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmInputDateTime = QtGui.QDialog()
    ui = Ui_frmInputDateTime()
    ui.setupUi(frmInputDateTime)
    frmInputDateTime.show()
    sys.exit(app.exec_())

