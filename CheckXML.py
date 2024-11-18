import requests
import xml.etree.ElementTree as ET

# API 요청 설정
api_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml"
api_key = "1"  # 키 값 올리면 안될거같아서 다른걸로 대체.
movie_cd = "20183782"  # 테스트용 영화 코드(기생충)

# API 요청
params = {
    "key": api_key,
    "movieCd": movie_cd
}
response = requests.get(api_url, params=params)

if response.status_code == 200:
    # XML 파싱
    root = ET.fromstring(response.content)

    # 출력해서 XML 구조 확인해보자
    print("XML 전체 구조:")
    print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
else:
    print(f"API 요청 실패: {response.status_code}")
