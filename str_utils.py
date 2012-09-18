# -*- coding: utf-8 -*-

# Производит регистронезависимую замену подстроки в строке
def ireplace(txt, old, new):
    idx = 0
    text = txt
    len_old = len(old)
    len_new = len(new)
    old_u = old.upper()
    while idx < len(text):
        index_u = text[idx:].upper().find(old_u)
        if index_u == -1:
            return text
        index_u += idx
        text = text[:index_u] + new + text[index_u + len_old:]
        idx = index_u + len_new
    return text

# Производит регистронезависимую замену подстроки в строке с учётом маски.
# Маска может содержаться только в переменной new (та подстрока, на которую заменяем).
# Значения, на которые заменяется маска:
#   ##OLD## - вставляется заменяемая подстрока.
def ireplace_ex(txt, old, new):
    idx = 0
    text = txt
    len_old = len(old)
    old_u = old.upper()
    while idx < len(text):
        index_u = text[idx:].upper().find(old_u)
        if index_u == -1:
            return text
        index_u += idx
        new_str = new.replace(u'##OLD##', text[index_u:index_u + len_old])
        text = text[:index_u] + new_str + text[index_u + len_old:]
        idx = index_u + len(new_str)
    return text
