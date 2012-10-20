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
            ui = app.main_form.ui
            ui.setupUi(app.main_form)
            ui.searchWidget.hide()
            app.main_form.setWindowTitle(PROGRAM_NAME_FULL)
            app.main_form.show()

            #
            # Services
            #
            ui.treeServices.user_id = user_id
            ui.treeServices.updateServices()
            if not ui.treeServices.getItemsCount():
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabServices))
            
            if staff_id is not None:
                #
                # Tasks
                #
                app.main_form.tl = ui.tl
                app.main_form.tl.main_form = app.main_form
                app.main_form.tl.staff_id = staff_id
                
                ui.statusLabel.task_list = app.main_form.tl
                ui.countLabel.task_list  = app.main_form.tl

                QObject.connect( app.main_form.tl, SIGNAL('totalCountChanged()'), ui.countLabel.updateCount )
                QObject.connect( app.main_form.tl, SIGNAL('totalTimeChanged()'), ui.statusLabel.updateStatus )
                QObject.connect( app.main_form.tl, SIGNAL('startEditItem()'), app.main_form.stopSearching )
                QObject.connect( ui.cmdNew, SIGNAL('clicked()'), app.main_form.addTask )
                QObject.connect( ui.cmdRefresh, SIGNAL('clicked()'), app.main_form.refreshTaskList )
                QObject.connect( ui.cmdRefresh, SIGNAL('clicked()'), app.main_form.stopSearching )
                QObject.connect( ui.cmdSearch, SIGNAL('clicked()'), app.main_form.startSearching )
                QObject.connect( ui.cmdCancelSearch, SIGNAL('clicked()'), app.main_form.stopSearching )
                QObject.connect( ui.txtSearchText, SIGNAL('textChanged(QString)'), app.main_form.searchForText )
                QObject.connect( ui.dt, SIGNAL('dateChanged(QDate)'), app.main_form.tl.updateOnDate )
                QObject.connect( ui.dt, SIGNAL('dateChanged(QDate)'), app.main_form.stopSearching )
                app.main_form.ui.dt.setDate(QDate.currentDate())
                
                #
                # Time
                #
                ui.tblWeek.staff_id = staff_id
                QObject.connect( ui.cmdComing,  SIGNAL('clicked()'), app.main_form.setNewComingTime )
                QObject.connect( ui.cmdLeaving, SIGNAL('clicked()'), app.main_form.setNewLeavingTime )
                QObject.connect( ui.cmdRefreshTimeSheet, SIGNAL('clicked()'), ui.tblWeek.updateForCurrentWeek )
                
                #
                # Other
                #
                QObject.connect( app.main_form.ui.tabWidget, SIGNAL('currentChanged(int)'), app.main_form.tabChanged )
            else:
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTasks))
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTime))
        finally:
            QApplication.restoreOverrideCursor()
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
