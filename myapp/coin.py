from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import re, json
import urllib
from bs4 import BeautifulSoup
import datetime

class CoinController:

    # def verifyString(res):
    #     res = res.replace("(", "")
    #     res = res.replace(")", "")
    #     res = res.replace("'", "")
    #     res = res.replace(";", "")  
    #     return res

    def getEachCoin(account, soup, pageNum, now):
        ### initialVelification ###
        soup = soup.find('table', class_='tw-basic-table tw-gift-table')
        # soup = soup.find('ul', class_='tw-item-icon-list')
        UserList = soup.find_all('tr')
        
        ### get User giving Coin. ###
        res = []; count = 0
        s = 'Coin'.encode(encoding='utf-8')
        
        flgCoin = True
        try:
            ## check the items in this Page
            for i, soup in enumerate(soup.find_all('tr')):
                tableitem = soup.find('td', class_='tw-gift-table-item')
                item = tableitem.find('a').attrs['href']
                item = item.replace("javascript:showItemDialog", "")
                
                item = item.replace("(", "")
                item = item.replace(")", "")
                item = item.replace("'", "")
                item = item.replace(";", "")
                
                res_user = {}
                status = str(tableitem.find('div').text)
                ## check the each item
                if re.search(r'coin', item):
                    # find Coin
                    flgCoin = True
                    
                    if re.search(r'baku', item):
                        ## check expired-CoinBaku
                        if re.search(r'Expired', status):
                            res_user["coin"] = 0
                            res_user["status"] = "Expired-CoinBaku"
                            res.append(res_user)
                            flgCoin = False
                            return res, int(99999999), flgCoin
                        else:
                            res_user["coin"] = 5
                            count += 5
                    else:
                        ## check expired-Coin
                        if re.search(r'Expired', status):
                            continue
                        else:
                            res_user["coin"] = 1
                            count += 1
                        
                    ## add user info 
                    ## user-name
                    userinfo = soup.find('td', class_='tw-gift-table-user')
                    name = userinfo.find('div', class_="tw-user-name-info").find("a")
                    res_user["name"] = str(name.text)
                    ## coin get time
                    time = userinfo.find('time', class_="tw-gift-table-date")
                    res_user["time"] = str(time.text)
                    ## coin get time substrat
                    td = datetime.datetime.strptime(str(time.text), '%Y/%m/%d %H:%M:%S')
                    if res_user["coin"] == 5:
                        un = td + datetime.timedelta(days=5)
                    else:
                        un = td + datetime.timedelta(days=3)
                    res_user["sbst"] = str(un - now)
                    ## coin status
                    status = status.replace("Expire Date                                        ", "")
                    res_user["status"] = status
                    
                    # shaping for return
                    res.append(res_user)
                                
        except Exception as e:
            print(e)
        
        return res, count, flgCoin

    def getAllCoin(soup):
        # Velification
        soup = soup.find('div', class_='tw-player-page__component tw-player-page__item')
        soup = soup.find('ul', class_='tw-item-icon-list')
        
        # get Coin
        res = {}
        s = 'Continue Coin'.encode(encoding='utf-8')
        try:
            for i, item in enumerate(soup.find_all('img')):
                if re.search(s, str(item).encode(encoding='utf-8')):
                    coin_n = soup.find_all('span')[i].text
                    res["coin_n"] = coin_n
                    break;
                
        except Exception as e:
            res["error"] = "Cannot find the 'Continue Coin' in latest 10 items"
        
        return res

    def bs4(url):
        ## Access to Arg-URL
        # Define User-Agent
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
                'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                'Chrome/55.0.2883.95 Safari/537.36 '
        
        # bs4 access
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response, 'lxml')
        response.close()
        
        return soup
