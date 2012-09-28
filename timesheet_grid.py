# -*- coding: utf-8 -*-

import datetime

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QTableWidgetItem, QBrush, QColor, QCursor

from xml.dom.minidom import parseString
from xml_utils import *
from remote_functions import *
from constants import *

week_days = [u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресение']
column_captions = [u'Дата', u'День недели', u'Приход', u'Уход']

class timesheet_grid(QtGui.QTableWidget):
    bInitialized = False
    staff_id = 0
    week_dates = []
    red_brush = QBrush(QColor('red'))
    today = 0
    
    def setCellColors(self, row, cell):
        if row > 4:
            cell.setForeground(self.red_brush)
    
    def __init__(self,  parent):
        super(timesheet_grid, self).__init__(parent)
        self.fillWeekDates()
        
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(column_captions)
        red_brush = QBrush(QColor('red'))
        for i in range(0, 7):
            self.insertRow(i)
            
            # Дата
            cell = QTableWidgetItem(self.week_dates[i].strftime('%d.%m.%Y'))
            self.setCellColors(i, cell)
            self.setItem(i, 0, cell)
            
            # День недели
            cell = QTableWidgetItem(week_days[i])
            self.setCellColors(i, cell)
            self.setItem(i, 1, cell)
            
            for j in range(2, 4):                
                cell = QTableWidgetItem('-')
                if i > 4: cell.setForeground(red_brush)
                self.setItem(i, j, cell)
        
        self.bInitialized = True
    
    def fillWeekDates(self):
        self.week_dates = []
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        for i in range(0, 7):
            self.week_dates.append(monday + datetime.timedelta(days=i))
    
    def updateForCurrentWeek(self):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            
            today = datetime.date.today()
            if self.today != today:
                self.fillWeekDates()
            self.today = today
            
            monday = today - datetime.timedelta(days=today.weekday())
            sunday = monday + datetime.timedelta(days=6)
            monday_str = monday.strftime(REMOTE_DATE_FORMAT)
            sunday_str = sunday.strftime(REMOTE_DATE_FORMAT)
            
            xml_str = get_timesheet(self.staff_id, monday_str, sunday_str)
            dom = parseString(xml_str)
            timesheets = dom.getElementsByTagName('TIMESHEET')
            last_table_row = -1
            for timesheet in timesheets:
                beg_datetime = get_node_element_value(timesheet, 'BEG_DATE')
                end_datetime = get_node_element_value(timesheet, 'END_DATE')
                
                cur_date = None
                if beg_datetime is not None:
                    cur_date = datetime.datetime.strptime(beg_datetime[:10], REMOTE_DATE_FORMAT).date()
                elif end_datetime is not None:
                    cur_date = datetime.datetime.strptime(end_datetime[:10], REMOTE_DATE_FORMAT).date()
                
                if cur_date is not None:
                    i = last_table_row
                    for dt in self.week_dates[last_table_row + 1:]:
                        i += 1
                        if dt == cur_date:
                            if beg_datetime is not None:
                                cell_beg = self.item(i, 2)
                                cell_beg.setText(beg_datetime[11:])
                            if end_datetime is not None:
                                cell_end = self.item(i, 3)
                                cell_end.setText(end_datetime[11:])
                            last_table_row = i
                            break
        finally:
            QApplication.restoreOverrideCursor()
    
    def setColumnCount(self, columns):
        if not self.bInitialized:
            super(timesheet_grid, self).setColumnCount(columns)
    
    def setRowCount(self, rows):
        if not self.bInitialized:
            super(timesheet_grid, self).setRowCount(rows)
