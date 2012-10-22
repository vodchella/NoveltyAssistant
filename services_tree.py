# -*- coding: utf-8 -*-

from xml.dom.minidom    import parseString
from constants          import *
from xml_utils          import get_node_element_value, get_xml_field_value
from qt_common          import *
from errors             import RaisedGuiException, GuiException
from remote_functions   import get_controllable_services
from novelty            import remote_call_ex, authenticate

class server_data():
    server  = None
    port    = 0
    use_ssl = False

class service_data():
    service_name = None

class services_tree(QTreeWidget):
    SERVICE_ACTION_START    = 1
    SERVICE_ACTION_STOP     = 2
    SERVICE_ACTION_RESTART  = 3
    
    user_id = 0
    service_menu = None
    bInitialized = False
    count = 0
    
    def __init__(self,  parent):
        super(services_tree, self).__init__(parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setIconSize(QSize(32, 32))
        
        menu = QMenu()
        act = menu.addAction(u'Запустить')
        act.triggered.connect(self.startService)
        act = menu.addAction(u'Остановить')
        act.triggered.connect(self.stopService)
        menu.addSeparator()
        act = menu.addAction(u'Перезапустить')
        act.triggered.connect(self.restartService)
        self.service_menu = menu
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect( self, SIGNAL('customContextMenuRequested(QPoint)'), self.popupMenu )
        
        self.bInitialized = True
    
    def doServiceAction(self, action):
        global session_id
        
        item = self.currentItem()
        if item is not None:
            parent = item.parent()
            if parent is not None:
                server_data  = parent.data(0, Qt.UserRole).toPyObject()
                service_data = item.data(0, Qt.UserRole).toPyObject()
                
                if action == self.SERVICE_ACTION_START:
                    cmd_str = 'startService'
                elif action == self.SERVICE_ACTION_STOP:
                    cmd_str = 'stopService'
                elif action == self.SERVICE_ACTION_RESTART:
                    cmd_str = 'restartService'
                else:
                    raise GuiException(u'Неизвестная команда')
                
                try:
                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    xml = remote_call_ex(cmd_str,
                                         dict(serviceName=service_data.service_name,
                                              sessionID=authenticate()),
                                         server_data.server,
                                         server_data.port,
                                         server_data.use_ssl)
                    QApplication.restoreOverrideCursor()
                    result = get_xml_field_value(xml, 'return')
                    if result is not None:
                        result = result.strip()
                    if result:
                        raise GuiException(result)
                    else:
                        QMessageBox.information(None, PROGRAM_NAME, u'Операция завершена успешно', QMessageBox.Ok)
                finally:
                    QApplication.restoreOverrideCursor()
    
    @pyqtSlot()
    def startService(self):
        self.doServiceAction(self.SERVICE_ACTION_START)
    
    @pyqtSlot()
    def stopService(self):
        self.doServiceAction(self.SERVICE_ACTION_STOP)
    
    @pyqtSlot()
    def restartService(self):
        self.doServiceAction(self.SERVICE_ACTION_RESTART)
    
    @pyqtSlot()
    def popupMenu(self, point):
        item = self.itemAt(point)
        if item is not None:
            if item.parent() is not None:
                self.service_menu.exec_(QCursor.pos())
    
    def getItemsCount(self):
        return self.count
    
    def updateServices(self):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            super(services_tree, self).clear()
            self.count = 0
            
            xml_str = get_controllable_services()
            #xml_str = '<?xml version="1.0" encoding="utf-8"?><SERVERS><SERVER><SERVER_NAME>developer</SERVER_NAME><SERVER_ADDRESS>developer.novelty.local</SERVER_ADDRESS><WEBSERVICE_PORT>28110</WEBSERVICE_PORT><SSL_BOOL>1</SSL_BOOL><SERVICES><SERVICE><SERVICE_NAME>NoveltyInsurance_ADV</SERVICE_NAME><DISPLAY_NAME>adv</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_AF</SERVICE_NAME><DISPLAY_NAME>standard</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_ALLIANZ</SERVICE_NAME><DISPLAY_NAME>kompetenz</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_ALP</SERVICE_NAME><DISPLAY_NAME>alp</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_ALPLIFE</SERVICE_NAME><DISPLAY_NAME>alliance_life</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_AMANAT</SERVICE_NAME><DISPLAY_NAME>amanat</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_ASKO</SERVICE_NAME><DISPLAY_NAME>asko</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_CESNA</SERVICE_NAME><DISPLAY_NAME>cesna</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_ESBD</SERVICE_NAME><DISPLAY_NAME>esbd</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_EUR</SERVICE_NAME><DISPLAY_NAME>eur</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_INTER</SERVICE_NAME><DISPLAY_NAME>interteach</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_NOMAD</SERVICE_NAME><DISPLAY_NAME>nomad</DISPLAY_NAME></SERVICE><SERVICE><SERVICE_NAME>NoveltyInsurance_SAYA</SERVICE_NAME><DISPLAY_NAME>saya</DISPLAY_NAME></SERVICE></SERVICES></SERVER><SERVER><SERVER_NAME>public</SERVER_NAME><SERVER_ADDRESS>test.novelty.kz</SERVER_ADDRESS><WEBSERVICE_PORT>28110</WEBSERVICE_PORT><SSL_BOOL>1</SSL_BOOL><SERVICES></SERVICES></SERVER><SERVER><SERVER_NAME>app01</SERVER_NAME><SERVER_ADDRESS>home2.novelty.kz</SERVER_ADDRESS><WEBSERVICE_PORT>28110</WEBSERVICE_PORT><SSL_BOOL>1</SSL_BOOL><SERVICES></SERVICES></SERVER><SERVER><SERVER_NAME>app02</SERVER_NAME><SERVER_ADDRESS>home.novelty.kz</SERVER_ADDRESS><WEBSERVICE_PORT>28110</WEBSERVICE_PORT><SSL_BOOL>1</SSL_BOOL><SERVICES></SERVICES></SERVER></SERVERS>'
            dom = parseString(xml_str)
            servers = dom.getElementsByTagName('SERVER')
            if servers is not None:
                iconServer = QIcon()
                iconServer.addPixmap(QPixmap(":/images/server_32.ico"), QIcon.Normal, QIcon.Off)
                iconService = QIcon()
                iconService.addPixmap(QPixmap(":/images/service_32.ico"), QIcon.Normal, QIcon.Off)
                for server in servers:
                    data = server_data()
                    data.server   = unicode(get_node_element_value(server, 'SERVER_ADDRESS'))
                    data.port     = int(get_node_element_value(server, 'WEBSERVICE_PORT'))
                    data.use_ssl  = int(get_node_element_value(server, 'SSL_BOOL')) != 0
                    server_name   = get_node_element_value(server, 'SERVER_NAME')
                    
                    itemServer = QTreeWidgetItem(self)
                    itemServer.setIcon(0, iconServer)
                    itemServer.setText(0, server_name)
                    itemServer.setData(0, Qt.UserRole, QVariant(data))
                    
                    self.count += 1
                    
                    services = server.getElementsByTagName('SERVICE')
                    for service in services:
                        data = service_data()
                        data.service_name = unicode(get_node_element_value(service, 'SERVICE_NAME'))
                        display_name = get_node_element_value(service, 'DISPLAY_NAME')
                        
                        itemService = QTreeWidgetItem(itemServer)
                        itemService.setIcon(0, iconService)
                        itemService.setText(0, display_name)
                        itemService.setData(0, Qt.UserRole, QVariant(data))
                        
                        self.count += 1
            
        except Exception as err:
            raise RaisedGuiException(err)
        finally:
            QApplication.restoreOverrideCursor()
    
    def setEditTriggers(self, value):
        if not self.bInitialized:
            super(services_tree, self).setEditTriggers(value)
    
    def setIconSize(self, size):
        if not self.bInitialized:
            super(services_tree, self).setIconSize(size)
