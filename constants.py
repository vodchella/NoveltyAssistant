# -*- coding: utf-8 -*-

#
# Defines
#
DONT_EXIT_IF_CANT_CONNECT = False

#
# Program
#
PROGRAM_REVISION_NUMBER = 70
PROGRAM_VERSION = '0.03.%s' % PROGRAM_REVISION_NUMBER
PROGRAM_NAME = 'Novelty Assistant'
PROGRAM_NAME_FULL = '%s v%s' % (PROGRAM_NAME, PROGRAM_VERSION)

#
# Novelty connection settings
#
HOME_NOVELTY_SERVERS    = ['home.novelty.kz', 'home2.novelty.kz']
HOME_NOVELTY_PORT       = 28110
BRIDGE_URL              = '/WebBridge/WebBridge'
SERVICES_URL            = '/WebApps/ServiceController'

#
# Dinners
#
DINNER_HTML = "http://dinner.kz/"
DINNER_LOADING_MESSAGE = u"Идёт обновление, подождите..."
DINNER_LOADING_FAULT_MESSAGE = u"Ошибка загрузки данных. Просмотрите меню на сайте <a href='%s'>dinner.kz</a>" % DINNER_HTML
DINNER_REPORT_ID = 237

#
# Reports
#
REPORT_EXT = '.pdf'
REPORT_PREFIX = 'novasstrep'
REPORT_MASK = r'^(novasstrep)\w+(\.pdf)$'

#
# Format masks
#
REMOTE_DATE_FORMAT = '%d.%m.%Y'
REMOTE_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
CACHE_DATETIME_FORMAT  = '%Y-%m-%d %H:%M:%S'

#
# Error codes
#
NO_ERROR            = 0
ERROR_SUCCESS       = NO_ERROR
ERROR_CANT_CONNECT  = 1
