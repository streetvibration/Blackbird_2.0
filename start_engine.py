#!/usr/bin/env python3

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
import sys
import os
from datetime \
    import datetime

# Shorten the access to functions instead of _grabox.function() -> gb.function()
import _gearbox as gb

# shorten all the access to the vars imstaead of _gearbox.globVarsS -> gv
from _gearbox import \
    setGlobalVars as gv

# Import the blackbird modules which are doing the work ;) from the 'flightplan' folder
from flightplan \
    import cruisealtitude, touchandgo, taxiing


gv = gb.globVarsS

#gv.FILE_AUTHORS = "TTTTTT"
print("Initial Value: ", gv.FILE_AUTHORS)
# importing all the blackbird modules
print("TESTING THE IMPORT FROM THE SUBFOLFER")
cruisealtitude.main()
print("After changed in cruisealtitude: ", gv.FILE_AUTHORS)
taxiing.main()

print("After changed in taxiing: ", gv.FILE_AUTHORS)



# Benchmarking the overall run
scriptStartTime = datetime.now()

# See all the logging level-names
gb.getLevelNames()

# Initiate the logging procesdure
script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

if (not gb.setup_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                               logfile_file=script_name + ".log", logfile_log_level="debug", logfile_log_color=False,
                               logfile_date='%Y-%m-%d %H:%M',
                               log_line_template="%(color_on)s %(asctime)s [%(filename)s:%(lineno)d] - %(levelname)s  %(message)s%(color_off)s")):
    print("Failed to setup logging, aborting.")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo',         required=True)
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
    parser.add_argument('--env',                choices=['test', 'prod'])
    parser.add_argument('--gh-remote-name',     action='store_true')

    args = parser.parse_args()

    # Check if we have a given SVN-Repository
    if args.repo == "":
        print(f'No given repo name for argument -r')
        sys.exit()

    # Sdet the given reponame for further checks/proceeding
    gb.globVarsS.reponame = args.repo

    # See if we have a given Envirinment - default "test"
    if not args.env:
        gv.enviroment = "test"
        logging.warning("No enviromet given- using 'test' as default")
    else:
        gv.enviroment = args.env
        logging.info("Running in :", gv.enviroment, "enviroment")

    # Read the config file - Exiting the script when the file does not exist
    gb.readTheConfig(gb.globVarsS.enviroment)

    # Checking/creating the travellers folder-structure
    # _gearbox.createFMigStructure()

    # Setting the vars after s successful read of the config file
    gb.setGlobalVars()

    # Check if the given SVN-Reponame is valid (existing folder)
    try:
        gb.checkIfSVN_RepoExists(gv.psvn_REPO)
    except Exception as ex:
        logging.exception('Caught an error')
        sys.exit()

    # Check if we have a given SVN-Repository
    if args.reset:
        logging.info("Resetting former migration data..")

        # start time and end time
        sTime = datetime.now()
        touchandgo.main()
        eTime = datetime.now()
        a, b = gb.calcRuntime(sTime, eTime)

        if gv.touchandgo_error:
            for i in gv.touchandgo_error:
                gv.touchandgo_list.append(i)
        else:
            gv.touchandgo_list.append("\tNo Error(s)")

        gv.touchandgo_list.append("Runtime: " + a + " " + b + "\n")

        logging.info("Runtime: " + a + " " + b)
    else:
        logging.info("Resetting skipped")
        gv.touchandgo_list.append("skipped")

    # Benchmarking the overall run
    scriptEndTime = datetime.now()
    a, b = gb.calcRuntime(scriptStartTime, scriptEndTime)
    totalRuntime = "\nTotal migratrion runtime: " + a + " " + b + "\n"

    # Printing / writing the runtimes of all scripts
    # TODO change the open path to "globVarsS.pttr_MIGRATION_LOG" after we have all folders & file defined
    with open("migration.log", "w+") as f:
        for key, value in gv.run_results.items():
            for i in value:
                print(i)
                f.write(f"{i}\n")
        print(totalRuntime)
        f.write(f"{totalRuntime}\n")

    print("\nTEST OVERRIDE A FUNCTION - GEARBOX/MECHANICS")
    cf = "mapAuthors"
    gb.overrideFunction(cf)
