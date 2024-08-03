#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cp.py
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

import requests, bs4, collections, argparse, json, urllib

bc_url = "http://bigcharts.marketwatch.com/historical/default.asp?"

def get_quote(s, sym, date):
  params = urllib.urlencode(dict(closeDate=date, symb=sym, x=0, y=0))
  
  page = s.get(bc_url + params)
  soup = bs4.BeautifulSoup(page.content, "lxml")
  
  try:
    elem = soup.find_all(text="Closing Price:")
    qt = elem[0].parent.parent.find_all('td')[0].get_text().strip()
  except:
    qt = "-"
  
  return qt.strip().replace(",", "")

def main():
  parser = argparse.ArgumentParser(description="")
  parser.add_argument("-s", "--symbol", help="The symbol.", required=True)
  parser.add_argument("-d", "--date", help="The date in mm/dd/yy format.", nargs='+')
  
  args = parser.parse_args()
  
  with requests.Session() as s:
    for d in args.date:
      qt = get_quote(s, args.symbol, d.strip())
      print "{} {}".format(d.strip(), qt)
      
  return 0

if __name__ == '__main__':
	main()
