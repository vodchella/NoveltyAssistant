# -*- coding: utf-8 -*- 

import datetime
from qt_common          import *
from get_date_time      import GetDateTime
from remote_functions   import set_coming_time, set_leaving_time
from errors             import GuiException

class main_form(QDialog):
    ui = None
    tl = None
    
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
    
    @pyqtSlot()
    def tabChanged(self, index):
        ob_name = self.ui.tabWidget.widget(index).objectName()
        if ob_name == 'tabTime':
            if (self.ui.tblWeek.today is None) or (self.ui.tblWeek.today != datetime.date.today()):
                self.ui.tblWeek.updateForCurrentWeek()
    
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
