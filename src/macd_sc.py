import requests, bs4, collections, argparse, json, datetime
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_bullish_macd_top(s, url, limit):
  page = s.get(url, headers=headers)
  soup = BeautifulSoup(page.content, 'lxml')
  table = soup.find_all('table')[0]
  thead = soup.find_all('thead')[0]
  tbody = soup.find_all('tbody')[0]

  items = {}
  for row in tbody.find_all('tr'):
    tds = row.find_all('td')
    price = float(tds[6].text)
    volume = float(tds[7].text)
    dollar_vol = price * volume
    if dollar_vol > limit:
      items['{:<5s} | {:<30s} | {:<20s} | {:8.2f} | {:,}'.format(tds[1].text, tds[2].text[:30], tds[4].text[:20], float(tds[6].text), int(tds[7].text))] = dollar_vol
  for w in sorted(items, key=items.get, reverse=True):
    print(w)


def main():
  parser = argparse.ArgumentParser(description="Sort the files in a folder into subfloders based on create date")
  parser.add_argument("-l", "--limit", help="The minimum trade volume in $ millions.", type=int, default=100)
  args = parser.parse_args()
  limit = args.limit * 1000 * 1000
  print(datetime.datetime.now())
  with requests.Session() as s:
    print("NYSE Bullish 50/200")
    nyse_url = "https://stockcharts.com/def/servlet/SC.scan?s=TSAL[t.t_eq_s]![t.e_eq_y]![as0,20,tv_gt_40000]![as0,50,tc_gt_as0,200,tc]![as1,50,tc_le_as1,200,tc]&report=predefall"
    get_bullish_macd_top(s, nyse_url, limit)
    print("\nNASDAQ Bullish 50/200")
    nasdaq_url = "https://stockcharts.com/def/servlet/SC.scan?s=TSAL[t.t_eq_s]![T.E_EQ_N]![T.E_NE_O]![as0,20,tv_gt_40000]![as0,50,tc_gt_as0,200,tc]![as1,50,tc_le_as1,200,tc]&report=predefall"
    get_bullish_macd_top(s, nasdaq_url, limit)
  return 0

if __name__ == '__main__':
  main()
