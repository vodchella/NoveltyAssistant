# -*- coding: utf-8 -*-

import sys
from qt_common          import *
from constants          import *
from gui.Ui_main_form   import *
from remote_functions   import get_staff_by_user
from cache              import initCache, fillCache
from login              import tryLogin
from main_form          import main_form
from tray_application   import tray_application
#from service_list       import service_list
from errors             import get_last_error


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
            
            #list = service_list(app.main_form.ui.tabAppServers)
            #list.setGeometry(QRect(50, 70, 256, 192))
            #list.show() 
            
            if staff_id is not None:
                #
                # Tasks
                #
                app.main_form.tl = app.main_form.ui.tl
                app.main_form.tl.main_form = app.main_form
                app.main_form.tl.staff_id = staff_id
                
                app.main_form.ui.statusLabel.task_list = app.main_form.tl
                app.main_form.ui.countLabel.task_list  = app.main_form.tl

                QObject.connect( app.main_form.tl, SIGNAL('totalCountChanged()'), app.main_form.ui.countLabel.updateCount )
                QObject.connect( app.main_form.tl, SIGNAL('totalTimeChanged()'), app.main_form.ui.statusLabel.updateStatus )
                QObject.connect( app.main_form.tl, SIGNAL('startEditItem()'), app.main_form.stopSearching )
                QObject.connect( app.main_form.ui.cmdNew, SIGNAL('clicked()'), app.main_form.addTask )
                QObject.connect( app.main_form.ui.cmdRefresh, SIGNAL('clicked()'), app.main_form.refreshTaskList )
                QObject.connect( app.main_form.ui.cmdRefresh, SIGNAL('clicked()'), app.main_form.stopSearching )
                QObject.connect( app.main_form.ui.cmdSearch, SIGNAL('clicked()'), app.main_form.startSearching )
                QObject.connect( app.main_form.ui.cmdCancelSearch, SIGNAL('clicked()'), app.main_form.stopSearching )
                QObject.connect( app.main_form.ui.txtSearchText, SIGNAL('textChanged(QString)'), app.main_form.searchForText )
                QObject.connect( app.main_form.ui.dt, SIGNAL('dateChanged(QDate)'), app.main_form.tl.updateOnDate )
                QObject.connect( app.main_form.ui.dt, SIGNAL('dateChanged(QDate)'), app.main_form.stopSearching )
                app.main_form.ui.dt.setDate(QDate.currentDate())
                
                #
                # Time
                #
                app.main_form.ui.tblWeek.staff_id = staff_id
                QObject.connect( app.main_form.ui.cmdComing,  SIGNAL('clicked()'), app.main_form.setNewComingTime )
                QObject.connect( app.main_form.ui.cmdLeaving, SIGNAL('clicked()'), app.main_form.setNewLeavingTime )
                QObject.connect( app.main_form.ui.cmdRefreshTimeSheet, SIGNAL('clicked()'), app.main_form.ui.tblWeek.updateForCurrentWeek )
                
                #
                # Other
                #
                QObject.connect( app.main_form.ui.tabWidget, SIGNAL('currentChanged(int)'), app.main_form.tabChanged )
            else:
                ui = app.main_form.ui
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTasks))
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTime))
        finally:
            QApplication.restoreOverrideCursor()
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
