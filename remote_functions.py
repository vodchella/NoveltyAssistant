# -*- coding: utf-8 -*-

from novelty    import login, get_data_xml
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
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'INPUT_DATE':date.toString('dd.MM.yyyy')}})
        )

def set_worksheet(xml):
    return get_data_xml('SetWorksheets', xml)

def get_customers():
    return get_data_xml("GetCustomers", "")

def get_task_types():
    return get_data_xml("GetTaskTypes", "")

def get_timesheet(staff_id, date_beg, date_end):
    return get_data_xml("GetTimesheet",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'BEG_DATE':date_beg, 'END_DATE':date_end}})
        )

def set_coming_time(staff_id, date_time_str):
    return get_data_xml("SetComingTime",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'DATE_TIME':date_time_str}})
        )

def set_leaving_time(staff_id, date_time_str):
    return get_data_xml("SetLeavingTime",
        dict_to_xml({'PARAMS':{'STAFF_ID':staff_id, 'DATE_TIME':date_time_str}})
        )

def get_program_version():
    return int(get_xml_field_value(get_data_xml("GetAssistantVersion", ""), 'VERSION_NUMBER'))

def set_program_version(version_number):
    vn = int(version_number)
    return get_data_xml("SetAssistantVersion", dict_to_xml({'PARAMS':{'VERSION_NUMBER':vn}}))

def get_new_in_version():
    return get_xml_field_value(get_data_xml("GetAssistantVersionDescription", ""), 'VERSION_DESCRIPTION')

def set_new_in_version(txt):
    return get_data_xml("SetAssistantVersionDescription",
        dict_to_xml({'PARAMS':{'VERSION_DESCRIPTION':txt}})
        )
