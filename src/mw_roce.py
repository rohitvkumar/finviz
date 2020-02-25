#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mw_roce.py
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

financials_url = "https://www.marketwatch.com/investing/stock/{sym}/financials"
balance_sheet_url = "https://www.marketwatch.com/investing/stock/{sym}/financials/balance-sheet"

tenpow = { 'T': 10**12, 'B': 10**9, 'M': 10**6, 'K': 10**3}

def get_text_tag(soup, tag):
  try:
    elem = soup.find_all(text=tag)
    text =  elem[0].parent.parent.find_all('td')[-2].get_text()
    return text
  except:
    return '-'

def text_to_float(text):
  if text[0] == '(' and text[-1] == ')':
    return float(text[1:-2]) * tenpow[text[-2]] * -1
  else:
    return float(text[0:-1]) * tenpow[text[-1]]

def get_ebit_netinc(s, symbol):
  page = s.get(financials_url.format(sym=symbol))
  soup = bs4.BeautifulSoup(page.content, "lxml")
  
  try:
    elem = soup.find_all(text=" EBITDA")
    text = elem[0].parent.parent.find_all('td')[-2].get_text()
    ebit = text
  except:
    ebit = '-'
  
  net_income = get_text_tag(soup, "Net Income After Extraordinaries")
  if net_income == '-':
    net_income = get_text_tag(soup, "Net Income Available to Common")
  
  return (ebit, net_income)
  
def get_assets_liabilities(s, symbol):
  page = s.get(balance_sheet_url.format(sym=symbol))
  soup = bs4.BeautifulSoup(page.content, "lxml")
  try:
    elem = soup.find_all(text=" Total Assets")
    text =  elem[0].parent.parent.find_all('td')[-2].get_text()
    assets = text
  except:
    assets = '-'
    
  curr_liabilities = get_text_tag(soup, " Total Current Liabilities")
  if curr_liabilities == '-':
    curr_liabilities = get_text_tag(soup, "Other Liabilities")
    
  return (assets, curr_liabilities)
  
def main():
  parser = argparse.ArgumentParser(description="Sort the files in a folder into subfloders based on create date")
  parser.add_argument("-s", "--symbol", help="The symbol.", nargs='+')
  args = parser.parse_args()
  with requests.Session() as s:
    for sym in args.symbol:
      if sym == "SYMBOL":
        print "EBIT NetInc TAssets TCurrLbl ROCE NICE"
      else:
        assets, liabilities = get_assets_liabilities(s, sym)
        ebit, net_inc = get_ebit_netinc(s, sym)
        try:
          working_cap = text_to_float(assets) - text_to_float(liabilities)
          NICE = round((text_to_float(net_inc) * 100 / working_cap), 2)
        except:
          NICE = -999
        try:
          ROCE = round((text_to_float(ebit) * 100 / working_cap), 2)
        except:
          ROCE = -999
        
        print "{} {} {} {} {} {}".format(ebit, net_inc, assets, liabilities, ROCE, NICE)
  return 0

if __name__ == '__main__':
  main()

