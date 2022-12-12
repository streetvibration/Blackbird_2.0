#!/usr/bin/python

"""
This script controls the migration from a SVN-Repo to Git

    Args:
        -r | --repo (string): name of the SVN-repo to be migrated (reqired)
        -x | --reset        : Resets the former data of a migration
        -i | --info         : Gathers the info of the SVN-Repo
        -e | --export       : Exporst a SVN-Repo into a bare Git-repo
        -c | --clone        : Clones the bare repo into a git repo
        -f | --filter       : Filters unwanted file-extensions out of the base repo
        -p | --push         : Pushes the filtered git-repo to the remote repo
        -b | --binaries     : Extract the filtered files into a flat filesystem
        -a | --archive      : Extract one or more paths into a flat filesystem
        --analize           : Analyzes a newly cloned repo
        --keep-ruleset      : Prtect a handcraftet rules file from being overwritten
        --env               : The desired environment to run th migration in ("test" is default
        --gh-remote-name    : Provides a deviating remote name

"""

import logging
import argparse
import g_vars
# import _gearbox as gb
import _gearbox
import mechanics
import svn
import pprint
import sys
import os
import subprocess
from datetime import datetime

#TODO How can we reuse the function mapAuthors from 2 different scripts with 2 different codes

from _gearbox import mapAuthors

# See all the logging level-names
_gearbox.getLevelNames()

# Initiate the logging procesdure
script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

if (not _gearbox.setup_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                               logfile_file=script_name + ".log", logfile_log_level="debug", logfile_log_color=False,
                               logfile_date='%Y-%m-%d %H:%M',
                               #log_line_template="%(color_on)s[%(created)d]  [%(module)s] %(lineno)d [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
                               log_line_template="%(color_on)s %(asctime)s [%(filename)s:%(lineno)d] - %(levelname)s  %(message)s%(color_off)s")):
    print("Failed to setup logging, aborting.")

mapAuthors()


if __name__ == '__main__':

    _gearbox.initializeVars()

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo', required=True)
    parser.add_argument('-x', '--reset',        action='store_true')
    parser.add_argument('-i', '--info',         action='store_true')
    parser.add_argument('-e', '--export',       action='store_true')
    parser.add_argument('-c', '--clone',        action='store_true')
    parser.add_argument('-f', '--filter',       action='store_true')
    parser.add_argument('-p', '--push',         action='store_true')
    parser.add_argument('-b', '--binaries',     action='store_true')
    parser.add_argument('-a', '--archive',      action='store_true')
    parser.add_argument('--analyze',            action='store_true')
    parser.add_argument('--keep-ruleset',       action='store_true')
    parser.add_argument('--trigger-initial',    action='store_true')
    parser.add_argument('--env', choices=['test', 'prod'])
    parser.add_argument('--gh-remote-name',     action='store_true')

    args = parser.parse_args()

    # Check if we have a given SVN-Repository
    if args.repo == "":
        print(f'No given repo name for argument -r')
        sys.exit()

    # Sdet the given reponame for further checks/proceeding
    _gearbox.globVarsS.reponame = args.repo

    # See if we have a given Envirinment - default "test"
    if not args.env:
        _gearbox.globVarsS.enviroment = "test"
        logging.warning("No enviromet given- using 'test' as default")
    else:
        _gearbox.globVarsS.enviroment = args.env
        logging.info("Running in :", _gearbox.globVarsS.enviroment, "enviroment")

    # Read the config file - Exiting the script when the file does not exist
    _gearbox.readTheConfig(_gearbox.globVarsS.enviroment)

    # Checking/creating the travellers folder-structure
    # _gearbox.createFMigStructure()

    # Setting the vars after s successful read of the config file
    _gearbox.setGlobalVars()

    # Check if the given SVN-Reponame is valid (existing folder)
    try:
        _gearbox.checkIfSVN_RepoExists(_gearbox.globVarsS.psvn_REPO)
    except Exception as ex:
        logging.exception('Caught an error')
        sys.exit()

    # Check if we have a given SVN-Repository
    if args.reset:
        logging.info("Resetting former migration data..")
        # start time and end time
        sTime = datetime.now()
        subprocess.call('python3 ./flightplan/touchandgo.py', shell=True)
        eTime = datetime.now()
        a, b = _gearbox.calcRuntime(sTime, eTime)
        print("Return time aus Calc: " + a + " " + b)
    else:
        logging.info("Resetting skipped")

    _gearbox.getAuthors()