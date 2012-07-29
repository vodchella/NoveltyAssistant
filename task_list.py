# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCursor

from xml.dom.minidom import parseString
from xml_utils import *
from remote_functions import *
from errors import GuiException
from cache import *

def getTimeText(minutes):
    m = int(minutes)
    if m < 60:
        return u'%s мин.' % m
    else:
        hours = m // 60
        minutes_remainder = m % 60
        if minutes_remainder == 0:
            return u'%s ч.' % hours
        else:
            return u'%s ч. %s мин.' % (hours, minutes_remainder)

class task_list(QtGui.QScrollArea):
    groups  = []
    items   = []
    staff_id = 0
    total_time = 0
    
    def __init__(self,  parent):
        super(task_list, self).__init__(parent)
        self.startEditNewItem = QtCore.pyqtSignal()
        self.totalTimeChanged = QtCore.pyqtSignal()

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.main_container = QtGui.QWidget()
        self.setWidget(self.main_container)
        self.vl = QtGui.QVBoxLayout(self.main_container)
        
        self.container = QtGui.QWidget(self.main_container)
        self.vl.addWidget(self.container)
        self.vl2 = QtGui.QVBoxLayout(self.container)
        self.spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vl.addItem(self.spacer)

        self.show()
    
    def addGroup(self, group, group_id):
        i_group_id = int(group_id)
        if self.getGroupById(i_group_id) is None:
            group.parent = self.container
            group.group_id = i_group_id
            self.vl2.addWidget(group)
            self.groups.append(group)
            group.group_index = len(self.groups) - 1
    
    def removeGroup(self, group_id):
        i_group_id = int(group_id)
        gr = self.getGroupById(i_group_id)
        if gr is not None:
            for item in self.items:
                if item.group_id == i_group_id:
                    self.removeItem(item.item_index)
            gr.setParent(None)
            del self.groups[gr.group_index],  gr
            self.updateGroupsIndexes()
    
    def getGroupById(self, group_id):
        i_group_id = int(group_id)
        for gr in self.groups:
            if gr.group_id == i_group_id:
                return gr
    
    def updateGroupsIndexes(self):
        index = 0
        for gr in self.groups:
            gr.group_index = index
            index += 1
    
    def addItem(self, item, group_id):
        i_group_id = int(group_id)
        gr = self.getGroupById(i_group_id)
        if gr is not None:
            item.parent = gr
            gr.vl.addWidget(item)
            self.items.append(item)
            item.parent_task_list = self
            item.item_index = len(self.items) - 1
            item.group_id = i_group_id
            self.total_time += item.time_value
            QtCore.QObject.emit( self, QtCore.SIGNAL('totalTimeChanged()') )
            QtCore.QObject.connect( self, QtCore.SIGNAL('startEditNewItem()'), item.stopEdit )
            QtCore.QObject.connect( item, QtCore.SIGNAL('beforeEditItem()'), self.beforeEditNewItem )
        else:
            raise GuiException('Группа с id равным %i не существует' % i_group_id)
    
    def getItemsCountInGroup(self, group_id):
        i_group_id = int(group_id)
        items_count_in_group = 0
        for i in self.items:
            if i.group_id == i_group_id:
                items_count_in_group += 1
        return items_count_in_group
    
    def removeItem(self, index):
        item = self.items[index]
        group_id = item.group_id
        
        if group_id != -1:
            items_count_in_group = self.getItemsCountInGroup(group_id)
        
        self.total_time -= item.time_value
        QtCore.QObject.emit( self, QtCore.SIGNAL('totalTimeChanged()') )
        
        item.setParent(None)
        del self.items[index], item
        self.updateItemsIndexes()
        
        if (items_count_in_group == 1) and (group_id != -1):
            self.removeGroup(group_id)
    
    def moveItemToGroup(self, item_index, new_group_id):
        gr = self.getGroupById(new_group_id)
        if gr is not None:
            item = self.items[item_index]
            item.parent = gr
            gr.vl.addWidget(item)
            item.group_id = new_group_id
    
    def updateItemsIndexes(self):
        index = 0
        for i in self.items:
            i.item_index = index
            index += 1

    def clear(self):
        for i in range(len(self.items) - 1, -1, -1):
            item = self.items[i]
            item.setParent(None)
            del self.items[i]
        for i in range(len(self.groups) - 1, -1, -1):
            group = self.groups[i]
            group.setParent(None)
            del self.groups[i]
        self.total_time = 0
        QtCore.QObject.emit( self, QtCore.SIGNAL('totalTimeChanged()') )
    
    @QtCore.pyqtSlot()
    def newItem(self):
        self.showNewItemGroup()
        ti = task_item(self)
        ti.setWorksheetId(0)
        self.addItem(ti, -1)
        ti.beginEdit()
    
    @QtCore.pyqtSlot()
    def updateOnDate(self, date):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.clear()
            
            gr = task_group(self)
            gr.setCaption(u'<Новая задача>')
            self.addGroup(gr, -1)
            gr.hide()
            
            xml_str = getWorksheetsXML(self.staff_id, date)
#            xml_str = """<WORKSHEETS><WORKSHEET><WORKSHEET_ID>3020</WORKSHEET_ID><CUSTOMER_ID>28</CUSTOMER_ID><CUSTOMER_NAME>NOVELTY</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>Интеграция с home.novelty. Добавлены методы GetWorksheets() и SetWorksheets() для управления отчётами о проделанной работе</DESCRIPTION><DURATION>215</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:32:46</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3021</WORKSHEET_ID><CUSTOMER_ID>28</CUSTOMER_ID><CUSTOMER_NAME>NOVELTY</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>Оптимизирован механизм аутентификации в пакете novelty_home_integration</DESCRIPTION><DURATION>80</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:33:36</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3022</WORKSHEET_ID><CUSTOMER_ID>7</CUSTOMER_ID><CUSTOMER_NAME>ЦЕСНА ГАРАНТ СК</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>2012062613000331</DESCRIPTION><DURATION>40</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:34:08</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3023</WORKSHEET_ID><CUSTOMER_ID>5</CUSTOMER_ID><CUSTOMER_NAME>НОМАД ИНШУРАНС</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>2012061813000187</DESCRIPTION><DURATION>15</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:35:39</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3024</WORKSHEET_ID><CUSTOMER_ID>2</CUSTOMER_ID><CUSTOMER_NAME>АСБ</CUSTOMER_NAME><TASK_TYPE_ID>10</TASK_TYPE_ID><TASK_TYPE_NAME>Решение инцидента (Служба поддержки)</TASK_TYPE_NAME><DESCRIPTION>2012062613000313</DESCRIPTION><DURATION>10</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:36:09</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3025</WORKSHEET_ID><CUSTOMER_ID>2</CUSTOMER_ID><CUSTOMER_NAME>АСБ</CUSTOMER_NAME><TASK_TYPE_ID>10</TASK_TYPE_ID><TASK_TYPE_NAME>Решение инцидента (Служба поддержки)</TASK_TYPE_NAME><DESCRIPTION>2012062613000322</DESCRIPTION><DURATION>10</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:36:45</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3026</WORKSHEET_ID><CUSTOMER_ID>7</CUSTOMER_ID><CUSTOMER_NAME>ЦЕСНА ГАРАНТ СК</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>2012062613000341</DESCRIPTION><DURATION>20</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:38:09</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3027</WORKSHEET_ID><CUSTOMER_ID>31</CUSTOMER_ID><CUSTOMER_NAME>KOMPETENZ</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>2012062713000188</DESCRIPTION><DURATION>5</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:39:52</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3028</WORKSHEET_ID><CUSTOMER_ID>9</CUSTOMER_ID><CUSTOMER_NAME>АЛЬЯНС ПОЛИС СК</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>2012062713000295</DESCRIPTION><DURATION>10</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:40:16</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3029</WORKSHEET_ID><CUSTOMER_ID>8</CUSTOMER_ID><CUSTOMER_NAME>АСКО СК</CUSTOMER_NAME><TASK_TYPE_ID>2</TASK_TYPE_ID><TASK_TYPE_NAME>Разработка (программирование)</TASK_TYPE_NAME><DESCRIPTION>2012062713000124</DESCRIPTION><DURATION>10</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:40:40</INPUT_DATE></WORKSHEET><WORKSHEET><WORKSHEET_ID>3030</WORKSHEET_ID><CUSTOMER_ID>8</CUSTOMER_ID><CUSTOMER_NAME>АСКО СК</CUSTOMER_NAME><TASK_TYPE_ID>14</TASK_TYPE_ID><TASK_TYPE_NAME>Перенос функционала (обновление)</TASK_TYPE_NAME><DESCRIPTION>2012062713000124 Перенос на боевую</DESCRIPTION><DURATION>10</DURATION><STAFF_ID>18</STAFF_ID><STAFF_NAME>Павлов Максим Андреевич</STAFF_NAME><INPUT_DATE>27.06.2012 19:41:03</INPUT_DATE></WORKSHEET></WORKSHEETS>"""
            dom = parseString(xml_str)
            worksheets = dom.getElementsByTagName('WORKSHEET')
            for worksheet in worksheets:
                group_id = get_node_element_value(worksheet, 'CUSTOMER_ID')
                if self.getGroupById(group_id) is None:
                    gr = task_group(self)
                    gr.setCaption(get_node_element_value(worksheet, 'CUSTOMER_NAME'))
                    self.addGroup(gr, group_id)
                ti = task_item(self)
                ti.setWorksheetId(get_node_element_value(worksheet, 'WORKSHEET_ID'))
                ti.setTime(get_node_element_value(worksheet, 'DURATION'))
                ti.setDesc(get_node_element_value(worksheet, 'DESCRIPTION'))
                ti.setTaskType(int(get_node_element_value(worksheet, 'TASK_TYPE_ID')))
                self.addItem(ti, group_id)
            if 'ti' in locals():
                del ti
            if 'gr' in locals():
                del gr
        finally:
            QApplication.restoreOverrideCursor()
    
    @QtCore.pyqtSlot()
    def beforeEditNewItem(self):
        QtCore.QObject.emit( self, QtCore.SIGNAL('startEditNewItem()') )
    
    def hideNewItemGroup(self):
        gr = self.getGroupById(-1)
        if gr is not None:
            gr.hide()
    
    def showNewItemGroup(self):
        gr = self.getGroupById(-1)
        if gr is not None:
            gr.show()


class task_group(QtGui.QFrame):
    group_id    = -1
    group_index = -1
    
    def __init__(self,  parent):
        super(task_group,  self).__init__(parent)
        
        self.vl = QtGui.QVBoxLayout(self)
        self.vl.setMargin(5)
        self.show()
        
        self.label = QtGui.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.vl.addWidget(self.label)
    
    def setCaption(self, caption):
        self.label.setText(caption)


class task_item(QtGui.QFrame):
    parent_task_list = None
    item_index = -1
    group_id = -1
    task_type_id = -1
    time_value = 0
    worksheet_id = 0
    
    def __init__(self,  parent):
        super(task_item,  self).__init__(parent)
        self.beforeEditItem = QtCore.pyqtSignal()

        self.pages = QtGui.QStackedWidget(self)
        self.vl = QtGui.QVBoxLayout(self)
        self.vl.addWidget(self.pages)
        self.pages.show()

        self.pgView = QtGui.QWidget()
        self.pages.addWidget(self.pgView)
        self.vlView = QtGui.QVBoxLayout(self.pgView)
        self.vlView.setMargin(5)
        self.pgView.show()

        self.lblDesc = task_label(self.pgView)
        self.lblDesc.setTextFormat(QtCore.Qt.PlainText)
        self.lblDesc.setWordWrap(True)
        QtCore.QObject.connect( self.lblDesc, QtCore.SIGNAL('clicked()'), self.beginEdit )
        self.vlView.addWidget(self.lblDesc)
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblDesc.setFont(font)
        
        self.lblTime = task_label(self.pgView)
        QtCore.QObject.connect( self.lblTime, QtCore.SIGNAL('clicked()'), self.beginEdit )
        self.vlView.addWidget(self.lblTime)
        
        self.frameBottomLine = QtGui.QFrame(self)
        self.frameBottomLine.setFrameShape(QtGui.QFrame.HLine)
        self.frameBottomLine.setFrameShadow(QtGui.QFrame.Raised)
        self.frameBottomLine.show()
        self.vl.addWidget(self.frameBottomLine)
    
    @QtCore.pyqtSlot()
    def saveData(self):
        self.buttonBox.setFocus()
        self.cboCustomer.validateValue()
        self.cboTaskType.validateValue()
        new_desc = self.txt.toPlainText().trimmed()
        new_desc_utf8 = new_desc.toUtf8()
        if new_desc.length() == 0:
            self.txt.setFocus()
            raise GuiException('Укажите описание выполненных работ')
        
        new_group_id = self.cboCustomer.itemData(self.cboCustomer.currentIndex()).toInt()[0]
        new_task_type_id = self.cboTaskType.itemData(self.cboTaskType.currentIndex()).toInt()[0]
        new_time = self.txtTime.value()
        
        xml_str = \
        """<WORKSHEETS>
                <WORKSHEET>
                    <WORKSHEET_ID>%i</WORKSHEET_ID>
                    <CUSTOMER_ID>%i</CUSTOMER_ID>
                    <TASK_TYPE_ID>%i</TASK_TYPE_ID>
                    <DESCRIPTION>%s</DESCRIPTION>
                    <DURATION>%i</DURATION>
                    <STAFF_ID>%i</STAFF_ID>
                </WORKSHEET>
            </WORKSHEETS>""" % (self.worksheet_id,
                                new_group_id,
                                new_task_type_id,
                                prepareString(new_desc_utf8),
                                new_time,
                                self.parent_task_list.staff_id)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            result_xml = setWorksheetXML(xml_str)
            if result_xml.find('<ACTION>INSERTED</ACTION>') != -1:
                self.worksheet_id = int(get_xml_field_value(result_xml, 'WORKSHEET_ID'))
        finally:
            QApplication.restoreOverrideCursor()
        
        if new_group_id != self.group_id:
            gr = self.parent_task_list.getGroupById(new_group_id)
            if gr is None:
                group_name = getCustomerNameById(new_group_id)
                if group_name is None:
                    raise GuiException('Заказчик с ID равным %i не существет' % new_group_id)
                gr = task_group(self.parent_task_list)
                gr.setCaption(group_name)
                self.parent_task_list.addGroup(gr, new_group_id)
            old_group_id = self.group_id
            self.parent_task_list.moveItemToGroup(self.item_index, new_group_id)
            if self.parent_task_list.getItemsCountInGroup(old_group_id) == 0:
                if old_group_id != -1:
                    self.parent_task_list.removeGroup(old_group_id)
                else:
                    self.parent_task_list.hideNewItemGroup()
        
        self.setTaskType(new_task_type_id)
        self.setDesc(new_desc)
        self.setTime(new_time)
        
        self.stopEdit()
    
    @QtCore.pyqtSlot()
    def stopEdit(self):
        try:
            self.esc_shortcut.setEnabled(False)
            self.esc_shortcut = None
            self.save_shortcut.setEnabled(False)
            self.save_shortcut = None
            self.pgEdit.setParent(None)
            del self.pgEdit
            
            if self.group_id == -1:
                self.parent_task_list.hideNewItemGroup()
                self.parent_task_list.removeItem(self.item_index)
        except:
            pass
    
    @QtCore.pyqtSlot()
    def beginEdit(self):
        QtCore.QObject.emit( self, QtCore.SIGNAL('beforeEditItem()') )
        
        self.pgEdit = QtGui.QWidget()
        self.pages.addWidget(self.pgEdit)
        self.vlEdit = QtGui.QVBoxLayout(self.pgEdit)
        self.vlEdit.setMargin(5)
        self.pgEdit.show()
        
        self.cboCustomer = task_combo_box(self.pgEdit)
        self.cboCustomer.setEditable(True)
        self.cboCustomer.setFrame(True)
        self.vlEdit.addWidget(self.cboCustomer)
        for customer in getCustomers():
            self.cboCustomer.addItem(customer[1], customer[0])
            if customer[0] == self.group_id:
                self.cboCustomer.setCurrentIndex(self.cboCustomer.count() - 1)
        if self.group_id == -1:
            self.cboCustomer.setEditText('')
        
        self.cboTaskType = task_combo_box(self.pgEdit)
        self.cboTaskType.setEditable(True)
        self.cboTaskType.setFrame(True)
        self.vlEdit.addWidget(self.cboTaskType)
        for task_type in getTaskTypes():
            self.cboTaskType.addItem(task_type[1], task_type[0])
            if task_type[0] == self.task_type_id:
                self.cboTaskType.setCurrentIndex(self.cboTaskType.count() - 1)
        if self.group_id == -1:
            self.cboTaskType.setEditText('')
        
        self.txt = QtGui.QPlainTextEdit(self.pgEdit)
        self.txt.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txt.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txt.setTabChangesFocus(True)
        self.txt.setPlainText(self.lblDesc.text())
        self.vlEdit.addWidget(self.txt)
        
        self.bottom_frame = QtGui.QFrame(self.pgEdit)
        self.vlEdit.addWidget(self.bottom_frame)
        
        self.bottom_frame_layout = QtGui.QHBoxLayout(self.bottom_frame)
        self.txtTime = QtGui.QSpinBox(self.bottom_frame)
        self.txtTime.setMinimumSize(QtCore.QSize(70, 0))
        self.txtTime.setMaximum(999999999)
        self.txtTime.setValue(self.time_value)
        self.bottom_frame_layout.addWidget(self.txtTime)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.bottom_frame_layout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(self.bottom_frame)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.bottom_frame_layout.addWidget(self.buttonBox)
        
        QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL('rejected()'), self.stopEdit )
        QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL('accepted()'), self.saveData )
        
        self.pages.setCurrentIndex(1)
        self.txt.setFocus(Qt.OtherFocusReason)
        
        self.esc_shortcut = QtGui.QShortcut(self)
        self.esc_shortcut.setKey(Qt.Key_Escape)
        QtCore.QObject.connect( self.esc_shortcut, QtCore.SIGNAL('activated()'), self.stopEdit )
        self.esc_shortcut.setEnabled(True)
        
        self.save_shortcut = QtGui.QShortcut(self)
        self.save_shortcut.setKey('Ctrl+S')
        QtCore.QObject.connect( self.save_shortcut, QtCore.SIGNAL('activated()'), self.saveData )
        self.save_shortcut.setEnabled(True)
        
        self.save_shortcut2 = QtGui.QShortcut(self)
        self.save_shortcut2.setKey(Qt.Key_Return)
        QtCore.QObject.connect( self.save_shortcut2, QtCore.SIGNAL('activated()'), self.saveData )
        self.save_shortcut2.setEnabled(True)
        
        if self.group_id == -1:
            self.cboCustomer.setFocus()
        
        self.parent_task_list.ensureWidgetVisible(self)
    
    def setTime(self, minutes):
        new_time = int(minutes)
        old_time = self.time_value
        self.time_value = new_time
        self.lblTime.setText(getTimeText(new_time))
        if self.parent_task_list is not None:
            self.parent_task_list.total_time -= old_time
            self.parent_task_list.total_time += new_time
            QtCore.QObject.emit( self.parent_task_list, QtCore.SIGNAL('totalTimeChanged()') )
    
    def setDesc(self, desc):
        self.lblDesc.setText(desc)
    
    def setTaskType(self, task_type_id):
        self.task_type_id = int(task_type_id)
    
    def setWorksheetId(self, worksheet_id):
        i_worksheet_id = int(worksheet_id)
        self.worksheet_id = i_worksheet_id
    
    def setSeparatorVisible(self, visible):
        if visible == True:
            self.frameBottomLine.show()
        else:
            self.frameBottomLine.hide()


class task_label(QtGui.QLabel):
    def __init__(self,  parent):
        super(task_label,  self).__init__(parent)
        self.clicked = QtCore.pyqtSignal()
    
    def mouseReleaseEvent(self, event):
        QtCore.QObject.emit( self, QtCore.SIGNAL('clicked()') )

class tasks_status_label(QtGui.QLabel):
    task_list = None
    
    def __init__(self,  parent):
        super(tasks_status_label,  self).__init__(parent)
    
    @QtCore.pyqtSlot()
    def updateStatus(self):
        if self.task_list is not None:
            if self.task_list.total_time != 0:
                self.setText(u'Общее время %s' % getTimeText(self.task_list.total_time))
                self.show()
            else:
                self.setText('')
                self.hide()

class task_combo_box(QtGui.QComboBox):
    def __init__(self,  parent):
        super(task_combo_box,  self).__init__(parent)
    
    def validateValue(self):
        txt = self.currentText()
        if txt.trimmed().length() == 0:
            self.setFocus()
            raise GuiException('Введите значение')
        if txt != self.itemText(self.currentIndex()):
            self.setFocus()
            raise GuiException('Введённое значение отсутствует в списке')
