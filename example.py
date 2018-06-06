"""
NAME
   example.py - example data and server commands

SYNOPSIS
   example.py -test | -load | -demo

OPTIONS
    -test
        runs all unit tests

    -load
        reinitializes database and loads csv data

    -demo
        starts the webserver to display sitter page
"""

import sys
import unittest2 as unittest2
from example.ingest.dataloader import DataLoader
from webserver import WebServer


def main():
    """
    main processing for example commands

    args: --
    returns: None
    """
    if len(sys.argv) == 2:
        flag = sys.argv[1]
        if flag == "-test":
            all_tests = unittest2.TestLoader().discover('./tests', pattern='*.py')
            unittest2.TextTestRunner(verbosity=2).run(all_tests)
        elif flag == "-load":
            DataLoader()
        elif flag == "-demo":
            # remove the command line arguments
            # web.py will inadvertantly pick them up to use
            # as port argument
            sys.argv = []
            webserver = WebServer()
            webserver.start()
        else:
            print
            print "invalid argument!"
            print __doc__
    else:
        print __doc__

if __name__ == "__main__":
    main()
