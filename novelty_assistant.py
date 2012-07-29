# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QSystemTrayIcon
from gui.Ui_main_form import *

from login import *
from task_list import *
from errors import *

class main_form(QtGui.QDialog):
    ui = None
    tl = None
    
    def __init__(self):
        super(main_form,  self).__init__()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()
    
    @QtCore.pyqtSlot()
    def refreshTaskList(self):
        self.tl.updateOnDate(self.ui.dt.date())
    
    @QtCore.pyqtSlot()
    def addTask(self):
        if self.ui.dt.date() != QtCore.QDate.currentDate():
            raise GuiException('Новая задача может быть создана только сегодняшним числом')
        self.tl.newItem()

class tray_application(QtGui.QApplication):
    def __init__(self, argv):
        super(tray_application, self).__init__(argv)
        
        QtGui.QApplication.setQuitOnLastWindowClosed( False )
        
        self.tray = QtGui.QSystemTrayIcon( QtGui.QIcon(':/images/main_64.ico'), self )
        QtCore.QObject.connect( self.tray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.iconActivated )
        self.tray.setToolTip('Novelty Assistant')
        self.tray.show()
        
        menu = QtGui.QMenu()
        act = menu.addAction(u'Показать')
        act.triggered.connect(self.doShowMainForm)
        menu.addSeparator()
        act = menu.addAction(u'Выход')
        act.triggered.connect(self.doExit)
        self.tray.setContextMenu(menu)
    
    @QtCore.pyqtSlot()
    def doExit(self):
        reply = QtGui.QMessageBox.question(None, u'Подтверждение', u'Действительно желаете закрыть Novelty Assistant?', QtGui.QMessageBox.Yes |  QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.tray.hide()
            self.quit()
    
    @QtCore.pyqtSlot()
    def doShowMainForm(self):
        if self.main_form.windowState() != Qt.WindowMaximized:
            self.main_form.showNormal()
        else:
            self.main_form.show()
        self.main_form.activateWindow()
    
    @QtCore.pyqtSlot()
    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.doShowMainForm()

def main():
    app = tray_application( sys.argv )

    initCache()

    user_id = tryLogin()
    if user_id == 0:
        sys.exit(0)
    else:
        staff_id = getStaffByUser(user_id)
        
        fillCache()
        
        app.main_form = main_form()
        app.main_form.ui = Ui_frmMain()
        app.main_form.ui.setupUi(app.main_form)
        app.main_form.show()
        
        app.main_form.tl = task_list(app.main_form.ui.tabTasks)
        app.main_form.tl.staff_id = staff_id
        app.main_form.ui.gridLayout_2.addWidget(app.main_form.tl, 1, 0, 1, 1)
        
        app.main_form.statusLabel = tasks_status_label(app.main_form.ui.tabTasks)
        app.main_form.statusLabel.task_list = app.main_form.tl
        app.main_form.statusLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        app.main_form.ui.gridLayout_2.addWidget(app.main_form.statusLabel, 2, 0, 1, 1)
#        app.main_form.statusLabel.show()

        QtCore.QObject.connect( app.main_form.tl, QtCore.SIGNAL('totalTimeChanged()'), app.main_form.statusLabel.updateStatus )
        QtCore.QObject.connect( app.main_form.ui.cmdNew, QtCore.SIGNAL('clicked()'), app.main_form.addTask )
        QtCore.QObject.connect( app.main_form.ui.cmdRefresh, QtCore.SIGNAL('clicked()'), app.main_form.refreshTaskList )
        QtCore.QObject.connect( app.main_form.ui.dt, QtCore.SIGNAL('dateChanged(QDate)'), app.main_form.tl.updateOnDate )
        app.main_form.ui.dt.setDate(QtCore.QDate.currentDate())
#        app.main_form.ui.dt.setDate(QtCore.QDate(2012, 07, 20))
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
