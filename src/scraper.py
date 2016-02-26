'''
Created on Feb 22, 2016

@author: rohit
'''

import requests, bs4, collections

def finviz_sam50under200():
    with requests.Session() as s:
        url = "http://finviz.com/login.ashx"
        email = "rohitvkumar@gmail.com"
        password = "rohitvk"
        
        s.get(url)
        login_data = dict(email=email, password=password, remember="true")
        s.post(url, data=login_data, headers={"Referer": "http://finviz.com"})
        
        symbols = []
        industries = []
            
        pages = collections.deque()
        pages.append("http://finviz.com/screener.ashx?v=111&f=an_recom_buybetter,cap_midover,sh_avgvol_o500,"
                     "sh_price_o15,ta_perf_4wup,ta_rsi_ob60,ta_sma200_pa,ta_sma50_sb200&ft=4&o=sector")
        
        more = False
        while pages:
            page = s.get(pages.popleft())
            soup_output = bs4.BeautifulSoup(page.content, "lxml")
            
            if not more:
                more = True
                tablink = soup_output.select('a[class="screener-pages"]')
                for tab in tablink:
                    pages.append("http://finviz.com/" + tab.get('href'))
            
            syms = soup_output.select('a[class="screener-link-primary"]')
            for sym in syms:
                symbols.append(sym.getText())
                
            elems = soup_output.select('a[class="screener-link"]')
            count = 1
            for elem in elems:
                if count % 10 == 3:
                    industries.append(elem.getText())
                count += 1
                
        total = len(symbols)
        
        for i in range(total):
            print symbols[i], industries[i]

if __name__ == '__main__':
    finviz_sam50under200()