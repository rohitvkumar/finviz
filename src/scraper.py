'''
Created on Feb 22, 2016

@author: rohit
'''

import requests, bs4, collections, argparse, json

global_host = "http://finviz.com/"
global_sam50under200 = "screener.ashx?v=111&f=an_recom_buybetter,cap_midover,sh_avgvol_o500,sh_price_o15,ta_perf_4wup,ta_rsi_ob60,ta_sma200_pa,ta_sma50_sb200&ft=4&o=sector"
global_strength_from_below = "screener.ashx?v=111&f=an_recom_buybetter,cap_midover,sh_avgvol_o500,sh_price_o15,ta_perf_4wup,ta_sma200_pb,ta_sma50_pca&ft=4&o=sector"
global_sam50cross200 = "screener.ashx?v=111&f=an_recom_buybetter,cap_midover,sh_avgvol_o500,sh_price_o15,ta_perf_4wup,ta_sma200_pa,ta_sma50_cross200a&ft=4&o=sector"
global_garp2 = "screener.ashx?v=110&f=an_recom_buybetter,cap_midover,fa_debteq_u1,fa_eps5years_o15,fa_epsqoq_o15,fa_epsyoy_o15,fa_epsyoy1_o5,fa_estltgrowth_o5,fa_sales5years_o5,fa_salesqoq_o5,sh_avgvol_o500,sh_price_o10&ft=4&o=-industry"

def scrape_screen(s, init_link):
    scraped_dict = {}
            
    pages = collections.deque()
    pages.append(global_host + init_link)
    
    more = False
    sym_idx = 0
    sector_idx = 0
    while pages:
        page = s.get(pages.popleft())
        soup_output = bs4.BeautifulSoup(page.content, "lxml")
        
        if not more:
            more = True
            tablink = soup_output.select('a[class="screener-pages"]')
            for tab in tablink:
                pages.append(global_host + tab.get('href'))
        
        syms = soup_output.select('a[class="screener-link-primary"]')
        for sym in syms:
            scraped_dict[sym_idx] = dict(symbol=sym.getText())
            sym_idx += 1
            
        elems = soup_output.select('a[class="screener-link"]')
        count = 0
        for elem in elems:
            mod = count % 10
            if mod == 1:
                scraped_dict[sector_idx]['name'] = elem.getText().replace(' ', '_')
            elif mod == 2:
                scraped_dict[sector_idx]['sector'] = elem.getText().replace(' ', '_')
            elif mod == 9:
                sector_idx += 1
            count += 1
    return scraped_dict
               
def finviz_session(in_json):
    with requests.Session() as s:
        url = "http://finviz.com/login.ashx"
        email = "rohitvkumar@gmail.com"
        password = "rohitvk"
        
        s.get(url)
        login_data = dict(email=email, password=password, remember="true")
        s.post(url, data=login_data, headers={"Referer": "http://finviz.com"})
        
        scraped_dict = scrape_screen(s, global_garp2)
        print json.dumps(dict(filter="Garp 2", count=len(scraped_dict)))
        for item in scraped_dict.itervalues():
            if in_json:
                print json.dumps(item)
            else:
                print "{symbol: <6s}".format(**item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-J", "--json", action="store_true")
    
    args = parser.parse_args()
    
    finviz_session(args.json)
