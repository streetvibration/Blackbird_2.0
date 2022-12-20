#!/usr/bin/python

import sys
import inspect
import os
import logging
import subprocess
import json
import os.path
import time
from logging import getLoggerClass, addLevelName, setLoggerClass, NOTSET
from datetime import datetime
import mechanics    # needed for the overrideFunction


# TODO - Tried to add a new log-level but something is not working
# class SucessLogger(getLoggerClass()):
#     def __init__(self, name, level=NOTSET):
#         super().__init__(name, level)
#
#         addLevelName(5, "SUCCESS")
#
#     def success(self, msg, *args, **kwargs):
#         if self.isEnabledFor(5):
#             self._log(5, msg, args, **kwargs)
#
#
# setLoggerClass(SucessLogger)

def overrideFunction(function):

    logging.info("Required function: " + function)

    try:
        # Try to get the attributes from a function in 'mechanics.py'
        mam = getattr(mechanics, function)
        logging.warning("Default function '" + function + "' overridden by custom code in 'mechanics'")
        mam()

    except: # The function is not defined in mechanics.py
        logging.info("Default function '"+ function + "' is proceeded.")
        mapAuthors()


def calcRuntime(sTime, eTime):
    tdelta = eTime - sTime
    #diff_in_minutes = 0
    diff_in_seconds = round(tdelta.total_seconds(), 2)

    if diff_in_seconds >= 60:
        diff_in_minutes = round(diff_in_seconds / 60, 2)
        dTime = str(diff_in_minutes)
        dUnit = "Minutes"
    else:
        dTime = str(diff_in_seconds)
        dUnit = "Seconds"

    return dTime, dUnit


def getLevelNames():
    print("Levelnames: {}".format(", ".join(
        logging.getLevelName(x)
        for x in range(1, 101)
        if not logging.getLevelName(x).startswith('Level'))))


class globVarsS:
    # logging.info("Initiate the vars")

    # Basic calling values (arguments)
    enviroment = ""
    reponame = ""

    # Vars for the final log of all the scripts

    touchandgo_list     = ["TOUCHANDGO \t(Resetting former data)"]
    touchandgo_error    = []

    taxiing_list        = ["TAXIING \t(Gathering data from the SVN repo)"]
    takeoff_list        = ["TAKEOFF \t(Fast exporting the SVN repo)"]
    initialclimb_list   = ["INITIALCLIMB \t(Cloning the bare repo)"]
    cruisealtitude_list = ["CRUISEALTITUDE \t(Analyzing the Git repo)"]
    descent_list        = ["DESCENT \t(Filtering the base repo)"]
    approach_list       = ["APPROACH \t(Pushing the repo)"]
    touchdown_list      = ["TOUCHDOWN \t(Flatten out the binaries)"]

    run_results = {
        'touchandgo'        : touchandgo_list,
        'taxiing'           : taxiing_list,
        'initialclimb'      : initialclimb_list,
        'cruisealtitude'    : cruisealtitude_list,
        'descent'           : descent_list,
        'approach'          : approach_list,
        'touchdown'         : touchdown_list
    }

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


def checkIfSVN_RepoExists(path):
    assert (os.path.exists(path)), "SVN-Repository not found"
    logging.info("SVN-Repository at '" + globVarsS.psvn_REPO + "' exists.")
    # isExisting = os.path.exists(path)


def setGlobalVars():
    globVarsS.psvn_REPO = globVarsS.path_svn_base + "/" + globVarsS.reponame
    globVarsS.pttr = globVarsS.path_travellers + "/" + globVarsS.reponame
    globVarsS.pttr_BOARDINGPASS = globVarsS.pttr + "/" + "boardingpass"
    globVarsS.pttr_AUTHORS = globVarsS.pttr_BOARDINGPASS + "/" + globVarsS.FILE_AUTHORS


def mapAuthors():
    #print("Mapping aus GEARBOX")
    #logging.info("Map aus GEARBOX")
    logging.info("Mapping the authors")
    # Remove former files
    # [ -e "${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}" ] && rm -f "${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}"
    # As we do not have any standard mapping we just copy the file
    # cp ${PATH_TRAVELLER_REPO_AUTHORS} ${PATH_TRAVELLER_REPO_AUTHORS_MAPPED}


def getAuthors():
    svn_filepath = "file://" + globVarsS.psvn_REPO
    cmd = "svn log -q " + svn_filepath + " | grep '^r' | grep '|' | awk '{print $3}' | sort | uniq"
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)

    # TODO change the open path to "globVarsS.pttr_AUTHORS" after we have all folders & file defined
    with open("authors.txt", "w+") as f:
        for line in proc.stdout:
            elem = line.strip().decode()
            elem = elem + " " + "=" + " " + elem + " <" + elem + "@" + "mycompany.com>\n"
            f.write(elem)  # add the line to the file


def readTheConfig(enviroment):
    """docstring"""
    #from pathlib import Path
    logging.info("Trying to read the Config-File for '" + globVarsS.enviroment + "' enviroment")

    CONFIG_FILE = "specs/config.json"

    if os.path.exists(CONFIG_FILE):
        logging.info("The config file at path '" + CONFIG_FILE + "' exists")
    else:
        sys.exit(f'The config file "{CONFIG_FILE}" does not exist')

    f = open(CONFIG_FILE)
    data = json.load(f)

    # Set the vars

    globVarsS.path_svn_base = data[enviroment][0]['path_svn_base']
    globVarsS.path_travellers = data[enviroment][0]['path_travellers']

# Logging formatter supporting colorized output
class LogFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # bright/bold magenta
        logging.ERROR: "\033[1;31m",  # bright/bold red
        logging.WARNING: "\033[1;33m",  # bright/bold yellow
        logging.INFO: "\033[0;37m",  # white / light gray
        logging.DEBUG: "\033[1;30m",  # bright/bold black / dark gray
        # logging.SUCCESS:  "\033[1;32m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)


# Setup logging
def setup_logging(console_log_output, console_log_level, console_log_color, logfile_date, logfile_file,
                  logfile_log_level, logfile_log_color, log_line_template):
    # Create logger
    # For simplicity, we use the root logger, i.e. call 'logging.getLogger()'
    # without name argument. This way we can simply use module methods for
    # for logging throughout the script. An alternative would be exporting
    # the logger, i.e. 'global logger; logger = logging.getLogger("<name>")'
    logger = logging.getLogger()

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_log_output = console_log_output.lower()
    if (console_log_output == "stdout"):
        console_log_output = sys.stdout
    elif (console_log_output == "stderr"):
        console_log_output = sys.stderr
    else:
        print("Failed to set console output: invalid output: '%s'" % console_log_output)
        return False
    console_handler = logging.StreamHandler(console_log_output)

    # Set console log level
    try:
        console_handler.setLevel(console_log_level.upper())  # only accepts uppercase level names
    except:
        print("Failed to set console log level: invalid level: '%s'" % console_log_level)
        return False

    # Create and set formatter, add console handler to logger
    console_formatter = LogFormatter(fmt=log_line_template, color=console_log_color, datefmt='%Y-%m-%d %H:%M')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create log file handler
    try:
        logfile_handler = logging.FileHandler(logfile_file)
    except Exception as exception:
        print("Failed to set up log file: %s" % str(exception))
        return False

    # Set log file log level
    try:
        logfile_handler.setLevel(logfile_log_level.upper())  # only accepts uppercase level names
    except:
        print("Failed to set log file log level: invalid level: '%s'" % logfile_log_level)
        return False

    # Create and set formatter, add log file handler to logger
    # logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color)
    logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color, datefmt='%Y-%m-%d %H:%M')
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)

    # Success
    return True
