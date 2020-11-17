#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from solution.solution import solutionExecutor

defaultProcessNum = 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lab', type=int, nargs=None, required=True,
                        help="lab number for tests to run")
    parser.add_argument('-p', '--part', type=int, nargs='?', default=None,
                        help="part number for tests to run")

    args = parser.parse_args()

    # read data

    """
    Using multiprocessing for possible multiple process concurrent running.
    Multiprocessing will serialize and deserialize the argument (deep copy). 
    Thus, each process will have it independent memory space (not affect other).
    """

    # select best

    # write vertex set


if __name__ == "main":
    main()