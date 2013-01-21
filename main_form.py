# -*- coding: utf-8 -*-

import datetime
from qt_common          import *
from constants          import *
from get_date_time      import GetDateTime
from remote_functions   import set_coming_time, set_leaving_time, get_dinner_order, create_ore_replace_dinner_order, generate_dinner_report
from errors             import GuiException, RaisedGuiException
from dinner             import get_today_menu_text
from xml_utils          import get_xml_field_value, prepare_string
from file_utils         import clear_tmp_dir, save_tmp_file, open_file_with_default_app

class main_form(QDialog):
    ui = None
    tl = None
    new_today_menu = None
    
    def __init__(self):
        super(main_form,  self).__init__()
        self.clearAllSearchSelectionsInTaskList = pyqtSignal()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()
    
    @pyqtSlot()
    def refreshTaskList(self):
        self.tl.updateOnDate(self.ui.dt.date())
    
    @pyqtSlot()
    def addTask(self):
        if self.ui.dt.date() != QDate.currentDate():
            raise GuiException('Новая задача может быть создана только сегодняшним числом')
        self.tl.newItem()
    
    @pyqtSlot()
    def setNewComingTime(self):
        date_time_str = GetDateTime(caption=u'Время прихода')
        if date_time_str is not None:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                set_coming_time(self.tl.staff_id, date_time_str)
            finally:
                self.ui.tblWeek.updateForCurrentWeek()
                QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def setNewLeavingTime(self):
        date_time_str = GetDateTime(caption=u'Время ухода')
        if date_time_str is not None:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                set_leaving_time(self.tl.staff_id, date_time_str)
            finally:
                self.ui.tblWeek.updateForCurrentWeek()
                QApplication.restoreOverrideCursor()
    
    def changeCaption(self):
        self.setWindowTitle('%s - %s' % (PROGRAM_NAME_FULL, self.ui.tabWidget.tabToolTip(self.ui.tabWidget.currentIndex())))
    
    def setDinnerOrderItemsFromXML(self, xml):
        salad = get_xml_field_value(xml, 'SALAD')
        if salad is not None:
            salad = int(salad)
        else:
            salad = 0
        first = get_xml_field_value(xml, 'FIRST')
        if first is not None:
            first = int(first)
        else:
            first = 0
        second = get_xml_field_value(xml, 'SECOND')
        if second is not None:
            second = int(second)
        else:
            second = 0
        
        if salad:
            self.ui.chkMenuSalad.setCheckState(Qt.Checked)
        else:
            self.ui.chkMenuSalad.setCheckState(Qt.Unchecked)
        if first:
            self.ui.chkMenuFirst.setCheckState(Qt.Checked)
        else:
            self.ui.chkMenuFirst.setCheckState(Qt.Unchecked)
        if second:
            self.ui.chkMenuSecond.setCheckState(Qt.Checked)
        else:
            self.ui.chkMenuSecond.setCheckState(Qt.Unchecked)
    
    def setDinnerOrderItems(self):
        self.setDinnerOrderItemsFromXML(get_dinner_order())
    
    @pyqtSlot()
    def createDinnerOrder(self):
        salad  = 0
        first  = 0
        second = 0
        
        if self.ui.chkMenuSalad.checkState() == Qt.Checked:
            salad  = 1
        if self.ui.chkMenuFirst.checkState() == Qt.Checked:
            first  = 1
        if self.ui.chkMenuSecond.checkState() == Qt.Checked:
            second = 1
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            menu = ''
            if self.new_today_menu is not None:
                menu = prepare_string(self.new_today_menu.encode('utf-8'))
            create_ore_replace_dinner_order(menu, salad, first, second)
        finally:
            QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def updateDinnerOrderPage(self, force=True):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            if (self.new_today_menu is None) or force:
                self.ui.lblTodayMenu.setText(DINNER_LOADING_MESSAGE)
                menu_text = get_today_menu_text()
                if menu_text:
                    self.ui.lblTodayMenu.setText(menu_text)
                    self.new_today_menu = menu_text
                else:
                    self.ui.lblTodayMenu.setText(DINNER_LOADING_FAULT_MESSAGE)
                self.setDinnerOrderItems()
        except Exception as err:
            self.ui.lblTodayMenu.setText(DINNER_LOADING_FAULT_MESSAGE)
            raise RaisedGuiException(err)
        finally:
            QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def printDinnerOrders(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            pdf = generate_dinner_report()
            filename = save_tmp_file(pdf)
            open_file_with_default_app(filename)
        except Exception as err:
            raise RaisedGuiException(err)
        finally:
            QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def tabChanged(self, index):
        self.changeCaption()
        tab = self.ui.tabWidget.widget(index)
        ob_name = tab.objectName()
        # Приход/уход
        if ob_name == 'tabTime':
            if (self.ui.tblWeek.today is None) or (self.ui.tblWeek.today != datetime.date.today()):
                self.ui.tblWeek.updateForCurrentWeek()
        # Обеды
        elif ob_name == 'tabDinner':
            clear_tmp_dir()
            self.updateDinnerOrderPage(force=False)
    
    @pyqtSlot()
    def startSearching(self):
        QObject.emit( self.tl, SIGNAL('stopEditAllItems()') )
        self.ui.txtSearchText.setPalette(self.createDefaultPalette())
        self.ui.searchWidget.show()
        self.ui.txtSearchText.setFocus()
        self.ui.txtSearchText.selectAll()
    
    @pyqtSlot()
    def stopSearching(self):
        QObject.emit( self, SIGNAL('clearAllSearchSelectionsInTaskList()') )
        self.ui.searchWidget.hide()
    
    def createNotFoundPalette(self):
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush = QBrush(QColor(255, 4, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        brush = QBrush(QColor(255, 4, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(169, 167, 167))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(244, 244, 244))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        return palette
    
    def createDefaultPalette(self):
        return self.ui.tabWidget.palette()
    
    @pyqtSlot()
    def searchForText(self, text):
        def highlightLabelIfNeed(label):
            caption = unicode(label.text())
            if txt_u in caption.upper():
                label.highlightText(text)
                return label
        
        QObject.emit( self, SIGNAL('clearAllSearchSelectionsInTaskList()') )
        first_widget = None
        
        try:
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
        except Exception as err:
            raise RaisedGuiException(err)
