#!/usr/bin/env python3

import subprocess

# sample cmd:
# cmd = "vsish -e ls /vmkModules/lsom/disks/  | cut -d '/' -f 1  | while read diskID  ; do echo $diskID; vsish -e cat /vmkModules/lsom/disks/$diskID/virstoStats | grep -iE 'Delete pending |trims currently queued' ;  echo '====================' ;done ;"
a = "AAA"
b = "BBB"
c = "CCC"

cmd = "echo " + a + "; echo " + b + "; echo c"


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    for line in proc_stdout.decode().split('\n'):
        print(line)


subprocess_cmd(cmd)
