# -*- coding: utf-8 -*-

from novelty import *
from xml_utils import *
from errors import GuiException

def remoteLogin(u_name, u_pwd):
    return login(u_name, u_pwd)

def getStaffByUser(user_id):
    result_xml = get_data_xml("GetStaffByUser", "<PARAMS><USER_ID>%s</USER_ID></PARAMS>" % user_id)
    staff_id = int(get_xml_field_value(result_xml, 'RESULT'))
    if staff_id is None:
        raise GuiException('Вы не являетесь сотрудником Novelty')
    return staff_id

def getWorksheetsXML(staff_id, date):
    return get_data_xml("GetWorksheets", "<PARAMS><STAFF_ID>%s</STAFF_ID><INPUT_DATE>%s</INPUT_DATE></PARAMS>" % (staff_id, date.toString('dd.MM.yyyy')))

def setWorksheetXML(xml):
    get_data_xml('SetWorksheets', xml)

def getCustomersXML():
    return get_data_xml("GetCustomers", "")

def getTaskTypesXML():
    return get_data_xml("GetTaskTypes", "")
