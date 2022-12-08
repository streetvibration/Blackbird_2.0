#!/usr/bin/python

import sys
import os
import subprocess
import json
import os.path
import g_vars

print('We are in the Module:', __name__)


def initializeVars():
    global var1
    var1 = "Initiasl value"

    global var2
    var2 = False


class globVarsS():
    # Basic calling values (arguments)
    enviroment = ""
    reponame = ""

    # Values from the config file
    path_svn_base = ""
    path_travellers = ""

    # File definitions
    FILE_AUTHORS = "authors.txt"

    # Shortened for PathToTravellerReponame
    pttr = ""
    pttr_BOARDINGPASS = ""
    pttr_AUTHORS = ""
    psvn_REPO = ""


def setGlobalVars():
    globVarsS.psvn_REPO = globVarsS.path_svn_base + "/" + globVarsS.reponame
    globVarsS.pttr = globVarsS.path_travellers + "/" + globVarsS.reponame
    globVarsS.pttr_BOARDINGPASS = globVarsS.pttr + "/" + "boardingpass"
    globVarsS.pttr_AUTHORS = globVarsS.pttr_BOARDINGPASS + "/" + globVarsS.FILE_AUTHORS


def mapAuthors():
    print("Map aus GEARBOX")
    # Remove former files
    # [ -e "${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}" ] && rm -f "${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}"
    # As we do not have any standard mapping we just copy the file
    # cp ${PATH_TRAVELLER_REPO_AUTHORS} ${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}


def getAuthors():
    svn_filepath = "file://" + globVarsS.psvn_REPO
    cmd = "svn log -q " + svn_filepath + " | grep '^r' | grep '|' | awk '{print $3}' | sort | uniq"
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)

    # TODO change the open path to "globVarsS.pttr_AUTHORS" after we have all folders & file defined
    f = open('authors.txt', 'a')  # open the file
    f.seek(0)  # set the position back to the beginning
    f.truncate()  # delete the content

    for line in proc.stdout:
        # print(line.strip().decode())
        my_elem = line.strip().decode()
        my_elem = my_elem + " " + "=" + " " + my_elem + " <" + my_elem + "@" + "mycompany.com>\n"
        f.write(my_elem)  # add the line to the file
        # print(my_elem)

    f.close()  # close the file


def readTheConfig(enviroment):
    """docstring"""
    from pathlib import Path
    print('\nRead the Config-File for enviroment: ', enviroment)

    CONFIG_FILE = "specs/config.json"

    if os.path.exists(CONFIG_FILE):
        print(f'The file {CONFIG_FILE} exists')
    else:
        sys.exit(f'The file "{CONFIG_FILE}" does not exist')

    f = open(CONFIG_FILE)
    data = json.load(f)

    # TODO - Check if we use this g_vars OR globVarsS
    g_vars.path_svn_base = data[enviroment][0]['path_svn_base']
    g_vars.path_travellers = data[enviroment][0]['path_travellers']

    globVarsS.path_svn_base = data[enviroment][0]['path_svn_base']
    globVarsS.path_travellers = data[enviroment][0]['path_travellers']
