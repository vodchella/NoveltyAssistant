# -*- coding: utf-8 -*-

import urllib
import lxml.html
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
            
            if not arr:
                for divs in filter(lambda l: l.tag == 'div', iter(root_div)):
                    for p in filter(lambda l: (l.tag == 'p'), iter(divs)):
                        for em in filter(lambda l: (l.tag == 'em'), iter(p)):
                            arr = ['%i. %s' % (i, a.strip()) for i, a in enumerate(em.text_content().encode('utf-8').replace('2. ', '1. ').replace('3. ', '1. ').replace('4. ', '1. ').split('1. '))][1:]
                            break
            
            if not arr:
                for divs in filter(lambda l: l.tag == 'div', iter(root_div)):
                    for d in filter(lambda l: (l.tag == 'div'), iter(divs)):
                        for strong in filter(lambda l: (l.tag == 'strong'), iter(d)):
                            for em in filter(lambda l: (l.tag == 'em'), iter(strong)):
                                arr.append(em.text.encode('utf-8').strip())
            
            if not arr:
                for divs in filter(lambda l: l.tag == 'div', iter(root_div)):
                    for d in filter(lambda l: (l.tag == 'div'), iter(divs)):
                        for strong in filter(lambda l: (l.tag == 'strong'), iter(d)):
                            for em in filter(lambda l: (l.tag == 'em'), iter(strong)):
                                for p in filter(lambda l: (l.tag == 'p'), iter(em)):
                                    for em1 in filter(lambda l: (l.tag == 'em'), iter(p)):
                                        arr.append(em1.text.encode('utf-8').strip())
            
        except:
            pass
    return arr

def get_today_menu_text():
    return '\n'.join(get_today_menu()).decode('utf-8')
