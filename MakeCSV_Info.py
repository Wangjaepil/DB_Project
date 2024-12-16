import requests
import pandas as pd
import xml.etree.ElementTree as ET

# API 키와 기본 URL
api_key = "b435355aedd0abd28466ab96ff2297cf" #이거 키번호 깃허브에 올리면 안될거같은디
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml"

# 영화 코드 모아둔 CSV 파일에서 영화 코드 읽기
df = pd.read_csv("movieCd.csv", encoding="utf-8-sig")

# 영화 코드 리스트
movie_codes = df['movieCd'].tolist()

# 영화 정보를 저장할 리스트
movie_details = []

success_count = 0  # 데이터 가져온 영화 개수 세려고 만든건데 데이터 잘 가져오나 확인하는 역할정도

def safe_get_text(element, default=""):
    #유명하지 않은 영화는 데이터가 비어있는게 너무 많아서 그걸 빈 문자열로 대체해주는 함수
    return element.text if element is not None and element.text is not None else default

for movie_cd in movie_codes:
    params = {
        "key": api_key,
        "movieCd": movie_cd
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        movie_info = root.find(".//movieInfo")
        
        if movie_info is not None:
            movie_name = safe_get_text(movie_info.find("movieNm"))  # 영화명
            original_name = safe_get_text(movie_info.find("movieNmEn"))  # 영어 영화명
            production_year = safe_get_text(movie_info.find("prdtYear"))  # 제작 연도
            show_time = safe_get_text(movie_info.find("showTm"))  # 상영 시간
            release_date = safe_get_text(movie_info.find("openDt"))  # 개봉 연도
            production_status = safe_get_text(movie_info.find("prdtStatNm"))  # 제작 상태명
            movie_type = safe_get_text(movie_info.find("typeNm"))  # 영화 유형명
            production_country = safe_get_text(movie_info.find(".//nationNm"))  # 제작 국가명
            genre = safe_get_text(movie_info.find(".//genreNm"))  # 장르명
            directors = safe_get_text(movie_info.find(".//directors/director/peopleNm"))  # 감독명
            actors = [safe_get_text(actor) for actor in movie_info.findall(".//actors/actor/peopleNm")]  # 배우명 (최대 3명, None 처리)
            screening_type = safe_get_text(movie_info.find(".//showTypeNm"))  # 상영 형태명
            rating = safe_get_text(movie_info.find(".//watchGradeNm"))  # 관람 등급 명칭
            companies = safe_get_text(movie_info.find(".//companyCd"))  

            # 배우명 최대 3명 추출
            actor_names = ", ".join(actors[:3])

            # 필요한 항목을 영화 상세 정보로 저장
            movie_details.append({
                "movieCd": movie_cd,
                "movieNm": movie_name,
                "movieNmEn": original_name,
                "prdtYear": production_year,
                "showTm": show_time,
                "openDt": release_date,
                "prdtStatNm": production_status,
                "typeNm": movie_type,
                "nationNm": production_country,
                "genreNm": genre,
                "director": directors,
                "actor": actor_names, 
                "showTypeNm": screening_type,
                "watchGradeNm": rating,
                "companyCd":companies,
            })
            success_count += 1 
            print(f"성공적으로 데이터를 가져온 영화 수: {success_count}") #데이터 가져왔나 확인해보려고 씀

    else:
        print(f"영화 코드 {movie_cd}에 대한 정보를 가져오는 데 실패했습니다.")

# DataFrame으로 변환
movie_Info_df = pd.DataFrame(movie_details)

# 결과 CSV로 저장하기
output_file = "movie_Info_2.csv"
movie_Info_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"영화 상세 정보 CSV 파일 저장 완료: {output_file}") #끝난거 확인역할
