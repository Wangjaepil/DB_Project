from flask import Flask, render_template, request, redirect
import sqlite3
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

def get_poster_from_kmdb(movie_name):
    # KMDb API 엔드포인트 및 API 키
    api_url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"
    api_key = "1YPAB4TIEY4J2E16C4U9"  # 발급받은 API 키를 입력

    # API 요청 파라미터
    params = {
        "collection": "kmdb_new2",
        "ServiceKey": api_key,
        "title": movie_name,  # 검색할 영화 제목
        "detail": "Y"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        data = response.json()  # JSON 응답 파싱

        # 포스터 URL 추출 (첫 번째 포스터만 선택)
        if "Data" in data and data["Data"]:
            movie_data = data["Data"][0]["Result"][0]
            posters = movie_data.get("posters", None)
            if posters:
                # 첫 번째 포스터 URL만 반환
                poster_url = posters.split('|')[0]  
                return poster_url
            else:
                return None  # 포스터가 없을 경우
        else:
            return None  # 결과가 없을 경우
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from KMDb API: {e}")
        return None

@app.route('/home/Search/', methods=['GET'])
def SearchMovie():
    movie_name = request.args.get("q")  # HTML 폼에서 전달된 'q' 값, 즉 이름 입력한 거를 가져옴
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()

    # 데이터베이스에서 영화 정보 검색
    cursor.execute("PRAGMA table_info(movie_Info)")
    Attribute_name = cursor.fetchall()
    Att_name = [ATName[1] for ATName in Attribute_name][1:] #movie_Info에서 첫번째 데이터는 영화코드라서 그거 빼고 추출하기 위한 코드
    Att_name.append("영화사 분류")
    Att_name.append("영화사 대표")
    Info = cursor.execute(
    'SELECT 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉일자, 제작상태, 영화유형, 제작국가, 장르, 감독, 주연배우, 상영형태, 관람등급, 영화사, "영화사 분류", "영화사 대표" '
    'FROM movie_Info '
    'JOIN CompanyCd ON movie_Info.영화사 = CompanyCd.CompanyNm '
    'WHERE 영화명 = ? OR "영화명(영어)" = ?', 
    (movie_name, movie_name)).fetchall()

    db.close()

    # KMDb API에서 포스터 URL 가져오기
    poster_url = get_poster_from_kmdb(movie_name)

    return render_template("search.html", name=movie_name, Att_name=Att_name, Info=Info, zip=zip, poster_url=poster_url)
    

@app.route('/home/Advanced_Search/')
def Advanced():
    Director = request.args.get("director")
    Country = request.args.get("country")
    Company = request.args.get("studio")
    Opdate_start = request.args.get("date_start")
    Opdate_end = request.args.get("date_end")
    genrelist = request.args.getlist("genre")
    WatchGrade = request.args.getlist("Grade")
    current_page = int(request.args.get("page", 1))  # 기본값은 1페이지
    limit_value = 10  # 페이지당 10개
    offset_value = (current_page - 1) * limit_value  # 시작 위치

    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()

    # 검색 조건 쿼리
    base_query = '''
    FROM movie_Info
    WHERE 1=1
    '''

    grade_mapping = {
        "allG": ["전체관람가", "연소자관람가", "미성년자관람가", "모든 관람객이 관람할 수 있는 등급"],
        "tweG": ["12세이상관람가", "12세관람가", "12세 미만인 자는 관람할 수 없는 등급", "연소자관람불가", "중학생이상관람가"],
        "fifG": ["15세관람가", "15세이상관람가", "고등학생이상관람가", "국민학생관람불가", "15세 미만인 자는 관람할 수 없는 등급"],
        "aduG": ["청소년관람불가", "18세관람가", "미성년자관람불가", "18세 미만인 자는 관람할 수 없는 등급"],
        "limG": ["제한상영가"]
    }
    gradeNm = []
    for grade in WatchGrade:
        if grade in grade_mapping:
            gradeNm.extend(grade_mapping[grade])

    params = []

    if Opdate_start:
        base_query += " AND 개봉일자 >= ?"
        params.append(Opdate_start.replace("-", ""))
    if Opdate_end:
        base_query += " AND 개봉일자 <= ?"
        params.append(Opdate_end.replace("-", ""))
    if Country:
        base_query += " AND 제작국가=?"
        params.append(Country)
    if Director:
        base_query += " AND 감독=?"
        params.append(Director)
    if Company:
        base_query += " AND 영화사=?"
        params.append(Company)
    if genrelist:
        base_query += " AND 장르 IN (" + ",".join(["?"] * len(genrelist)) + ")"
        params.extend(genrelist)
    if gradeNm:
        base_query += " AND 관람등급 IN (" + ",".join(["?"] * len(gradeNm)) + ")"
        params.extend(gradeNm)

    # 전체 데이터 개수 계산
    count_query = f"SELECT COUNT(*) {base_query}"
    total_results = cursor.execute(count_query, tuple(params)).fetchone()[0]
    total_pages = (total_results + limit_value - 1) // limit_value

    # 페이지 데이터 조회
    query = f'''
    SELECT 영화명, 장르, 개봉일자, 제작국가, 감독, 관람등급, 영화사
    {base_query}
    LIMIT ? OFFSET ?
    '''
    params.extend([limit_value, offset_value])  # LIMIT, OFFSET 값 추가
    Movie_table = cursor.execute(query, tuple(params)).fetchall()

    # 페이지네이션 처리 (5개 단위)
    start_page = max(1, current_page - 2)  # 현재 페이지 기준 앞뒤로 2개씩 표시
    end_page = min(total_pages, start_page + 4)  # 최대 5개까지 표시
    page_range = range(start_page, end_page + 1)

    db.close()

# 검색 조건 유지용 딕셔너리
    search_params = {
        "director": Director,
        "country": Country,
        "studio": Company,
        "date_start": Opdate_start,
        "date_end": Opdate_end,
        "genre": genrelist,
        "Grade": WatchGrade,
    }
    return render_template(
        'Advanced_Search.html',
        Movie_table=Movie_table,
        current_page=current_page,
        total_pages=total_pages,
        page_range=page_range,
        search_params=search_params,  # 검색 조건 추가
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)


# if __name__ == '__main__':
#     movie_name = "범죄도시2"
#     poster_url = get_poster_from_kmdb(movie_name)
#     if poster_url:
#         print(f"영화: {movie_name}\n포스터 URL: {poster_url}")
#     else:
#         print(f"영화: {movie_name}\n포스터 URL을 찾을 수 없습니다.")