#!/usr/bin/env python3

import _gearbox as gb

def main():
    print("CRUISEALTITUDE")

    gv = gb.globVarsS
    print(" In Cruisealtitude: ", gv.FILE_AUTHORS)
    gv.FILE_AUTHORS = "CCCCCCC"


if __name__ == "__main__":
    main()



