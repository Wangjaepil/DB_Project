from flask import Flask, render_template, request, redirect
import sqlite3
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

kmdb_api_key = "1YPAB4TIEY4J2E16C4U9"

@app.route('/search', methods=['GET'])
def search_movie():
    movie_name = request.args.get('q', '')  # 검색할 영화 제목
    poster_url = ""

    # KMDb API 호출
    try:
        kmdb_url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"
        params = {
            "collection": "kmdb_new",
            "ServiceKey": kmdb_api_key,
            "title": movie_name,
            "listCount": 1  # 검색 결과 개수 제한
        }

        response = requests.get(kmdb_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("Data"):
                movie_info = data["Data"][0]["Result"][0]
                poster_url = movie_info.get("posters", "").split("|")[0]  # 포스터 URL 가져오기
    except Exception as e:
        print(f"Error fetching data from KMDb API: {e}")

    # 결과를 템플릿에 전달
    return render_template('search.html', name=movie_name, poster_url=poster_url)

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