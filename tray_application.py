# -*- coding: utf-8 -*-  

from constants          import *
from qt_common          import *
from remote_functions   import get_program_version, get_new_in_version

class tray_application(QApplication):
    def __init__(self, argv):
        super(tray_application, self).__init__(argv)
        
        QApplication.setQuitOnLastWindowClosed( False )
        
        self.tray = QSystemTrayIcon( QIcon(':/images/main_64.ico'), self )
        QObject.connect( self.tray, SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.iconActivated )
        self.tray.setToolTip(PROGRAM_NAME_FULL)
        self.tray.show()
        
        menu = QMenu()
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
    
    @pyqtSlot()
    def doExit(self):
        reply = QMessageBox.question(None, u'Подтверждение', u'Действительно желаете закрыть %s?' % PROGRAM_NAME, QMessageBox.Yes |  QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tray.hide()
            self.quit()
    
    @pyqtSlot()
    def doShowMainForm(self):
        if self.main_form.windowState() != Qt.WindowMaximized:
            self.main_form.showNormal()
        else:
            self.main_form.show()
        self.main_form.activateWindow()
    
    @pyqtSlot()
    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.doShowMainForm()
    
    @pyqtSlot()
    def checkUpdates(self, msgbox_if_false=True):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            last_version_number = get_program_version()
            QApplication.restoreOverrideCursor()
            if last_version_number > PROGRAM_REVISION_NUMBER:
                new_in_version = get_new_in_version().decode('utf-8').replace('\n', '<br>')
                if new_in_version is not None:
                    new_in_version = u"<br><br>Новое в версии:<br>%s" % new_in_version
                else:
                    new_in_version = ''
                if QMessageBox.question(None, PROGRAM_NAME, u'Доступна новая версия программы. Перейти на страницу загрузки?%s' % new_in_version, QMessageBox.Yes |  QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                    QDesktopServices.openUrl(QUrl('https://launchpad.net/novelty-assistant/+download'))
            else:
                if msgbox_if_false:
                    QMessageBox.information(None, PROGRAM_NAME, u'У Вас установлена самая свежая версия', QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def showAbout(self):
        s = QDialog(None)
        s.setLayout( QVBoxLayout( s ) )

        s.setWindowTitle( PROGRAM_NAME )
        
        icon = QIcon()
        icon.addPixmap(QPixmap(":/images/main_64.ico"), QIcon.Normal, QIcon.Off)
        s.setWindowIcon(icon)

        label = QLabel( u"%s<br><br>Twister© 2012 для компании <a href='http://novelty.kz'>Novelty</a><br><br><a href='https://launchpad.net/novelty-assistant/'>https://launchpad.net/novelty-assistant/</a>" % PROGRAM_NAME_FULL )
        label.setWordWrap( True )
        label.setOpenExternalLinks( True )
        s.layout().addWidget( label )

        button = QPushButton( "Ok" )
        s.layout().addWidget( button )
        s.layout().setAlignment( button, Qt.AlignHCenter )

        QObject.connect( button, SIGNAL( "clicked()" ), s, SLOT( "accept()" ) )
        
        s.exec_()
