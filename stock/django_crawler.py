import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_listinfo(code_number):
    #종목코드에 따른 현재가, 등락폭(listview에 필요한)을 가져온다.
    #input : (str)종목번호 , output : list [종가/ 전일대비 , 거래량]
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임

    url = base_url.format(code_number)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.select('.corp_group1 > h1') # '.'은 BeautifulSoup에서 태그를 추출할때 사용하는 것임.
    name_2 = str(name) # name이 리스트 형식이여서 문자열로 변경
    name_3 = name_2.split('<') # '<' 기호를 기준으로 나누었음
    name_last = name_3[1] # 나눈 것 중 2번째에 있는 리스트 선택
    name_last = name_last.split('>') # 선택한 것을 다시 '>' 기호를 기준으로 나누었음
    name_last = str(name_last[1]) #종목명만 다시 name_last에 저장


    info_list = []
    info_list.append(name_last)
    info_list.append(code_number)

    #종가, 전일대비, 거래량 내용을 추출/ 시세현황 테이블
    ifrs = soup.select('#svdMainGrid1 > table > tbody > tr.rwf > td' )
    for ifrs_data in ifrs:
        info_list.append(ifrs_data.get_text())
    print(info_list)
    return info_list

def get_all_detail_info(code_number):
    #종목코드에 따른 디테일한 정보를 전부 가져옴.
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임

    url = base_url.format(code_number)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')

    #기본 정보 0 
    detail_info = []
    group_info = []
    ifrs = soup.select('div.corp_group2 > dl > dd')
    for ifrs_data in ifrs:
        group_info.append(ifrs_data.text)
    detail_info.append(group_info)

    #시세현황 1
    group_info = []
    ifrs = soup.select('#svdMainGrid1 > table > tbody > tr')
    for ifrs_data in ifrs:
        ifrs_data = ifrs_data.select('td')
        for ifrs_data_td in ifrs_data:
                group_info.append(ifrs_data_td.text)
    detail_info.append(group_info)
    
    #실적이슈 2
    group_info = []
    ifrs = soup.select('#svdMainGrid2 > table > tbody > tr > td')
    for ifrs_data in ifrs:
        group_info.append(ifrs_data.get_text())
    detail_info.append(group_info)

 
    #운용사별 보유현황 3 
    group_info = []
    ifrs = soup.select('#svdMainGrid3 > table > tbody > tr')
    for ifrs_tr in ifrs:
        inst_list = [ifrs_tr.select_one('th').text]
        ifrs_tds = ifrs_tr.select('td')
        for ifrs_td in ifrs_tds:
            inst_list.append(ifrs_td.text)
        group_info.append(inst_list)
    detail_info.append(group_info)

    #주주현황 4 
    group_info = []
    ifrs = soup.select('#svdMainGrid4 > table > tbody > tr')
    for ifrs_tr in ifrs:
        inst_list = []
        temp = ifrs_tr.select_one('th > div')
        if temp.string == None:
            inst_list.append(temp.select_one('a').text)
        else:
            inst_list.append(temp.text)

        ifrs_tds = ifrs_tr.select('td')
        for ifrs_td in ifrs_tds:
            inst_list.append(ifrs_td.text)
        group_info.append(inst_list)
    detail_info.append(group_info)
    
    #주주구분현황 5
    group_info = []
    ifrs = soup.select('#svdMainGrid5 > table > tbody > tr')
    for ifrs_tr in ifrs:
        inst_list = []
        temp = ifrs_tr.select_one('th > div')
        if temp.string == None:
            inst_list.append(temp.select_one('a').text)
        else:
            inst_list.append(temp.text)
        
        ifrs_tds = ifrs_tr.select('td')
        for ifrs_td in ifrs_tds:
            inst_list.append(ifrs_td.text)
        group_info.append(inst_list)
    detail_info.append(group_info)

    print(detail_info)

    return(detail_info)

#가격변동 정보
def get_price_info(code_number):

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임
    
    url = base_url.format(code_number)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')

    ifrs = soup.select_one('#svdMainGrid1 > table > tbody > tr.rwf > td.r > span')
    delta_price = ifrs.text
    print(delta_price)
    if delta_price[0] == '-':
        return False
    elif delta_price[0] == '+':
        return True


#차트정보
import datetime
def get_chart_info(code_number):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    count = 10
    timeframe = 'day'
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe={}&count={}&requestType=0".format(code_number,timeframe,count)
    get_result = requests.get(url,headers = headers)
    bs_obj = BeautifulSoup(get_result.content, "html.parser")
    inf = bs_obj.select('item')
    columns = ['Date', 'Open' ,'High', 'Low', 'Close', 'Volume']
    df_inf = pd.DataFrame([], columns = columns, index = range(len(inf)))
    for i in range(len(inf)):
        df_inf.iloc[i] = str(inf[i]['data']).split('|')
    
    return df_inf.drop(['Open','High','Low'], axis=1)