# -*- coding: utf-8 -*-

import tempfile
import os
import re
import subprocess
from constants import *

def clear_tmp_dir():
    dir = tempfile.gettempdir()
    for f in os.listdir(dir):
        if re.search(REPORT_MASK, f):
            try:
                os.remove(os.path.join(dir, f))
            except:
                pass

def save_tmp_file(file_data, suffix=REPORT_EXT, prefix=REPORT_PREFIX):
    fd = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    f = os.fdopen(fd[0], 'w')
    f.write(file_data)
    f.close()
    return fd[1]

def open_file_with_default_app(filename):
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(['xdg-open', filename])
