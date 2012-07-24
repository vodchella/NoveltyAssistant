# -*- coding: utf-8 -*-

import os
import sqlite3
from xml.dom.minidom import parseString
from xml_utils import *
from remote_functions import *

datadir = os.path.expanduser("~") + '/.novelty_assistant'
dbfile = datadir + '/cache.db'

CACHE_USER_NAME = 'user_name'
CACHE_USER_PASS = 'user_pass'

def sqliteConnection():
    return sqlite3.connect(dbfile)

def sqliteCursor(connection=None):
    if connection is None:
        con = sqlite3.connect(dbfile)
        connection = con
    return connection.cursor()

def initCache():
    if not os.path.isdir(datadir):
        os.makedirs(datadir)
    if not os.path.isfile(dbfile):
        con = sqliteConnection()
        cur = sqliteCursor(con)
        cur.execute("""CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                             novelty_id INTEGER NOT NULL,
                                                             customer_name TEXT NOT NULL,
                                                             priority INTEGER NOT NULL DEFAULT (0))""")
        cur.execute("""CREATE TABLE IF NOT EXISTS task_types (task_type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                              novelty_id INTEGER NOT NULL,
                                                              task_type_name TEXT NOT NULL,
                                                              priority INTEGER NOT NULL DEFAULT (0))""")
        cur.execute("""CREATE TABLE IF NOT EXISTS settings (setting_id INTEGER PRIMARY KEY NOT NULL,
                                                            setting_name TEXT NOT NULL,
                                                            setting_value TEXT)""")

def fillCache():
    con = sqliteConnection()
    cur = sqliteCursor(con)
    cur.execute("select count(*) from sqlite_master where tbl_name = 'customers'")
    if cur.fetchall()[0][0] == 1:
        cur.execute("select count(*) from customers")
        if cur.fetchall()[0][0] == 0:
            xml_str = getCustomersXML()
            dom = parseString(xml_str)
            customers = dom.getElementsByTagName('CUSTOMER')
            for customer in customers:
                customer_id   = get_node_element_value(customer, 'CUSTOMER_ID')
                customer_name = get_node_element_value(customer, 'CUSTOMER_NAME')
                cur.execute('insert into customers (novelty_id, customer_name) values (?, ?)', (customer_id, customer_name))
            
            xml_str = getTaskTypesXML()
            dom = parseString(xml_str)
            task_types = dom.getElementsByTagName('TASK_TYPE')
            for task_type in task_types:
                task_type_id   = get_node_element_value(task_type, 'TASK_TYPE_ID')
                task_type_name = get_node_element_value(task_type, 'TASK_TYPE_NAME')
                cur.execute('insert into task_types (novelty_id, task_type_name) values (?, ?)', (task_type_id, task_type_name))
            
            con.commit()

def getCustomers():
    cur = sqliteCursor()
    cur.execute("select novelty_id, customer_name from customers order by priority, customer_name")
    return cur.fetchall()

def getCustomerNameById(customer_id):
    cur = sqliteCursor()
    cur.execute("select max(customer_name) from customers where novelty_id = %i" % customer_id)
    return cur.fetchall()[0][0]

def getTaskTypes():
    cur = sqliteCursor()
    cur.execute("select novelty_id, task_type_name from task_types order by priority, task_type_name")
    return cur.fetchall()

def saveSetting(setting, value):
    set = str(setting)
    val = str(value)
    
    con = sqliteConnection()
    cur = sqliteCursor(con)
    cur.execute("select count(*) from settings where setting_name = ?", [set])
    cnt = cur.fetchall()[0][0]
    if cnt != 0:
        cur.execute("update settings set setting_value = ? where setting_name = ?", (val, set))
    else:
        cur.execute("insert into settings (setting_name, setting_value) values (?, ?)", (set, val))
    con.commit()

def getSetting(setting):
    cur = sqliteCursor()
    cur.execute("select max(setting_value) from settings where setting_name = ?", [str(setting)])
    return cur.fetchall()[0][0]

def getSavedLoginData():
    user_name = getSetting(CACHE_USER_NAME)
    user_pass = getSetting(CACHE_USER_PASS)
    if user_name is not None:
        return (user_name, user_pass)
    
def saveLoginData(user_name, user_pass):
    saveSetting(CACHE_USER_NAME, user_name)
    saveSetting(CACHE_USER_PASS, user_pass)
