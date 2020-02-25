#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  zweig_score_nasdaq.py
#  
#  Copyright 2019 Rohit Valsakumar <rohit@rohit-Vostro-270s>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import requests, bs4, collections, argparse, json

zweig_url = "https://www.nasdaq.com/symbol/{sym}/guru-analysis/zweig"

def get_zweig_score(symbol):
  with requests.Session() as s:
    page = s.get(zweig_url.format(sym=symbol))
    soup = bs4.BeautifulSoup(page.content, "lxml")
    zweig_score = soup.find_all(text="Martin Zweig")[2].parent.next_sibling.next_sibling.next_sibling
    
    return zweig_score.get_text()

def main():
  parser = argparse.ArgumentParser(description="Sort the files in a folder into subfloders based on create date")
  parser.add_argument("-s", "--symbol", help="The symbol.", required=True)
  args = parser.parse_args()
  try:
    zs = get_zweig_score(args.symbol)
    print "{} {}".format(zs, args.symbol)
  except:
    print "- {}".format(args.symbol)
    return 1
  return 0

if __name__ == '__main__':
  main()

