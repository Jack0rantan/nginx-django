from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

import re, json
import urllib
import urllib.request
from bs4 import BeautifulSoup
import datetime

from .coin import CoinController as CC


def index(req):
    return render(req, "index.html")


def coin(req):
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    now = now.replace(microsecond=0)
    account = ''
    
    # アカウント名が未入力
    if req.GET.get("account") is None or req.GET.get("account") == '':
        caution = "アカウント名を入力してください"
        return render(req, "coin.html",{"caution": caution})
    
    else:
        account = req.GET.get("account")
        print(account)
        
        # account = "hyo_tam"
        url = "https://twitcasting.tv/" + str(account)
        
        # Scraping
        try:
            soupTop = CC.bs4(url)
            resAllCoin = CC.getAllCoin(soupTop)
        except Exception as e:
            print(e)
            caution = "アカウント名が正しくない可能性があります。検索に失敗しました。"
            return render(req, "coin.html", {"caution": caution})
            
        allCoin = resAllCoin["coin_n"]
        count = 0; page_i = 0; limitPage = 30; res = {}; res["coinuserinfo"] = {}
        
        ## loop in AllCoin
        while int(allCoin) > int(count):
            
            # get GiftPage
            giftUrl = "https://twitcasting.tv/" + str(account) + "/gifts/" + str(page_i)
            soupGift = CC.bs4(giftUrl)
        
            # search coin
            resEachCoin, resCount, flg = CC.getEachCoin(account, soupGift, page_i, now)
            print("page", page_i,"countCoin", resCount, "page", giftUrl)
            try:
                # find Expired-coin
                if flg == False:
                    print("find expired Coin")
                    break
                else:
                    if resEachCoin == []:
                        page_i += 1
                        continue
                    res["coinuserinfo"]["page" + str(page_i)] = resEachCoin
                    count += resCount
                    page_i += 1
        
                # limit page 
                if page_i > limitPage:
                    break
            except Exception as e:
                return JsonResponse("not find")
            
        res["allcoin"] = resAllCoin["coin_n"]
        
        return render(req, "coin.html", res)
