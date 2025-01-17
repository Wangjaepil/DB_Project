import requests
import pandas as pd
import xml.etree.ElementTree as ET

# API 정보
api_key = "749cea3b1d8320b9e085ae3402483fc8"  # API Key 근데 이거 깃허브에 올리면 안될거같은데
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.xml"
params = {
    "key": api_key,
    "curPage": 1, #한 페이지에 데이터가 100개뿐이라 페이지 넘기면서 찾자
    "itemPerPage": 100 #여러 테스트 한 결과 한 페이지에 데이터 100개라는걸 파악했다
}

Company = []  # 영화사코드하고 영화사이름 저장할 곳

while True:
    # API 호출하고
    response = requests.get(url, params=params)
    if response.status_code != 200: #200은 html 요청성공 코드
        print(f"API 호출 실패: {response.status_code}")
        break
    
    # XML 연결하는 법이라네요
    root = ET.fromstring(response.content)
    
    # 데이터 추출해보자
    company = root.findall(".//company") #내가 XML확인해보니까 .//company 파일 밑에 다 있길래 이렇게 하고
    if not company:  # 더 이상 데이터가 없으면 종료하자
        break
    
    for companies in company:
        Company_Cd = {
            "CompanyCd": companies.findtext("companyCd"),  # 영화사 코드
            "CompanyNm": companies.findtext("companyNm"),  # 영화사 이름
            "companyPartNames": companies.findtext("companyPartNames"),  # 영화사 코드
            "ceoNm": companies.findtext("ceoNm")   # 영화사 이름
        }
        Company.append(Company_Cd)
    
    print(f"Page {params['curPage']} 처리 완료. {len(company)}개 데이터 추가.") #데이터 읽어오다가 중간에 끊기는 경우가 있어서 어디서 끊기는지 확인을 해주려고...
    
    # 다음 페이지로 이동, 이거 안하면 첫페이지에 있는 데이터밖에 못가져옴
    params["curPage"] += 1

# 데이터프레임 생성 및 CSV파일로 저장하기
df = pd.DataFrame(Company)
output_file = "CompanyCd_.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"CSV 파일 저장 완료: {output_file}") #파일 저장 되었나 확인해주고
print(f"총 데이터 개수: {len(Company)}") #데이터 개수 맞는지 확인해주고
