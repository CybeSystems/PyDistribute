#!/usr/bin/env python

###################################################################################################
# CybeSystems PyDistribute
#
# Distribute Python programs
#
# Distribute your python program with real python interpreter (full stdlibs)
# without freezer like cx_freeze or pyinstaller
#
# This script strip down the python interperter to 4-5MB and can create a launcher with nuitka
# additional options are e.g. zip stdlibs (less files -> better for USB Sticks) and
# includes a "Hooks" section for PyQt (manually pick the needed files -> much smaller distriubution)
#
# It includes also a option to crate a NSIS launcher
#
# I've made this script because cx_freeze and pyinstaller need (for my programs) a lot of workarounds
# and I need a real interpreter for subscripts (like updates)
#
# Please make sure to read the section description before using this script
#
###################################################################################################

###################################################################################################
# SECTION INDEX
#
#    NSIS Config
#    Build Config
#    PERFORMANCE SETTINGS
#
###################################################################################################

import os, sys, json

scriptpath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(scriptpath, 'lib'))

from pyDistribute import *

if __name__ == "__main__":
    print("Creating sample installer with default config")

    # This json file MUST have absolute path
    config = getConfig(scriptpath + "\\pyDistribute.json")

    # Override settings in script if needed
    # Better is to set options in pyDistribute.json
    config['release']['usePortableAppsStructure'] = False

    #Create distribution
    cyDistribute(config)
else:
    print("Please dont include this file")
    print("Use e.g. a Windows Batch:")
    print('    python.exe C:\PyDistribute\pyDistribute.py --config "C:\YOURPYTHONPROGRAM\pyDistribute.json"')
    sys.exit()