#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ROCE_yahoo.py
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

import argparse, bs4, time
from requests_html import HTMLSession
from headers import headers

financials_url = "https://finance.yahoo.com/quote/{sym}/financials?p={sym}"
balance_sheet_url = "https://finance.yahoo.com/quote/{sym}/balance-sheet?p={sym}"
tenpow = { 'T': 10**12, 'B': 10**9, 'M': 10**6, 'K': 10**3}

def reduce(x):
  try:
    x = float(x.replace(",", "")) * 1000
  except:
    return x
  if x >= tenpow['T'] or x <= -tenpow['T']:
    return str(round(x / tenpow['T'], 2)) + 'T'
  if x >= tenpow['B'] or x <= -tenpow['B']:
    return str(round(x / tenpow['B'], 2)) + 'B'
  if x >= tenpow['M'] or x <= -tenpow['M']:
    return str(round(x / tenpow['M'], 2)) + 'M'
  
def get_text_tag(soup, tag):
  try:
    elem = soup.find_all(text=tag)
    text =  elem[0].parent.parent.parent.find_all('div')[2].get_text()
    return text
  except:
    return '-'
  
def get_text_tag_bs(soup, tag):
  try:
    elem = soup.find_all(text=tag)
    text =  elem[0].parent.parent.parent.find_all('div')[3].get_text()
    return text
  except:
    return '-'
  
def get_text_tag_bs_1(soup, tag):
  try:
    elem = soup.find('div', {"class": "rowTitle yf-1xjz32c", "title": "Total Liabilities Net Minority Interest"})
    print(elem)
    print('\n')
    text =  elem[0].parent.parent.parent.find_all('div')[3].get_text()
    return text
  except:
    return '-'

def text_to_float(text):
  return float(text.replace(',',''))

def get_ebit_netinc(s, symbol):
  page = s.get(financials_url.format(sym=symbol))
  page.html.render()
  soup = bs4.BeautifulSoup(page.html.html, "lxml")
  
  ebit = get_text_tag(soup, "Normalized EBITDA")
  net_income = get_text_tag(soup, "Normalized Income")
  
  return (ebit, net_income)
  
def get_assets_liabilities(s, symbol):
  page = s.get(balance_sheet_url.format(sym=symbol))
  page.html.render()
  soup = bs4.BeautifulSoup(page.html.html, "lxml")

  assets = get_text_tag_bs(soup, "Total Assets")
  curr_liabilities = get_text_tag_bs_1(soup, "Current Liabilities")
    
  return (assets, curr_liabilities)

def get_yh_roce(s, sym):
  if sym == "SYMBOL":
    return("EBIT;NetInc;TotAssets;TotCurrLiab;ROCE;NICE;")
  else:
    ebit, net_inc = get_ebit_netinc(s, sym)
    time.sleep(2)
    assets, liabilities = get_assets_liabilities(s, sym)
      
    try:
      working_cap = int(assets.replace(",", "")) - int(liabilities.replace(",", ""))
      NICE = round((float(net_inc.replace(",", "")) * 100 / working_cap), 2)
    except:
      NICE = -999
      
    try:
      ROCE = round((float(ebit.replace(",", "")) * 100 / working_cap), 2)
    except:
      ROCE = -999
    
    return("{};{};{};{};{};{};".format(reduce(ebit), reduce(net_inc), reduce(assets), reduce(liabilities), ROCE, NICE))
    
def main():
  parser = argparse.ArgumentParser(description="Sort the files in a folder into subfloders based on create date")
  parser.add_argument("-s", "--symbol", help="The symbol.", nargs='+')
  args = parser.parse_args()

  custom_headers = headers
  custom_headers['Host'] = 'finance.yahoo.com'

  with HTMLSession() as s:
    s.headers.update(custom_headers)
    for sym in args.symbol:
      print(get_yh_roce(s,sym))
  return 0

if __name__ == '__main__':
  main()

