#!/usr/bin/env python3
import logging
import os
import sys
import time
import subprocess
import _gearbox



def main():

    time.sleep(3)

    cwd = os.getcwd()

    print(__name__)

    #print("REPO: ", repo)
    print("RRR: ", _gearbox.globVarsS.reponame)

    # Print the current working directory
    print("Current working directory: {0}".format(cwd))

    # Print the type of the returned object
    print("os.getcwd() returns an object of type: {0}".format(type(cwd)))

    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))

    #print("BB")
    #subprocess.run(["ls"])
    #print("AA")
    # Change the current working directory
    #os.chdir('./flightplan')

    logging.error("This is an error")
    _gearbox.globVarsS.touchandgo_error.append("\tERROR - This is an error")
    #_gearbox.globVarsS.touchandgo_error.append("\tERROR - This is another error")

    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))

    path = 'flightplan'
    try:
        os.chdir(path)
        print("Current working directory: {0}".format(os.getcwd()))
    except FileNotFoundError:
        print("ERROR - Directory: {0} does not exist".format(path))
    except NotADirectoryError:
        print("ERROR -{0} is not a directory".format(path))
    except PermissionError:
        print("ERROR - You do not have permissions to change to {0}".format(path))

    os.chdir(cwd)

if __name__ == "__main__":
    main()
