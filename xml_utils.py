# -*- coding: utf-8 -*-

def get_xml_field_value(xml, field):
    beg_str = '<%s>' % field
    pos = xml.find(beg_str)
    if pos != -1:
        result = xml[pos + len(beg_str) : xml.find('</%s>' % field)]
        if len(result) > 0:
            return result

def replace_field_in_xml(xml, field, value):
    result_xml = xml
    beg_str = '<%s>' % field
    beg = xml.find(beg_str)
    end = xml.find('</%s>' % field)
    if (beg != -1) and (end != -1):
        result_xml = xml[:beg + len(beg_str)] + value + xml[end:]
    return result_xml

def get_node_element_value(node, elem_name):
    elem = node.getElementsByTagName(elem_name)
    try:
        return elem[0].childNodes[0].nodeValue
    except:
        pass

def prepare_string(str):
    return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def dict_to_xml(dictionary):
    result = ''
    for rec in dictionary.items():
        if type(rec[1]) == dict:
            value = dict_to_xml(rec[1])
        else:
            value = rec[1]
        result += '<%(name)s>%(value)s</%(name)s>' % {'name':rec[0], 'value':value}
    return result
