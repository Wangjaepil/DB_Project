import requests
import pandas as pd
import xml.etree.ElementTree as ET

# API 키와 기본 URL
api_key = "b435355aedd0abd28466ab96ff2297cf"  # API Key
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.xml"

# 영화사 코드 모아둔 CSV 파일에서 영화사 코드 읽기
df = pd.read_csv("CompanyCd.csv", encoding="utf-8-sig")

# 영화사 코드 리스트
company_codes = df['CompanyCd'].tolist()

# 영화사 정보를 저장할 리스트
company_details = []

success_count = 0  # 데이터 가져온 영화사 개수 확인

def safe_get_text(element, default=""):
    # NULL값을 빈 문자열로 대체해주는 함수
    return element.text if element is not None and element.text is not None else default

for company_cd in company_codes:
    params = {
        "key": api_key,
        "companyCd": company_cd
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        company_info = root.find(".//companyInfo")
        
        if company_info is not None:
            company_name = safe_get_text(company_info.find("companyNm"))  # 영화사명
            ceoNm = safe_get_text(company_info.find("ceoNm"))  # 대표자명

            # 영화 목록 추출
            films = []
            for filmo in company_info.findall(".//filmo"):
                movie_name = safe_get_text(filmo.find("movieNm"))
                company_part = safe_get_text(filmo.find("companyPartNm"))
                films.append(f"{movie_name} ({company_part})")  # 영화명과 분류명을 합쳐서 저장

            # 영화사 정보와 영화 목록을 결합하여 저장
            company_details.append({
                "companyCd": company_cd,  # 영화사 코드
                "companyNm": company_name,  # 영화사명
                "ceoNm": ceoNm,  # 대표자명
                "movies": "; ".join(films)  # 영화명과 분류명을 이어서 저장
            })
            success_count += 1
            print(f"성공적으로 데이터를 가져온 영화사 정보: {success_count}, {company_name}")  # 데이터 확인

    else:
        print(f"영화사 코드 {company_cd}에 대한 정보를 가져오는 데 실패했습니다.")

# DataFrame으로 변환
company_info_df = pd.DataFrame(company_details)

# 결과 CSV로 저장하기
output_file = "Company_Info.csv"
company_info_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"영화사 정보 CSV 파일 저장 완료: {output_file}")
