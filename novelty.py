# -*- coding: utf-8 -*-

import httplib
import base64

from constants  import *
from xml_utils  import replace_field_in_xml, get_xml_field_value, dict_to_xml
from errors     import GuiException, set_last_error

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

def set_session_in_xml(xml, session):
    new_xml = replace_field_in_xml(xml, 'aSessionID', session)
    new_xml = replace_field_in_xml(new_xml, 'sessionID', session)
    new_xml = replace_field_in_xml(new_xml, 'aSession', session)
    return new_xml

#
#  TODO !!!
#  Сейчас аутентификация происходит только на home.novelty.
#  Об этом не стоит забывать и, в случае чего, необходимо переделать.
#
def request_ex(xml, servers, port, use_ssl, url=SERVICES_URL, err_msg='Невозможно установить соединение с БД'):
    connected = False
    for server in servers:
        host_str = '%s:%s' % (server, port)
        if use_ssl:
            h = httplib.HTTPSConnection(host_str)
        else:
            h = httplib.HTTPConnection(host_str)
        headers = {
            'Host':host_str,
            'Content-Type':'text/xml; charset=utf-8',
            'Content-Length':len(xml),
            }
        try:
            h.request('POST', url, body=xml, headers=headers)
            connected = True
        except:
            pass
    
    if not connected:
        set_last_error(ERROR_CANT_CONNECT)
        raise GuiException(err_msg)
    
    r = h.getresponse()
    d = r.read()
    
    err = get_xml_field_value(d, 'faultstring')
    if err is None:
        err = get_xml_field_value(d, 'ErrorMessage')
    if err is not None:
        print err
        if 'Сессия не определена' in err:
            return request_ex(set_session_in_xml(xml, authenticate(force=True)), [server], port, use_ssl, url, err_msg)
        else:
            raise GuiException(err)
    
    return d

def request(xml):
    return request_ex(xml, HOME_NOVELTY_SERVERS, HOME_NOVELTY_PORT, True, BRIDGE_URL)

def remote_call(function, params):
    xml = xml_template % {'function':function, 'param_list':dict_to_xml(params)}
    return request(xml)

def remote_call_ex(function, params, server, port, use_ssl, url=SERVICES_URL):
    xml = xml_template % {'function':function, 'param_list':dict_to_xml(params)}
    return request_ex(xml, [server], port, use_ssl, url, 'Сервис управления серверами приложений недоступен')

def authenticate(force=False):
    global session_id, user_id
    if not session_id or force:
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

def generate_jasper_report_sync(report_id, param_xml):
    param = dict(
        aSession = authenticate(),
        aParamsXML = "<![CDATA[<report><name>%i</name><return>pdf</return>%s</report>]]>" % (report_id, param_xml)
        )
    result_xml = remote_call('generateJasperReportSync', param)
    encoded_result = get_xml_field_value(result_xml, 'return')
    if encoded_result is None:
        raise GuiException("Неизвестный тип ответа от веб-сервиса")
    
    return base64.b64decode(encoded_result)
