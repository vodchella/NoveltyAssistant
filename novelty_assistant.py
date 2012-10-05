# -*- coding: utf-8 -*-

import sys
import datetime

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
        self.clearAllSearchSelectionsInTaskList = QtCore.pyqtSignal()
    
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
                set_coming_time(self.tl.staff_id, date_time_str)
            finally:
                self.ui.tblWeek.updateForCurrentWeek()
                QApplication.restoreOverrideCursor()
    
    @QtCore.pyqtSlot()
    def setNewLeavingTime(self):
        date_time_str = GetDateTime(caption=u'Время ухода')
        if date_time_str is not None:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                set_leaving_time(self.tl.staff_id, date_time_str)
            finally:
                self.ui.tblWeek.updateForCurrentWeek()
                QApplication.restoreOverrideCursor()
    
    @QtCore.pyqtSlot()
    def tabChanged(self, index):
        ob_name = self.ui.tabWidget.widget(index).objectName()
        if ob_name == 'tabTime':
            if (self.ui.tblWeek.today is None) or (self.ui.tblWeek.today != datetime.date.today()):
                self.ui.tblWeek.updateForCurrentWeek()
    
    @QtCore.pyqtSlot()
    def startSearching(self):
        QtCore.QObject.emit( self.tl, QtCore.SIGNAL('stopEditAllItems()') )
        self.ui.txtSearchText.setPalette(self.createDefaultPalette())
        self.ui.searchWidget.show()
        self.ui.txtSearchText.setFocus()
        self.ui.txtSearchText.selectAll()
    
    @QtCore.pyqtSlot()
    def stopSearching(self):
        QtCore.QObject.emit( self, QtCore.SIGNAL('clearAllSearchSelectionsInTaskList()') )
        self.ui.searchWidget.hide()
    
    def createNotFoundPalette(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 4, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 4, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(169, 167, 167))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        return palette
    
    def createDefaultPalette(self):
        return self.ui.tabWidget.palette()
    
    @QtCore.pyqtSlot()
    def searchForText(self, text):
        def highlightLabelIfNeed(label):
            caption = unicode(label.text())
            if txt_u in caption.upper():
                label.highlightText(text)
                return label
        
        QtCore.QObject.emit( self, QtCore.SIGNAL('clearAllSearchSelectionsInTaskList()') )
        first_widget = None
        
        txt_u = unicode(text).upper().strip()
        if txt_u:
            for gr in filter(lambda g: g.group_id != -1, self.tl.groups):
                widget = highlightLabelIfNeed(gr.label)
                if first_widget is None: first_widget = widget
                for item in filter(lambda i: i.group_id == gr.group_id, self.tl.items):
                    widget = highlightLabelIfNeed(item.lblDesc)
                    if first_widget is None: first_widget = widget
                    widget = highlightLabelIfNeed(item.lblTime)
                    if first_widget is None: first_widget = widget
            if first_widget is not None:
                self.tl.ensureWidgetVisible(first_widget)
                self.ui.txtSearchText.setPalette(self.createDefaultPalette())
            else:
                self.ui.txtSearchText.setPalette(self.createNotFoundPalette())
        else:
            self.ui.txtSearchText.setPalette(self.createDefaultPalette())

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
            last_version_number = get_program_version()
            QApplication.restoreOverrideCursor()
            if last_version_number > PROGRAM_REVISION_NUMBER:
                new_in_version = get_new_in_version()
                if new_in_version is not None:
                    new_in_version = u"<br><br>Новое в версии:<br>%s" % new_in_version
                else:
                    new_in_version = ''
                if QtGui.QMessageBox.question(None, PROGRAM_NAME, u'Доступна новая версия программы. Перейти на страницу загрузки?%s' % new_in_version, QtGui.QMessageBox.Yes |  QtGui.QMessageBox.No, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
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
    if user_id == 0 and not DONT_EXIT_IF_CANT_CONNECT:
        sys.exit(0)
    else:
        #
        # Условия "get_last_error() != ERROR_CANT_CONNECT" никогда не будут выполняться
        # без установленного флага DONT_EXIT_IF_CANT_CONNECT, т.к. без этого флага,
        # в случае невозможности соединиться с базой, выполнение просто не дойдет до сюда.
        #
        # Флаг DONT_EXIT_IF_CANT_CONNECT предназначен только для отладочных целей и никогда
        # не должен использоваться в production-версиях.
        #
        if get_last_error() != ERROR_CANT_CONNECT:
            app.checkUpdates(False)
        
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            if get_last_error() != ERROR_CANT_CONNECT:
                staff_id = get_staff_by_user(user_id)
                fillCache()
            else:
                staff_id = None
            
            app.main_form = main_form()
            app.main_form.ui = Ui_frmMain()
            app.main_form.ui.setupUi(app.main_form)
            app.main_form.ui.searchWidget.hide()
            app.main_form.setWindowTitle(PROGRAM_NAME_FULL)
            app.main_form.show()
            
            if staff_id is not None:
                #
                # Tasks
                #
                app.main_form.tl = app.main_form.ui.tl
                app.main_form.tl.main_form = app.main_form
                app.main_form.tl.staff_id = staff_id
                
                app.main_form.ui.statusLabel.task_list = app.main_form.tl
                app.main_form.ui.countLabel.task_list  = app.main_form.tl

                QtCore.QObject.connect( app.main_form.tl, QtCore.SIGNAL('totalCountChanged()'), app.main_form.ui.countLabel.updateCount )
                QtCore.QObject.connect( app.main_form.tl, QtCore.SIGNAL('totalTimeChanged()'), app.main_form.ui.statusLabel.updateStatus )
                QtCore.QObject.connect( app.main_form.tl, QtCore.SIGNAL('startEditItem()'), app.main_form.stopSearching )
                QtCore.QObject.connect( app.main_form.ui.cmdNew, QtCore.SIGNAL('clicked()'), app.main_form.addTask )
                QtCore.QObject.connect( app.main_form.ui.cmdRefresh, QtCore.SIGNAL('clicked()'), app.main_form.refreshTaskList )
                QtCore.QObject.connect( app.main_form.ui.cmdRefresh, QtCore.SIGNAL('clicked()'), app.main_form.stopSearching )
                QtCore.QObject.connect( app.main_form.ui.cmdSearch, QtCore.SIGNAL('clicked()'), app.main_form.startSearching )
                QtCore.QObject.connect( app.main_form.ui.cmdCancelSearch, QtCore.SIGNAL('clicked()'), app.main_form.stopSearching )
                QtCore.QObject.connect( app.main_form.ui.txtSearchText, QtCore.SIGNAL('textChanged(QString)'), app.main_form.searchForText )
                QtCore.QObject.connect( app.main_form.ui.dt, QtCore.SIGNAL('dateChanged(QDate)'), app.main_form.tl.updateOnDate )
                QtCore.QObject.connect( app.main_form.ui.dt, QtCore.SIGNAL('dateChanged(QDate)'), app.main_form.stopSearching )
                app.main_form.ui.dt.setDate(QtCore.QDate.currentDate())
                
                #
                # Time
                #
                app.main_form.ui.tblWeek.staff_id = staff_id
                QtCore.QObject.connect( app.main_form.ui.cmdComing,  QtCore.SIGNAL('clicked()'), app.main_form.setNewComingTime )
                QtCore.QObject.connect( app.main_form.ui.cmdLeaving, QtCore.SIGNAL('clicked()'), app.main_form.setNewLeavingTime )
                QtCore.QObject.connect( app.main_form.ui.cmdRefreshTimeSheet, QtCore.SIGNAL('clicked()'), app.main_form.ui.tblWeek.updateForCurrentWeek )
                
                #
                # Other
                #
                QtCore.QObject.connect( app.main_form.ui.tabWidget, QtCore.SIGNAL('currentChanged(int)'), app.main_form.tabChanged )
            else:
                ui = app.main_form.ui
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTasks))
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTime))
        finally:
            QApplication.restoreOverrideCursor()
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
