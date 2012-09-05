# -*- coding: utf-8 -*-

import httplib
import base64

from xml_utils import *
from errors import GuiException

HOST = 'home2.novelty.kz:28110'
URL = '/WebBridge/WebBridge'

session_id = ''
user_name = ''
user_pass = ''
user_id = 0

def request(xml, SOAPAction):
    global session_id

    h = httplib.HTTPSConnection(HOST)
    headers={
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

def authenticate():
    global session_id, user_id

    if len(session_id) == 0:
        xml = \
        """<?xml version = "1.0" encoding = "UTF8" ?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
           <S:Body>
             <ns2:authenticateUser xmlns:ns2="http://ws.novelty.kz/">
               <aName>%s</aName>
               <aPassword>%s</aPassword>
               <aAlias>home</aAlias>
             </ns2:authenticateUser>
           </S:Body>
        </S:Envelope>""" % (user_name, user_pass)
        result_xml = request(xml, "authenticateUser")

        session_id = get_xml_field_value(result_xml, 'sessionID')
        if session_id is not None:
            user_id = get_xml_field_value(result_xml, 'ID')
        else:
            raise GuiException("Формат данных не распознан")

    return session_id

def get_data_xml(request_type, xml):
    try:
        encoded_xml = base64.b64encode(xml)
    except:
        raise GuiException('Невозможно перекодировать запрос в base64')
    request_xml = \
    """<?xml version = "1.0" encoding = "UTF-8" ?>
    <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
        <S:Body>
          <ns2:getDataXml xmlns:ns2="http://ws.novelty.kz/">
            <aSessionID>%s</aSessionID>
            <aRequest>
              <Type>%s</Type>
              <Version>1</Version>
              <Body>%s</Body>
            </aRequest>
          </ns2:getDataXml>
        </S:Body>
    </S:Envelope>""" % (authenticate(), request_type, encoded_xml)

    result_xml = request(request_xml, "getDataXml")

    encoded_body_xml = get_xml_field_value(result_xml, 'Body')
    if encoded_body_xml is None:
        raise GuiException("Формат данных не распознан")

    return base64.b64decode(encoded_body_xml)

def login(name, pwd):
    global user_name, user_pass
    user_name, user_pass = name, pwd
    authenticate()
    return user_id
