#!/usr/bin/python

import sys
import json
import os.path
import g_vars

class globVarsS():

    # Basic calling values (arguments)
    enviroment      = False
    reponame        = False

    # Values from the config file
    path_svn_base   = False
    path_travellers = False

    # File definitions

    # Path definitions

    # Shortened for PathToTravellerReponame
    pttr = False

def mapAuthors():
    print("Map aus GEARBOX")
    # Remove former files
    #[ -e "${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}" ] && rm -f "${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}"
    # As we do not have any standard mapping we just copy the file
    #cp ${PATH_TRAVELLER_REPO_AUTHORS} ${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}



print('In the Module:', __name__)

def readTheConfig(enviroment):
    """docstring"""
    from pathlib import Path
    print('\nRead the Config-File for enviroment: ', enviroment)

    # declarring the vars
    global PATH_CONFIG_FILE
    global CONFIG_FILE

    PATH_CONFIG_FILE = "specs"
    CONFIG_FILE = PATH_CONFIG_FILE + "/config.json"

    if os.path.exists(CONFIG_FILE):
        print(f'The file {CONFIG_FILE} exists')
    else:
        sys.exit(f'The file "{CONFIG_FILE}" does not exist')

    f = open(CONFIG_FILE)
    data = json.load(f)

    g_vars.path_svn_base    = data[enviroment][0]['path_svn_base']
    g_vars.path_travellers  = data[enviroment][0]['path_travellers']

    globVarsS.path_svn_base = data[enviroment][0]['path_svn_base']
    globVarsS.path_travellers = data[enviroment][0]['path_travellers']
