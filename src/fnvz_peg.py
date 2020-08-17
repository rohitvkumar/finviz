#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ROA_ROE_finviz.py
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

fin_url = "https://finviz.com/quote.ashx?t={sym}"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_roa_roe(s, symbol):
  page = s.get(fin_url.format(sym=symbol), headers=headers)
  soup = bs4.BeautifulSoup(page.content, "lxml")
  
  try:
    elem = soup.find_all(text="ROA")
    roa = elem[0].parent.next_sibling.find('b').get_text().strip('%')
  except Exception as e:
    roa = "-"
  
  try:
    elem = soup.find_all(text="ROE")
    roe = elem[0].parent.next_sibling.find('b').get_text().strip('%')
  except:
    roe = "-"
  
  try:
    elem = soup.find_all(text="PEG")
    peg = elem[0].parent.next_sibling.find('b').get_text()
  except:
    peg = 0
    
  try:
    elem = soup.find_all(text="P/E")
    pe = elem[0].parent.next_sibling.find('b').get_text()
  except:
    pe = 0
  
  try:
    elem = soup.find_all(text="EPS past 5Y")
    eps1 = elem[0].parent.next_sibling.find('b').get_text().strip('%')
  except:
    eps1 = 0
  
  #elem = soup.find_all(text="EPS next 5Y")
  #eps2 = elem[0].parent.next_sibling.find('b').get_text().strip('%')
  try:
    elem = soup.find_all(text="Dividend %")
    div = elem[0].parent.next_sibling.find('b').get_text().strip('%')
    if div == '-':
      div = 0
  except:
    div = 0
    
  try:
    elem = soup.find_all(text="Debt/Eq")
    deq = elem[0].parent.next_sibling.find('b').get_text().strip('%')
  except:
    deq = 0


  try:
    elem = soup.find_all("td", class_="fullview-links", align="center")[0].find_all("a")
    sect = elem[0].get_text()
    subs = elem[1].get_text()
    cnty = elem[2].get_text()
  except:
    sect = '-'
    subs = '-'
    cnty = '-'
  return (roa, roe, div, peg, pe, eps1, deq, sect, subs, cnty)

def get_fnvz_peg(s, sym):
  if sym == "SYMBOL":
    return("PEG;PEGD;DY;D/EQ;EPS5Y;PEF;PE;SECT;SUBS;CNTY;SYM")
  else:
    roa, roe, div, pef, pe, eps, deq, sect, subs, cnty = get_roa_roe(s, sym)
    
    try:
      peg = round((float(pe) / float(eps)), 2)
    except:
      peg = -999
      
    try:
      pegd = round((float(pe) /(float(eps) + float(div))), 2)
    except:
      pegd = -999
      
    return("{};{};{};{};{};{};{};{};{};{};{}".format(peg, pegd, div, deq, eps, pef, pe, sect, subs, cnty, sym))

def main():
  parser = argparse.ArgumentParser(description="Sort the files in a folder into subfloders based on create date")
  parser.add_argument("-s", "--symbol", help="The symbol.", nargs='+')
  args = parser.parse_args()
  with requests.Session() as s:
    for sym in args.symbol:
      print(get_fnvz_peg(s, sym))
  return 0

if __name__ == '__main__':
  main()
