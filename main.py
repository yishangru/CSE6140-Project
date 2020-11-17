#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lab', type=int, nargs=None, required=True,
                        help="lab number for tests to run")
    parser.add_argument('-p', '--part', type=int, nargs='?', default=None,
                        help="part number for tests to run")

    args = parser.parse_args()


if __name__ == "main":
    main()