# -*- coding: utf-8 -*-

import sys
from datetime           import datetime
from qt_common          import *
from constants          import *
from gui.Ui_main_form   import *
from remote_functions   import get_staff_by_user, get_dinner_order_permissions, get_directories_changed_at
from cache              import initCache, fillCache, getSetting, deleteCacheData
from login              import tryLogin
from main_form          import main_form
from tray_application   import tray_application
from errors             import get_last_error, RaisedGuiException
from xml_utils          import get_xml_field_value

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

            #
            # Тут получим даты последних обновлений справочников с сервера и из кэша
            #
            customers_updated_at  = None
            task_types_updated_at = None
            dir_dates = get_directories_changed_at()
            customers_updated_at_str  = getSetting('customers_updated_at')
            task_types_updated_at_str = getSetting('task_types_updated_at')
            if customers_updated_at_str is not None:
                customers_updated_at  = datetime.strptime(customers_updated_at_str,  CACHE_DATETIME_FORMAT)
            if task_types_updated_at_str is not None:
                task_types_updated_at = datetime.strptime(task_types_updated_at_str, CACHE_DATETIME_FORMAT)
            
            #
            # Если данные устарели, то удалим их, fillCache() подтянет их заново
            #
            if customers_updated_at is not None:
                if customers_updated_at < dir_dates['customers_changed_at']:
                    deleteCacheData('customers')
            if task_types_updated_at is not None:
                if task_types_updated_at < dir_dates['task_types_changed_at']:
                    deleteCacheData('task_types')

            if get_last_error() != ERROR_CANT_CONNECT:
                try:
                    staff_id = get_staff_by_user(user_id)
                except:
                    staff_id = None
                fillCache(dir_dates['server_time'])
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
            # Other
            #
            QObject.connect( app.main_form.ui.tabWidget, SIGNAL('currentChanged(int)'), app.main_form.tabChanged )

            try:
                xml = get_dinner_order_permissions()
                access = int(get_xml_field_value(xml, 'ACCESS_TO_ORDERS'))
                if access:
                    view_all = int(get_xml_field_value(xml, 'VIEW_ALL_ORDERS'))
                    if not view_all:
                        ui.cmdAllDinnerOrdersToday.hide()
                else:
                    ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabDinner))
            except Exception as err:
                raise RaisedGuiException(err)

            #
            # Services
            #
            ui.treeServices.user_id = user_id
            ui.treeServices.updateServices()
            if not ui.treeServices.getItemsCount():
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabServices))
            
            #
            # Dinner
            #
            QObject.connect( ui.cmdRefreshMenu, SIGNAL('clicked()'), app.main_form.updateDinnerOrderPage )
            QObject.connect( ui.cmdCreateOrder, SIGNAL('clicked()'), app.main_form.createDinnerOrder )
            QObject.connect( ui.cmdAllDinnerOrdersToday, SIGNAL('clicked()'), app.main_form.printDinnerOrders )

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

            else:
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTasks))
                ui.tabWidget.removeTab(ui.tabWidget.indexOf(ui.tabTime))
            
            app.main_form.changeCaption()
        finally:
            QApplication.restoreOverrideCursor()
        
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
