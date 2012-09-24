# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QSystemTrayIcon
from gui.Ui_main_form import *

from login import *
from task_list import *
from errors import *
from get_date_time import *
from remote_functions import *
from constants import *
from str_utils import *

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
    
    @QtCore.pyqtSlot()
    def setNewComingTime(self):
        date_time_str = GetDateTime(caption=u'Время прихода')
        if date_time_str is not None:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                setComingTimeXML(self.tl.staff_id, date_time_str)
            finally:
                self.ui.tblWeek.updateForCurrentWeek()
                QApplication.restoreOverrideCursor()
    
    @QtCore.pyqtSlot()
    def setNewLeavingTime(self):
        date_time_str = GetDateTime(caption=u'Время ухода')
        if date_time_str is not None:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                setLeavingTimeXML(self.tl.staff_id, date_time_str)
            finally:
                self.ui.tblWeek.updateForCurrentWeek()
                QApplication.restoreOverrideCursor()

class tray_application(QtGui.QApplication):
    def __init__(self, argv):
        super(tray_application, self).__init__(argv)
        
        QtGui.QApplication.setQuitOnLastWindowClosed( False )
        
        self.tray = QtGui.QSystemTrayIcon( QtGui.QIcon(':/images/main_64.ico'), self )
        QtCore.QObject.connect( self.tray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.iconActivated )
        self.tray.setToolTip('Novelty Assistant')
        self.tray.show()
        
        menu = QtGui.QMenu()
        act = menu.addAction(u'О программе...')
        act.triggered.connect(self.showAbout)
        act = menu.addAction(u'Проверить обновления')
        act.triggered.connect(self.checkUpdates)
        menu.addSeparator()
        act = menu.addAction(u'Показать')
        act.triggered.connect(self.doShowMainForm)
        menu.addSeparator()
        act = menu.addAction(u'Выход')
        act.triggered.connect(self.doExit)
        self.tray.setContextMenu(menu)
    
    @QtCore.pyqtSlot()
    def doExit(self):
        reply = QtGui.QMessageBox.question(None, u'Подтверждение', u'Действительно желаете закрыть %s?' % PROGRAM_NAME, QtGui.QMessageBox.Yes |  QtGui.QMessageBox.No, QtGui.QMessageBox.No)
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
    
    @QtCore.pyqtSlot()
    def checkUpdates(self, msgbox_if_false=True):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            last_version_number = getProgramVersion()
            QApplication.restoreOverrideCursor()
            if last_version_number > PROGRAM_REVISION_NUMBER:
                if QtGui.QMessageBox.question(None, PROGRAM_NAME, u'Доступна новая версия программы. Перейти на страницу загрузки?', QtGui.QMessageBox.Yes |  QtGui.QMessageBox.No, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                    QDesktopServices.openUrl(QUrl('https://launchpad.net/novelty-assistant/+download'))
            else:
                if msgbox_if_false:
                    QtGui.QMessageBox.information(None, PROGRAM_NAME, u'У Вас установлена самая свежая версия', QtGui.QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()
    
    @QtCore.pyqtSlot()
    def showAbout(self):
        s = QtGui.QDialog(None)
        s.setLayout( QtGui.QVBoxLayout( s ) )

        s.setWindowTitle( PROGRAM_NAME )
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/main_64.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        s.setWindowIcon(icon)

        label = QtGui.QLabel( u"%s<br><br>Twister© 2012 для компании <a href='http://novelty.kz'>Novelty</a><br><br><a href='https://launchpad.net/novelty-assistant/'>https://launchpad.net/novelty-assistant/</a>" % PROGRAM_NAME_FULL )
        label.setWordWrap( True )
        label.setOpenExternalLinks( True )

        s.layout().addWidget( label )

        button = QtGui.QPushButton( "Ok" )
        s.layout().addWidget( button )
        s.layout().setAlignment( button, Qt.AlignHCenter )

        QtCore.QObject.connect( button, QtCore.SIGNAL( "clicked()" ), s, QtCore.SLOT( "accept()" ) )
        
        s.exec_()

def main():
    app = tray_application( sys.argv )

    initCache()

    user_id = tryLogin()
    if user_id == 0:
        sys.exit(0)
    else:
        app.checkUpdates(False)
        
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            staff_id = getStaffByUser(user_id)
            fillCache()
            
            app.main_form = main_form()
            app.main_form.ui = Ui_frmMain()
            app.main_form.ui.setupUi(app.main_form)
            app.main_form.setWindowTitle(PROGRAM_NAME_FULL)
            app.main_form.show()
            
            #
            # Tasks
            #
            app.main_form.tl = app.main_form.ui.tl
            app.main_form.tl.staff_id = staff_id
            
            app.main_form.ui.statusLabel.task_list = app.main_form.tl
            app.main_form.ui.countLabel.task_list  = app.main_form.tl

            QtCore.QObject.connect( app.main_form.tl, QtCore.SIGNAL('totalCountChanged()'), app.main_form.ui.countLabel.updateCount )
            QtCore.QObject.connect( app.main_form.tl, QtCore.SIGNAL('totalTimeChanged()'), app.main_form.ui.statusLabel.updateStatus )
            QtCore.QObject.connect( app.main_form.ui.cmdNew, QtCore.SIGNAL('clicked()'), app.main_form.addTask )
            QtCore.QObject.connect( app.main_form.ui.cmdRefresh, QtCore.SIGNAL('clicked()'), app.main_form.refreshTaskList )
            QtCore.QObject.connect( app.main_form.ui.dt, QtCore.SIGNAL('dateChanged(QDate)'), app.main_form.tl.updateOnDate )
            app.main_form.ui.dt.setDate(QtCore.QDate.currentDate())
            
            #
            # Time
            #
            app.main_form.ui.tblWeek.staff_id = staff_id
            app.main_form.ui.tblWeek.updateForCurrentWeek()
            
            QtCore.QObject.connect( app.main_form.ui.cmdComing,  QtCore.SIGNAL('clicked()'), app.main_form.setNewComingTime )
            QtCore.QObject.connect( app.main_form.ui.cmdLeaving, QtCore.SIGNAL('clicked()'), app.main_form.setNewLeavingTime )
        finally:
            QApplication.restoreOverrideCursor()
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
