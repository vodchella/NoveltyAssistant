# -*- coding: utf-8 -*-

import httplib
import base64

from xml_utils import *
from errors import GuiException

HOST = 'home2.novelty.kz:28110'
URL = '/WebBridge/WebBridge'

xml_template = \
"""<?xml version = "1.0" encoding = "UTF8" ?>
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
   <S:Body>
     <ns2:%(function)s xmlns:ns2="http://ws.novelty.kz/">
       %(param_list)s
     </ns2:%(function)s>
   </S:Body>
</S:Envelope>"""

session_id = ''
user_name = ''
user_pass = ''
user_id = 0

def request(xml, SOAPAction):
    global session_id

    h = httplib.HTTPSConnection(HOST)
    headers = {
        'Host':HOST,
        'Content-Type':'text/xml; charset=utf-8',
        'Content-Length':len(xml),
        'SOAPAction':'"https://WebBridge.novelty.kz/%s"' % SOAPAction,
        }
    try:
        h.request ('POST', URL, body=xml, headers=headers)
    except:
        raise GuiException('Невозможно установить соединение с БД')
    r = h.getresponse()
    d = r.read()

    err = get_xml_field_value(d, 'faultstring')
    if err is None:
        err = get_xml_field_value(d, 'ErrorMessage')

    if err is not None:
        if err.find('java.lang.Exception: Сессия не определена') != -1:
            session_id = ''
            return request(replace_field_in_xml(xml, 'aSessionID', authenticate()), SOAPAction)
        else:
            raise GuiException(err)

    return d

def remote_call(function, params):
    xml = xml_template % {'function':function, 'param_list':dict_to_xml(params)}
    return request(xml, function)

def authenticate():
    global session_id, user_id

    if len(session_id) == 0:
        param = dict(aName = user_name, aPassword = user_pass, aAlias = 'home')
        result_xml = remote_call('authenticateUser', param)
        session_id = get_xml_field_value(result_xml, 'sessionID')
        if session_id is not None:
            user_id = get_xml_field_value(result_xml, 'ID')
        else:
            raise GuiException("Не удалось получить идентификатор сессии после авторизации")

    return session_id

def get_data_xml(request_type, xml):
    try:
        encoded_xml = base64.b64encode(xml)
    except:
        raise GuiException('Невозможно перекодировать запрос в base64')
    param = dict(
        aSessionID = authenticate(),
        aRequest = dict(Type = request_type, Version = 1, Body = encoded_xml)
        )
    result_xml = remote_call('getDataXml', param)
    encoded_body_xml = get_xml_field_value(result_xml, 'Body')
    if encoded_body_xml is None:
        raise GuiException("Неизвестный тип ответа от веб-сервиса")

    return base64.b64decode(encoded_body_xml)

def login(name, pwd):
    global user_name, user_pass
    user_name, user_pass = name, pwd
    authenticate()
    return user_id
