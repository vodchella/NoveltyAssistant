# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/twister/Dropbox/novelty_assistant/gui/main_form.ui'
#
# Created: Sun Jul 29 19:35:58 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmMain(object):
    def setupUi(self, frmMain):
        frmMain.setObjectName(_fromUtf8("frmMain"))
        frmMain.resize(410, 399)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmMain.sizePolicy().hasHeightForWidth())
        frmMain.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/main_64.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmMain.setWindowIcon(icon)
        frmMain.setSizeGripEnabled(False)
        self.gridLayout_3 = QtGui.QGridLayout(frmMain)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tabWidget = QtGui.QTabWidget(frmMain)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTasks = QtGui.QWidget()
        self.tabTasks.setObjectName(_fromUtf8("tabTasks"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabTasks)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.frame = QtGui.QFrame(self.tabTasks)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cmdNew = QtGui.QPushButton(self.frame)
        self.cmdNew.setAutoDefault(False)
        self.cmdNew.setObjectName(_fromUtf8("cmdNew"))
        self.horizontalLayout.addWidget(self.cmdNew)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.dt = QtGui.QDateEdit(self.frame)
        self.dt.setCalendarPopup(True)
        self.dt.setObjectName(_fromUtf8("dt"))
        self.horizontalLayout.addWidget(self.dt)
        self.cmdRefresh = QtGui.QPushButton(self.frame)
        self.cmdRefresh.setAutoDefault(False)
        self.cmdRefresh.setFlat(False)
        self.cmdRefresh.setObjectName(_fromUtf8("cmdRefresh"))
        self.horizontalLayout.addWidget(self.cmdRefresh)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTasks, _fromUtf8("Задачи"))
        self.tabTime = QtGui.QWidget()
        self.tabTime.setObjectName(_fromUtf8("tabTime"))
        self.gridLayout = QtGui.QGridLayout(self.tabTime)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget.addTab(self.tabTime, _fromUtf8("Приход / уход"))
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(frmMain)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def retranslateUi(self, frmMain):
        frmMain.setWindowTitle(QtGui.QApplication.translate("frmMain", "Novelty Assistant", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdNew.setToolTip(QtGui.QApplication.translate("frmMain", "CTRL+N", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdNew.setText(QtGui.QApplication.translate("frmMain", "Новая", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdNew.setShortcut(QtGui.QApplication.translate("frmMain", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmMain", "Задачи на дату:", None, QtGui.QApplication.UnicodeUTF8))
        self.dt.setDisplayFormat(QtGui.QApplication.translate("frmMain", "dd.MM.yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdRefresh.setToolTip(QtGui.QApplication.translate("frmMain", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdRefresh.setText(QtGui.QApplication.translate("frmMain", "Обновить", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdRefresh.setShortcut(QtGui.QApplication.translate("frmMain", "F5", None, QtGui.QApplication.UnicodeUTF8))

import novelty_assistant_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmMain = QtGui.QDialog()
    ui = Ui_frmMain()
    ui.setupUi(frmMain)
    frmMain.show()
    sys.exit(app.exec_())

