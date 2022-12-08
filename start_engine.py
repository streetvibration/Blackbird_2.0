#!/usr/bin/python

import argparse
import g_vars
# import _gearbox as gb
import _gearbox
import mechanics
import svn
import pprint

#TODO How can we reuse the function mapAuthors from 2 different scripts with 2 different codes

from _gearbox import mapAuthors
from mechanics import mapAuthors

mapAuthors()

if __name__ == '__main__':

    # TODO - Check if we use this g_vars OR globVarsS
    g_vars.initialize()
    print("SVN - After first run of init: ", g_vars.path_svn_base )
    print("Travellers - After first run of init: ", g_vars.path_travellers )

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

    if not args.env:
        _gearbox.globVarsS.enviroment = "test"
        print("No enviromet given- using 'test' as default")
    else:
        _gearbox.globVarsS.enviroment = args.env
        print("Running in :", _gearbox.globVarsS.enviroment, "enviroment")

    _gearbox.readTheConfig(_gearbox.globVarsS.enviroment)

    #print("\n The Script-Name & Arguments: \n")
    #print(__name__)
    #print(args)

    #print("SVN-Base: ", _gearbox.globVarsS.path_svn_base)
    #print("Tavellers: ", _gearbox.globVarsS.path_travellers)

    if args.repo == "":
        print(f'No given repo name for argument -r')
    else:
        print(f'The repo ', args.repo, 'exists')
        _gearbox.globVarsS.reponame = args.repo

    _gearbox.setGlobalVars()

    _gearbox.getAuthors()