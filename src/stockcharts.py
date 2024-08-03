'''
Created on Mar 05, 2016

@author: rohit
'''

import requests, bs4, optparse, json

global_host = "http://stockcharts.com/"

global_strong_vol_nyse = "def/servlet/SC.scan?s=TSAL[t.t_eq_s]![t.e_eq_y]![as0,20,tv_gt_40000]![tv0_gt_as1,20,tv*4]![tc0_gt_tc1]&report=predefall"
global_strong_vol_nsdq = "def/servlet/SC.scan?s=TSAL[t.t_eq_s]![T.E_EQ_N]![T.E_NE_O]![as0,20,tv_gt_40000]![tv0_gt_as1,20,tv*4]![tc0_gt_tc1]&report=predefall"
global_bullish_50_200_nyse = "def/servlet/SC.scan?s=TSAL[t.t_eq_s]![t.e_eq_y]![as0,20,tv_gt_40000]![as0,50,tc_gt_as0,200,tc]![as1,50,tc_le_as1,200,tc]&report=predefall"
global_bullish_50_200_nsdq = "def/servlet/SC.scan?s=TSAL[t.t_eq_s]![T.E_EQ_N]![T.E_NE_O]![as0,20,tv_gt_40000]![as0,50,tc_gt_as0,200,tc]![as1,50,tc_le_as1,200,tc]&report=predefall"
global_uptrend_adx_nyse = "def/servlet/SC.scan?s=TSAL[t.t_eq_s]![t.e_eq_y]![as0,20,tv_gt_40000]![bm0,14_gt_20]![bm1,14_le_20]![bm2,14_le_20]![bn0,14_gt_bo0,14]&report=predefall"
global_uptrend_adx_nsdq = "def/servlet/SC.scan?s=TSAL[t.t_eq_s]![T.E_EQ_N]![T.E_NE_O]![as0,20,tv_gt_40000]![bm0,14_gt_20]![bm1,14_le_20]![bm2,14_le_20]![bn0,14_gt_bo0,14]&report=predefall"


def scrape_screen(s, link_list):
    scraped = []
    for link in link_list:
        url = global_host + link
        page = s.get(url)
        soup = bs4.BeautifulSoup(page.content, 'lxml')
        for item in soup.find_all('b'):
            scraped.append(item.getText())
    return scraped

def strong_vol_gainers(s):
    return scrape_screen(s, [global_strong_vol_nyse,global_strong_vol_nsdq])

def bullish_50_200(s):
    return scrape_screen(s, [global_bullish_50_200_nyse,global_bullish_50_200_nsdq])

def uptrend_adx(s):
    return scrape_screen(s, [global_uptrend_adx_nyse,global_uptrend_adx_nsdq])

def stockcharts_session():
    with requests.Session() as s:
        s.headers.update({'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"})
        strong_vol = strong_vol_gainers(s)
        print "Strong Vol gainers: {0}".format(json.dumps(strong_vol))
        bullish = bullish_50_200(s)
        print "Bullish 50/200 crossover: {0}".format(json.dumps(bullish))
        uptrend = uptrend_adx(s)
        print "Uptrend: {0}".format(json.dumps(uptrend))
        
        strong_vol_uptrend = [x for x in bullish if x in uptrend ]
        
        print "Strong volume and uptrend: {0}".format(json.dumps(strong_vol_uptrend))
        
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-J", "--json", dest="json_output", default=False, action="store_true")
    
    opt, args = parser.parse_args()
    
    stockcharts_session()
