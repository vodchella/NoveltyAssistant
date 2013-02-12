# -*- coding: utf-8 -*-

import urllib
import lxml.html
from remote_functions   import get_dinner_paths
from constants          import *

def get_dinner_html():
    try:
        ufile = urllib.urlopen(DINNER_HTML)
        if ufile.info().gettype() == 'text/html':
            return ufile.read()
    except:
        pass

def arr_from_string(sz):
    magic_str = '*<*>*'
    return sz.replace('1. ', magic_str).replace('2. ', magic_str).replace('3. ', magic_str).replace('4. ', magic_str).split(magic_str)[1:]

def numerate_arr(arr):
    return ['%i. %s' % (i+1, a.strip()) for i, a in enumerate(arr)]

def go_deep(root, path_arr, result):
    for elem in filter(lambda l: l.tag == path_arr[0], iter(root)):
        if len(path_arr) > 1:
            go_deep(elem, path_arr[1:], result)
        else:
            if elem.text is not None:
                result += arr_from_string(elem.text_content().encode('utf-8'))

def get_today_menu():
    arr = []
    html = get_dinner_html()
    if html is not None:
        try:
            doc = lxml.html.document_fromstring(html)
            root_div = doc.xpath('/html/body/div[@id="wrapper"]/div[@id="body"]/div[@id="right"]/div[@id="booking"]')[0]
            
            #div/p
            #div/p/em
            #div/div/strong/em/p/em
            #div/div/strong/em
            #div/div/p/em
            #div/div/em/p/em
            
            paths = get_dinner_paths()
            for path in paths:
                if not arr:
                    go_deep(root_div, path.split('/'), arr)
                else:
                    break
        except:
            pass
    return numerate_arr(arr)

def get_today_menu_text():
    return '\n'.join(get_today_menu()).decode('utf-8')
