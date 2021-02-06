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
    #종가, 전일대비, 거래량 내용을 추출/ 시세현황 테이블
    ifrs = soup.select('#svdMainGrid1 > table > tbody > tr.rwf > td' )
    info_list = []

    name = soup.select('.corp_group1 > h1') # '.'은 BeautifulSoup에서 태그를 추출할때 사용하는 것임.
    name_2 = str(name) # name이 리스트 형식이여서 문자열로 변경
    name_3 = name_2.split('<') # '<' 기호를 기준으로 나누었음
    name_last = name_3[1] # 나눈 것 중 2번째에 있는 리스트 선택
    name_last = name_last.split('>') # 선택한 것을 다시 '>' 기호를 기준으로 나누었음
    name_last = str(name_last[1]) #종목명만 다시 name_last에 저장

    info_list.append(name_last)
    info_list.append(code_number)
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
    #
    detail_info = []
    ifrs = soup.select('.corp_group2 > dl > dd')
    for ifrs_data in ifrs:
        detail_info.append(ifrs_data.get_text())

    #시세현황
    ifrs = soup.select('#svdMainGrid1 > table > tbody > tr')
    for ifrs_data in ifrs:
        ifrs_data = ifrs_data.select('td')
        for ifrs_data_td in ifrs_data:
                detail_info.append(ifrs_data_td.get_text())
    
    ifrs = soup.select('#svdMainGrid2 > table > tbody > tr > td')
    for ifrs_data in ifrs:
        detail_info.append(ifrs_data.get_text())

    print(detail_info)

    return(detail_info)
    



