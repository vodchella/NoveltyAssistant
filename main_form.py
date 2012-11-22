# -*- coding: utf-8 -*-

import datetime
from qt_common          import *
from constants          import *
from get_date_time      import GetDateTime
from remote_functions   import set_coming_time, set_leaving_time, get_dinner_order
from errors             import GuiException, RaisedGuiException
from dinner             import get_today_menu
from xml_utils          import get_xml_field_value

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
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                if self.new_today_menu is None:
                    self.ui.lblTodayMenu.setText(DINNER_LOADING_MESSAGE)
                    xml = get_dinner_order()
                    today_menu = get_today_menu()
                    menu_text = '\n'.join(today_menu).decode('utf-8')
                    if today_menu:
                        self.ui.lblTodayMenu.setText(menu_text)
                        self.new_today_menu = menu_text
                    else:
                        self.ui.lblTodayMenu.setText(DINNER_LOADING_FAULT_MESSAGE)
                    self.setDinnerOrderItemsFromXML(xml)
                
            except Exception as err:
                self.ui.lblTodayMenu.setText(DINNER_LOADING_FAULT_MESSAGE)
                raise RaisedGuiException(err)
            finally:
                QApplication.restoreOverrideCursor()
    
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
