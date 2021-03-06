# -*- coding: utf-8 -*-

from datetime   import datetime
from constants  import *
from novelty    import login, get_data_xml, generate_jasper_report_sync
from xml_utils  import get_xml_field_value, dict_to_xml
from errors     import GuiException

def remote_login(u_name, u_pwd):
    return login(u_name, u_pwd)

def get_staff_by_user(user_id):
    result_xml = get_data_xml("GetStaffByUser", dict_to_xml({'PARAMS':{'USER_ID':user_id}}))
    staff_id = int(get_xml_field_value(result_xml, 'RESULT'))
    if staff_id is None:
        raise GuiException('Вы не являетесь сотрудником Novelty')
    return staff_id

def get_worksheets(staff_id, date):
    return get_data_xml("GetWorksheets",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'INPUT_DATE':date.toString('dd.MM.yyyy')}}))

def set_worksheet(xml):
    return get_data_xml('SetWorksheets', xml)

def get_customers():
    return get_data_xml("GetCustomers", "")

def get_task_types():
    return get_data_xml("GetTaskTypes", "")

def get_timesheet(staff_id, date_beg, date_end):
    return get_data_xml("GetTimesheet",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'BEG_DATE':date_beg, 'END_DATE':date_end}}))

def set_coming_time(staff_id, date_time_str):
    return get_data_xml("SetComingTime",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'DATE_TIME':date_time_str}}))

def set_leaving_time(staff_id, date_time_str):
    return get_data_xml("SetLeavingTime",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'DATE_TIME':date_time_str}}))

def get_program_version():
    return int(get_xml_field_value(get_data_xml("GetAssistantVersion", ""), 'VERSION_NUMBER'))

def set_program_version(version_number):
    vn = int(version_number)
    return get_data_xml("SetAssistantVersion", dict_to_xml({'PARAMS':{'VERSION_NUMBER':vn}}))

def get_new_in_version():
    return get_xml_field_value(get_data_xml("GetAssistantVersionDescription", ""), 'VERSION_DESCRIPTION')

def set_new_in_version(txt):
    return get_data_xml("SetAssistantVersionDescription",
        dict_to_xml({'PARAMS':{'VERSION_DESCRIPTION':txt}}))

def get_controllable_services():
    return get_data_xml("GetControllableServices", "")

def create_ore_replace_dinner_order(menu, salad, first, second):
    return get_data_xml("CreateOrReplaceDinnerOrder",
        dict_to_xml({'PARAMS':{'MENU':menu, 'ORDER':{'SALAD':salad, 'FIRST':first, 'SECOND':second}}}))

def get_dinner_order():
    return get_data_xml("GetDinnerOrder", "")

def get_dinner_order_permissions():
    return get_data_xml("GetDinnerOrderPermissions", "")

def get_directories_changed_at():
    xml = get_data_xml("GetDirectoriesChangedAt", "")
    result = {}
    result['server_time'] = datetime.strptime(get_xml_field_value(xml, 'SERVER_TIME'), REMOTE_DATETIME_FORMAT)
    result['customers_changed_at']  = datetime.strptime(get_xml_field_value(xml, 'CUSTOMERS_CHANGED_AT'), REMOTE_DATETIME_FORMAT)
    result['task_types_changed_at'] = datetime.strptime(get_xml_field_value(xml, 'TASK_TYPES_CHANGED_AT'), REMOTE_DATETIME_FORMAT)
    return result

def generate_dinner_report():
    return generate_jasper_report_sync(DINNER_REPORT_ID, "<param name='aOrderDate' type='date'>%s</param>" % (datetime.now().strftime(REMOTE_DATE_FORMAT)))
    
def get_dinner_paths():
    return get_xml_field_value(get_data_xml("GetDinnerPaths", ""), 'PATHS').split()
