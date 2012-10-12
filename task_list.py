# -*- coding: utf-8 -*-

from qt_common          import *
from xml.dom.minidom    import parseString
from xml_utils          import get_node_element_value, dict_to_xml, prepare_string, get_xml_field_value
from str_utils          import ireplace_ex
from remote_functions   import get_worksheets, set_worksheet
from errors             import GuiException
from cache              import getTaskTypes, getCustomers

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

class task_list(QScrollArea):
    main_form = None
    groups  = []
    items   = []
    staff_id = 0
    total_time = 0
    
    def __init__(self,  parent):
        super(task_list, self).__init__(parent)
        self.startEditItem = pyqtSignal()
        self.stopEditAllItems = pyqtSignal()
        self.totalTimeChanged = pyqtSignal()
        self.totalCountChanged = pyqtSignal()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.main_container = QWidget()
        self.setWidget(self.main_container)
        self.vl = QVBoxLayout(self.main_container)
        
        self.container = QWidget(self.main_container)
        self.vl.addWidget(self.container)
        self.vl2 = QVBoxLayout(self.container)
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
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
            QObject.connect( self.main_form, SIGNAL('clearAllSearchSelectionsInTaskList()'), group.label.clearHighlighting )
    
    def removeGroup(self, group_id):
        i_group_id = int(group_id)
        gr = self.getGroupById(i_group_id)
        if gr is not None:
            for item in filter(lambda i: i.group_id == i_group_id, self.items):
                self.removeItem(item.item_index)
            gr.setParent(None)
            del self.groups[gr.group_index],  gr
            self.updateGroupsIndexes()
    
    def getGroupById(self, group_id):
        i_group_id = int(group_id)
        for group in filter(lambda g: g.group_id == i_group_id, self.groups):
            return group
    
    def updateGroupsIndexes(self):
        for index, gr in enumerate(self.groups):
            gr.group_index = index
    
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
            if i_group_id != -1:
                QObject.emit( self, SIGNAL('totalCountChanged()') )
            QObject.emit( self, SIGNAL('totalTimeChanged()') )
            QObject.connect( self, SIGNAL('startEditItem()'), item.stopEdit )
            QObject.connect( self, SIGNAL('stopEditAllItems()'), item.stopEdit )
            QObject.connect( item, SIGNAL('beforeEditItem()'), self.beforeEditNewItem )
            QObject.connect( self.main_form, SIGNAL('clearAllSearchSelectionsInTaskList()'), item.lblDesc.clearHighlighting )
            QObject.connect( self.main_form, SIGNAL('clearAllSearchSelectionsInTaskList()'), item.lblTime.clearHighlighting )
        else:
            raise GuiException('Группа с id равным %i не существует' % i_group_id)
    
    def getItemsCountInGroup(self, group_id):
        i_group_id = int(group_id)
        return len(filter(lambda i: i.group_id == i_group_id, self.items))
    
    def removeItem(self, index):
        item = self.items[index]
        group_id = item.group_id
        
        if group_id != -1:
            items_count_in_group = self.getItemsCountInGroup(group_id)
        
        self.total_time -= item.time_value
        QObject.emit( self, SIGNAL('totalTimeChanged()') )
        
        item.setParent(None)
        del self.items[index], item
        QObject.emit( self, SIGNAL('totalCountChanged()') )
        self.updateItemsIndexes()
        
        if (items_count_in_group == 1) and (group_id != -1):
            self.removeGroup(group_id)
    
    def moveItemToGroup(self, item_index, new_group_id):
        gr = self.getGroupById(new_group_id)
        if gr is not None:
            item = self.items[item_index]
            item.parent = gr
            gr.vl.addWidget(item)
            if (item.group_id == -1) and (new_group_id != -1):
                QObject.emit( self, SIGNAL('totalCountChanged()') )
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
        QObject.emit( self, SIGNAL('totalTimeChanged()') )
        QObject.emit( self, SIGNAL('totalCountChanged()') )
    
    @pyqtSlot()
    def newItem(self):
        self.showNewItemGroup()
        ti = task_item(self)
        ti.setWorksheetId(0)
        self.addItem(ti, -1)
        ti.beginEdit()
    
    @pyqtSlot()
    def updateOnDate(self, date):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.clear()
            
            gr = task_group(self)
            gr.setCaption(u"[Новая задача]")
            self.addGroup(gr, -1)
            gr.hide()
            
            xml_str = get_worksheets(self.staff_id, date)
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
    
    @pyqtSlot()
    def beforeEditNewItem(self):
        QObject.emit( self, SIGNAL('startEditItem()') )
    
    def hideNewItemGroup(self):
        gr = self.getGroupById(-1)
        if gr is not None:
            gr.hide()
    
    def showNewItemGroup(self):
        gr = self.getGroupById(-1)
        if gr is not None:
            gr.show()


class task_group(QFrame):
    group_id    = -1
    group_index = -1
    
    def __init__(self,  parent):
        super(task_group,  self).__init__(parent)
        
        self.vl = QVBoxLayout(self)
        self.vl.setMargin(5)
        self.show()
        
        self.label = task_label(self)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.vl.addWidget(self.label)
    
    def setCaption(self, caption):
        self.label.setText(caption)
    
    def caption(self):
        return self.label.text()


class task_item(QFrame):
    parent_task_list = None
    item_index = -1
    group_id = -1
    task_type_id = -1
    time_value = 0
    worksheet_id = 0
    
    def __init__(self,  parent):
        super(task_item,  self).__init__(parent)
        self.beforeEditItem = pyqtSignal()

        self.pages = QStackedWidget(self)
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.pages)
        self.pages.show()

        self.pgView = QWidget()
        self.pages.addWidget(self.pgView)
        self.vlView = QVBoxLayout(self.pgView)
        self.vlView.setMargin(5)
        self.pgView.show()

        self.lblDesc = task_label(self.pgView)
        QObject.connect( self.lblDesc, SIGNAL('clicked()'), self.beginEdit )
        self.vlView.addWidget(self.lblDesc)
        
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblDesc.setFont(font)
        
        self.lblTime = task_label(self.pgView)
        QObject.connect( self.lblTime, SIGNAL('clicked()'), self.beginEdit )
        self.vlView.addWidget(self.lblTime)
        
        self.frameBottomLine = QFrame(self)
        self.frameBottomLine.setFrameShape(QFrame.HLine)
        self.frameBottomLine.setFrameShadow(QFrame.Raised)
        self.frameBottomLine.show()
        self.vl.addWidget(self.frameBottomLine)
    
    @pyqtSlot()
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
        
        xml_str = dict_to_xml(dict(WORKSHEETS = dict(WORKSHEET = dict(
            WORKSHEET_ID = self.worksheet_id,
            CUSTOMER_ID = new_group_id,
            TASK_TYPE_ID = new_task_type_id,
            DESCRIPTION = prepare_string(new_desc_utf8),
            DURATION = new_time,
            STAFF_ID = self.parent_task_list.staff_id
            ))))

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            result_xml = set_worksheet(xml_str)
            if '<ACTION>INSERTED</ACTION>' in result_xml:
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
    
    @pyqtSlot()
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
    
    @pyqtSlot()
    def beginEdit(self):
        QObject.emit( self, SIGNAL('beforeEditItem()') )
        
        self.pgEdit = QWidget()
        self.pages.addWidget(self.pgEdit)
        self.vlEdit = QVBoxLayout(self.pgEdit)
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
        
        self.txt = QPlainTextEdit(self.pgEdit)
        self.txt.setMaximumSize(QSize(16777215, 100))
        self.txt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.txt.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt.setTabChangesFocus(True)
        self.txt.setPlainText(self.lblDesc.text())
        self.vlEdit.addWidget(self.txt)
        
        self.bottom_frame = QFrame(self.pgEdit)
        self.vlEdit.addWidget(self.bottom_frame)
        
        self.bottom_frame_layout = QHBoxLayout(self.bottom_frame)
        self.txtTime = QSpinBox(self.bottom_frame)
        self.txtTime.setMinimumSize(QSize(70, 0))
        self.txtTime.setMaximum(999999999)
        self.txtTime.setValue(self.time_value)
        self.bottom_frame_layout.addWidget(self.txtTime)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bottom_frame_layout.addItem(spacerItem1)
        self.buttonBox = QDialogButtonBox(self.bottom_frame)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.bottom_frame_layout.addWidget(self.buttonBox)
        
        QObject.connect( self.buttonBox, SIGNAL('rejected()'), self.stopEdit )
        QObject.connect( self.buttonBox, SIGNAL('accepted()'), self.saveData )
        
        self.pages.setCurrentIndex(1)
        self.txt.setFocus(Qt.OtherFocusReason)
        
        self.esc_shortcut = QShortcut(self)
        self.esc_shortcut.setKey(Qt.Key_Escape)
        QObject.connect( self.esc_shortcut, SIGNAL('activated()'), self.stopEdit )
        self.esc_shortcut.setEnabled(True)
        
        self.save_shortcut = QShortcut(self)
        self.save_shortcut.setKey('Ctrl+S')
        QObject.connect( self.save_shortcut, SIGNAL('activated()'), self.saveData )
        self.save_shortcut.setEnabled(True)
        
        self.save_shortcut2 = QShortcut(self)
        self.save_shortcut2.setKey(Qt.Key_Return)
        QObject.connect( self.save_shortcut2, SIGNAL('activated()'), self.saveData )
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
            QObject.emit( self.parent_task_list, SIGNAL('totalTimeChanged()') )
    
    def setDesc(self, desc):
        self.lblDesc.setText(unicode(desc))
    
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


class task_label(QLabel):
    plain_text = ''
    
    def __init__(self,  parent):
        super(task_label,  self).__init__(parent)
        self.setTextFormat(Qt.RichText)
        self.setWordWrap(True)
        self.clicked = pyqtSignal()
    
    def formatHtml(self, html_text):
        return html_text.replace('\n', '<br>')
    
    def setText(self, caption):
        self.plain_text = caption
        super(task_label, self).setText(self.formatHtml(caption))
    
    def text(self):
        return self.plain_text
    
    def highlightText(self, str, backcolor='yellow'):
        super(task_label, self).setText(self.formatHtml(ireplace_ex(self.plain_text, str, u'<font style=background-color:%s>##OLD##</font>' % backcolor)))
    
    @pyqtSlot()
    def clearHighlighting(self):
        super(task_label, self).setText(self.formatHtml(self.plain_text))
    
    def mouseReleaseEvent(self, event):
        QObject.emit( self, SIGNAL('clicked()') )

class tasks_status_label(QLabel):
    task_list = None
    
    def __init__(self,  parent):
        super(tasks_status_label,  self).__init__(parent)
    
    @pyqtSlot()
    def updateStatus(self):
        if self.task_list is not None:
            if self.task_list.total_time != 0:
                self.setText(u'Общее время %s' % getTimeText(self.task_list.total_time))
                self.show()
            else:
                self.setText('')
                self.hide()

class tasks_count_label(QLabel):
    task_list = None
    
    def __init__(self,  parent):
        super(tasks_count_label,  self).__init__(parent)
    
    @pyqtSlot()
    def updateCount(self):
        if self.task_list is not None:
            l = len(self.task_list.items)
            if l != 0:
                self.setText(u'Количество задач: %s' % l)
                self.show()
            else:
                self.setText('')
                self.hide()

class task_combo_box(QComboBox):
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
