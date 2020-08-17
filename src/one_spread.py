#!/usr/bin/env python

import argparse, requests
from mw_roce import get_mw_roce
from fnvz_peg import get_fnvz_peg


def main():
  parser = argparse.ArgumentParser(description="Sort the files in a folder into subfloders based on create date")
  parser.add_argument("-s", "--symbol", help="The symbol.", nargs='+')
  args = parser.parse_args()
  with requests.Session() as s:
    for sym in args.symbol:
      print("{};{}".format(get_mw_roce(s, sym),get_fnvz_peg(s,sym)))
  return 0

if __name__ == '__main__':
  main()