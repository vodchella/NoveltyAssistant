# -*- coding: utf-8 -*-

#
# Defines
#
DONT_EXIT_IF_CANT_CONNECT = False

#
# Program
#
PROGRAM_REVISION_NUMBER = 48
PROGRAM_VERSION = '0.02.%s' % PROGRAM_REVISION_NUMBER
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
# Format masks
#
REMOTE_DATE_FORMAT = '%d.%m.%Y'

#
# Error codes
#
NO_ERROR            = 0
ERROR_SUCCESS       = NO_ERROR
ERROR_CANT_CONNECT  = 1
