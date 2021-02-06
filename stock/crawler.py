import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#파이선을 mysql에 연동해주는 코드

import mysql.connector
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, VARCHAR


#종목 코드 파일 불러오는 코드
def csv2list(filename):
    lists = []
    file = open('C:\\Users\\azxsd\\Downloads\\새 폴더\\stock_code.csv', 'r')
    while True:
        line = file.readline().rstrip("\n")
        if line:
            #line = line.split(",")
            lists.append(line)
        else:
            break
    return lists

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
    for ifrs_data in ifrs:
        info_list.append(ifrs_data.get_text())

    return info_list

    


def main():

    get_listinfo('000020')
    return

def asdf():
    accounts = csv2list('')
    #크롤링 코드 시작
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임

    test_add_df = pd.DataFrame()
    db_list = []
    i = 0
    for n in accounts:

        url = base_url.format(n) #{}에 종목코드 리스트 넣음
        
        html = requests.get(url, headers = headers).text
        soup = BeautifulSoup(html, 'html.parser')

        #연결 / 전체
        ifrs = soup.select('#highlight_D_A > table')
        ifrs_html = str(ifrs) #html 정보를 문자열로 변경
        #연간
        ifrs = soup.select('#highlight_D_Y > table')
        ifrs_html = str(ifrs) #html 정보를 문자열로 변경
        #분기
        ifrs = soup.select('#highlight_D_Q > table')
        ifrs_html = str(ifrs) #html 정보를 문자열로 변경

        #별도 / 전체
        ifrs_gaap = soup.select('#highlight_B_A > table')
        ifrs_gaap_htmlA = str(ifrs_gaap) #html 정보를 문자열로 변경
        #연간
        ifrs_gaap = soup.select('#highlight_B_Y > table')
        ifrs_gaap_htmlY = str(ifrs_gaap) #html 정보를 문자열로 변경
        #분기
        ifrs_gaap = soup.select('#highlight_B_Q > table')
        ifrs_gaap_htmlQ = str(ifrs_gaap) #html 정보를 문자열로 변경
        


        name = soup.select('.corp_group1 > h1') # '.'은 BeautifulSoup에서 태그를 추출할때 사용하는 것임.
        name_2 = str(name) # name이 리스트 형식이여서 문자열로 변경
        name_3 = name_2.split('<') # '<' 기호를 기준으로 나누었음
        name_last = name_3[1] # 나눈 것 중 2번째에 있는 리스트 선택
        name_last = name_last.split('>') # 선택한 것을 다시 '>' 기호를 기준으로 나누었음
        name_last = str(name_last[1]) #종목명만 다시 name_last에 저장

        db_list.append([i+1,n,name_last])

        name = soup.select('.corp_group1')
        try:
            ifrs_df_list = pd.read_html(ifrs_html) #pandas read_html로 정보 읽기
            ifrs_df_list2 = pd.read_html(ifrs_gaap_htmlA) #pandas read_html로 정보 읽기
        except:
            pass #조회가 되지 않는 ETN 코드도 포함되어 있어 오류 발생할때 무시. (추후 개선하면 좋음)

        ifrs_df = ifrs_df_list[0]
        ifrs_df2 = ifrs_df_list2[0]
        try:
            ifrs_df.columns = ifrs_df.columns.droplevel([0]) #불필요한 columns 삭제
            ifrs_df2.columns = ifrs_df2.columns.droplevel([0]) #불필요한 columns 삭제
        except:
            pass #삭제할 columns이 없을 경우 무시.

        try:
            test_df = ifrs_df.set_index('IFRS(연결)').T #데이터프레임 행렬 변환
        except:
            test_df = ifrs_df2.set_index('GAAP(개별)').T #데이터프레임 행렬 변환
        
        
        test_df['종목명'] = name_last #크롤링한 종목명을 '종목명' 인덱스 아래 데이터 입력
        test_df.reset_index(drop=False, inplace=True) #drop=False 인덱스를 리셋한 후 삭제할 것인지 / inplace=True 원본 객체를 변경할지 여부
        test_add_df = pd.concat([test_add_df, test_df]) #추후 다른 종목을 이어서 데이터를 넣을때 사용
        i += 1
        #end for
    
    db_path = "mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8".format('root', 'Gnlwls01!', 'localhost','django_db')

    engine = create_engine(db_path, encoding='utf-8')
    conn = engine.connect
    labels = ['id','code','name']
    db_df = pd.DataFrame.from_records(db_list,columns=labels)

    db_df.to_sql(name='stock_stockinfo', con=engine, if_exists='replace', index=False)
    return test_df

if __name__ == '__main__':
    main()

