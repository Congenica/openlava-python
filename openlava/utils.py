#!/usr/bin/python

import os, os.path
import glob

def find_openlava():
    if 'LSF_ENVDIR' in os.environ:
        return os.path.abspath(os.path.join(os.environ['LSF_ENVDIR'], '..'))

    if os.path.exists('/opt/openlava'):
        return '/opt/openlava'

    #see if there are any openlava versions in opt
    folders = glob.glob('/opt/openlava-[0-9]*')
    if folders:
        if len(folders) > 1:
            raise Exception("Multiple openlava installations in /opt!")
        else:
            return folders[0]

    raise Exception("Can't find open installation under /opt (expecting /opt/openlava-3.2 or similar)")
