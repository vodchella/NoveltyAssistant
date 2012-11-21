# -*- coding: utf-8 -*-

import          urllib
import          lxml.html
from constants  import *

def get_dinner_html():
    try:
        ufile = urllib.urlopen(DINNER_HTML)
        if ufile.info().gettype() == 'text/html':
            return ufile.read()
    except:
        pass

def get_today_menu():
    arr = []
    html = get_dinner_html()
    if html is not None:
        try:
            doc = lxml.html.document_fromstring(html)
            root_div = doc.xpath('/html/body/div[@id="wrapper"]/div[@id="body"]/div[@id="right"]/div[@id="booking"]')[0]
            for divs in filter(lambda l: l.tag == 'div', iter(root_div)):
                for p in filter(lambda l: (l.tag == 'p') and (l.text is not None), iter(divs)):
                    arr.append(p.text.encode('utf-8'))
        except:
            pass
    return arr
