from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

# 임시 데이터베이스 대체 (실제 DB 사용 시 수정)
user_movies = [
    {"id": 1, "name": "영화1", "movie_id": 101},
    {"id": 2, "name": "영화2", "movie_id": 102},
]

@app.route('/home/my_page')
def my_page():
    return render_template('my_page.html', movies=user_movies)

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
            movie_data = data["Data"][0]
            
            # 'Result' 키가 있는지 확인하고, 없으면 빈 리스트로 처리
            # 이 과정을 왜 하냐면 KMDB에 없는 영화일 수 있거든.
            result_data = movie_data.get("Result", [])
            if result_data:
                posters = result_data[0].get("posters", None)
                if posters:
                    poster_url = posters.split('|')[0]  # 첫 번째 포스터 URL만 사용
                    return poster_url
            else:
                print("No 'Result' data found.")
        else:
            print("No 'Data' or 'Data' is empty.")
        return None  # 결과가 없을 경우

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from KMDb API: {e}")
        return None


def get_poster_from_kmdb_Cd(movie_cd):
    # KMDb API 엔드포인트 및 API 키
    api_url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"
    api_key = "1YPAB4TIEY4J2E16C4U9"  # 발급받은 API 키를 입력

    # API 요청 파라미터
    params = {
        "collection": "kmdb_new2",
        "ServiceKey": api_key,
        "movieId": movie_cd,  # 영화 코드로 검색
        "detail": "Y"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        data = response.json()  # JSON 응답 파싱

        # 포스터 URL 추출 (첫 번째 포스터만 선택)
        if "Data" in data and data["Data"]:
            movie_data = data["Data"][0]
            
            # 'Result' 키가 있는지 확인하고, 없으면 빈 리스트로 처리
            result_data = movie_data.get("Result", [])
            if result_data:
                posters = result_data[0].get("posters", None)
                if posters:
                    poster_url = posters.split('|')[0]  # 첫 번째 포스터 URL만 사용
                    return poster_url
            else:
                print("No 'Result' data found.")
        else:
            print("No 'Data' or 'Data' is empty.")
        return None  # 결과가 없을 경우

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from KMDb API: {e}")
        return None
    

@app.route('/home/CRUD/', methods=['GET', 'POST'])
def insert_movie():
    if request.method == 'POST':
        action = request.form.get('action')

        # 삽입 요청 처리
        if action == 'insert':
            movieCd = request.form['movieCd']
            영화명 = request.form['영화명']
            영화명_영어 = request.form['영화명(영어)']
            제작연도 = request.form['제작연도']
            상영시간 = request.form['상영시간']
            개봉일자 = request.form['개봉일자']
            제작상태 = request.form['제작상태']
            영화유형 = request.form['영화유형']
            제작국가 = request.form['제작국가']
            장르 = request.form['장르']
            감독 = request.form['감독']
            주연배우 = request.form['주연배우']
            상영형태 = request.form['상영형태']
            관람등급 = request.form['관람등급']
            영화사코드 = request.form['영화사코드']

            # 데이터베이스에 연결
            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()

            try:
                if 영화사코드:
                    # 영화사 코드가 CompanyCd 테이블에 존재하는지 확인
                    cursor.execute("SELECT COUNT(*) FROM CompanyCd WHERE CompanyCd = ?", (영화사코드,))
                    company_exists = cursor.fetchone()[0]

                    if company_exists == 0:
                        success_message = "해당 영화사 코드가 존재하지 않습니다. 올바른 영화사 코드를 입력하세요."
                        return render_template('CRUD.html', success_message=success_message)
                
                # 삽입 쿼리 실행
                cursor.execute("""
                    INSERT INTO movie_Info (
                        movieCd, 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉일자,
                        제작상태, 영화유형, 제작국가, 장르, 감독, 주연배우, 상영형태, 관람등급, CompanyCd
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    movieCd, 영화명, 영화명_영어, 제작연도, 상영시간, 개봉일자,
                    제작상태, 영화유형, 제작국가, 장르, 감독, 주연배우, 상영형태, 관람등급, 영화사코드
                ))

                # 커밋하여 데이터베이스에 반영
                conn.commit()
                success_message = "영화 정보가 성공적으로 삽입되었습니다."

            except sqlite3.IntegrityError:
                # movieCd가 Primary Key라서 중복이 발생할 경우 에러 메시지 처리
                success_message = "영화 Code가 중복되었습니다. 다른 Code를 사용해 주세요."
            finally:
            # 연결 종료
                conn.close()

            # 삽입 후 성공 메시지를 같은 페이지에 표시
            return render_template('CRUD.html', success_message=success_message)

        # 삭제 요청 처리
        elif action == 'delete':
            movieCd = request.form['movieCd']
            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()

            try:
                # movieCd가 존재하는지 확인
                cursor.execute("SELECT * FROM movie_Info WHERE movieCd = ?", (movieCd,))
                movie = cursor.fetchone()

                if movie:
                    # movieCd를 기준으로 영화 삭제
                    cursor.execute("DELETE FROM movie_Info WHERE movieCd = ?", (movieCd,))
                    conn.commit()

                    success_message = "영화가 성공적으로 삭제되었습니다."
                else:
                    success_message = f"영화 Code '{movieCd}'는 존재하지 않습니다다."
            except sqlite3.Error as e:
                success_message = f"영화를 삭제하는데 문제가 발생했습니다: {e}"
            finally:
                conn.close()

            # 삭제 후 페이지에 메시지 전달
            return render_template('CRUD.html', success_message=success_message)

        elif action == 'edit':
            searchMovieCd = request.form.get('searchMovieCd')
            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()
                
            try:
                cursor.execute("SELECT * FROM movie_Info WHERE movieCd = ?", (searchMovieCd,))
                row = cursor.fetchone()

                if row:
                    # 검색 결과 매핑
                    movie_data = {
                        'movieCd': row[0], '영화명': row[1], '영화명(영어)': row[2],
                        '제작연도': row[3], '상영시간': row[4], '개봉일자': row[5],
                        '제작상태': row[6], '영화유형': row[7], '제작국가': row[8],
                        '장르': row[9], '감독': row[10], '주연배우': row[11],
                        '상영형태': row[12], '관람등급': row[13], '영화사코드': row[14]
                    }
                    return render_template('CRUD.html', update_stage="edit", movie_data=movie_data)
                else:
                    success_message = "해당 MovieCd가 데이터베이스에 없습니다."
                    return render_template('CRUD.html', success_message=success_message, update_stage=None)
            except sqlite3.Error as e:
                success_message = f"데이터베이스 오류 발생: {e}"
                return render_template('CRUD.html', success_message=success_message, update_stage=None)
            finally:
                conn.close()

        # 수정 제출 요청
        elif action == 'update_submit':
            movieCd = request.form.get('movieCd')
            updated_data = (
                request.form.get('영화명'), request.form.get('영화명(영어)'),
                request.form.get('제작연도'), request.form.get('상영시간'),
                request.form.get('개봉일자'), request.form.get('제작상태'),
                request.form.get('영화유형'), request.form.get('제작국가'),
                request.form.get('장르'), request.form.get('감독'),
                request.form.get('주연배우'), request.form.get('상영형태'),
                request.form.get('관람등급'), request.form.get('영화사코드'), movieCd
            )

            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()
            try:
                # 영화사 코드가 NULL이 아닌 경우에만 존재 여부를 확인
                영화사코드 = request.form.get('영화사코드')
                if 영화사코드:
                    cursor.execute("SELECT COUNT(*) FROM CompanyCd WHERE CompanyCd = ?", (영화사코드,))
                    company_exists = cursor.fetchone()[0]
                    if company_exists == 0:
                        success_message = "해당 영화사 코드가 존재하지 않습니다. 올바른 영화사 코드를 입력하세요."
                        return render_template('CRUD.html', success_message=success_message)
                cursor.execute("""
                    UPDATE movie_Info
                    SET 영화명 = ?, "영화명(영어)" = ?, 제작연도 = ?, 상영시간 = ?, 개봉일자 = ?, 제작상태 = ?,
                        영화유형 = ?, 제작국가 = ?, 장르 = ?, 감독 = ?, 주연배우 = ?, 상영형태 = ?, 관람등급 = ?, CompanyCd = ?
                    WHERE movieCd = ?
                """, updated_data)
                conn.commit()
                success_message = "영화 정보가 성공적으로 수정되었습니다."
            except sqlite3.Error as e:
                success_message = f"수정 중 오류 발생: {e}"
            finally:
                conn.close()

            return render_template('CRUD.html', success_message=success_message)
    # GET 요청 시 빈 폼을 반환
    return render_template('CRUD.html', success_message=None)

@app.route('/home/CRUD_Cp/', methods=['GET', 'POST'])
def CRUD_company():
    if request.method == 'POST':
        action = request.form.get('action')

        # 삽입 요청 처리
        if action == 'insert':
            CompanyCd = request.form['CompanyCd']
            영화사이름 = request.form['영화사이름']
            영화사분류 = request.form['영화사분류']
            영화사대표 = request.form['영화사대표']

            # 데이터베이스에 연결
            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()

            try:
                # 삽입 쿼리 실행
                cursor.execute("""
                    INSERT INTO CompanyCd (
                        CompanyCd, 영화사, "영화사 분류", "영화사 대표"
                    ) VALUES (?, ?, ?, ?)
                """, (
                    CompanyCd, 영화사이름, 영화사분류, 영화사대표
                ))

                # 커밋하여 데이터베이스에 반영
                conn.commit()
                success_message = "영화사 정보가 성공적으로 삽입되었습니다."
            except sqlite3.IntegrityError:
                # CompanyCd가 Primary Key라서 중복이 발생할 경우 에러 메시지 처리
                success_message = "영화사 Code가 중복되었습니다. 다른 Code를 사용해 주세요."
            finally:
                # 연결 종료
                conn.close()

            # 삽입 후 성공 메시지를 같은 페이지에 표시
            return render_template('CRUD_company.html', success_message=success_message)

        # 삭제 요청 처리
        elif action == 'delete':
            CompanyCd = request.form['CompanyCd']
            conn = sqlite3.connect('Movie_Info.db')
            conn.execute("PRAGMA foreign_keys = ON;")  # 외래키 제약 활성화
            cursor = conn.cursor()

            try:
                # CompanyCd가 존재하는지 확인
                cursor.execute("SELECT * FROM CompanyCd WHERE CompanyCd = ?", (CompanyCd,))
                movie = cursor.fetchone()

                if movie:
                    # CompanyCd를 기준으로 영화 삭제
                    cursor.execute("DELETE FROM CompanyCd WHERE CompanyCd = ?", (CompanyCd,))
                    conn.commit()

                    success_message = "영화사가 성공적으로 삭제되었습니다."
                else:
                    success_message = f"영화사 Code '{CompanyCd}'는 존재하지 않습니다."
            except sqlite3.Error as e:
                success_message = f"영화사를 삭제하는데 문제가 발생했습니다: {e}"
            finally:
                conn.close()

            # 삭제 후 페이지에 메시지 전달
            return render_template('CRUD_company.html', success_message=success_message)

        elif action == 'edit':
            searchCompanyCd = request.form.get('searchCompanyCd')
            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()
                
            try:
                cursor.execute("SELECT * FROM CompanyCd WHERE CompanyCd = ?", (searchCompanyCd,))
                row = cursor.fetchone()

                if row:
                    # 검색 결과 매핑
                    company_data = {
                        'CompanyCd': row[0], '영화사이름': row[1], '영화사분류': row[2],
                        '영화사대표': row[3]
                    }
                    return render_template('CRUD_company.html', update_stage="edit", company_data=company_data)
                else:
                    success_message = "해당 CompanyCd가 데이터베이스에 없습니다."
                    return render_template('CRUD_company.html', success_message=success_message, update_stage=None)
            except sqlite3.Error as e:
                success_message = f"데이터베이스 오류 발생: {e}"
                return render_template('CRUD_company.html', success_message=success_message, update_stage=None)
            finally:
                conn.close()

        # 수정 제출 요청
        elif action == 'update_submit':
            CompanyCd = request.form.get('CompanyCd')
            updated_data = (
                request.form.get('영화사이름'), request.form.get('영화사분류'),
                request.form.get('영화사대표'), CompanyCd
            )

            conn = sqlite3.connect('Movie_Info.db')
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE CompanyCd
                    SET 영화사 = ?, "영화사 분류" = ?, "영화사 대표" = ?
                    WHERE CompanyCd = ?
                """, updated_data)
                conn.commit()
                success_message = "영화 정보가 성공적으로 수정되었습니다."
            except sqlite3.Error as e:
                success_message = f"수정 중 오류 발생: {e}"
            finally:
                conn.close()

            return render_template('CRUD_company.html', success_message=success_message)
    # GET 요청 시 빈 폼을 반환
    return render_template('CRUD_company.html', success_message=None)

@app.route('/home/Search/', methods=['GET'])
def SearchMovie():
    movie_name = request.args.get("q")  # 영화명
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()

    # 데이터베이스에서 영화 정보 검색
    cursor.execute("PRAGMA table_info(movie_Info)")
    Attribute_name = cursor.fetchall()
    Att_name = [ATName[1] for ATName in Attribute_name][1:]  # 첫 번째는 영화코드라서 제외
    Att_name = [name for name in Att_name if name != "CompanyCd"]
    Att_name.append("영화사")
    Att_name.append("영화사 분류")
    Att_name.append("영화사 대표")

    # 영화 이름으로 검색
    Info = cursor.execute(
        'SELECT 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉일자, 제작상태, 영화유형, 제작국가, 장르, 감독, 주연배우, 상영형태, 관람등급, 영화사, "영화사 분류", "영화사 대표" '
        'FROM movie_Info '
        'LEFT JOIN CompanyCd ON movie_Info.CompanyCd = CompanyCd.CompanyCd '
        'WHERE 영화명 = ? OR "영화명(영어)" = ?', 
        (movie_name, movie_name)).fetchall()
    db.close()

    # KMDb API에서 포스터 URL 가져오기
    poster_url = get_poster_from_kmdb(movie_name)

    if len(Info) > 1:
        # 영화명이 중복되는 경우, 상세 페이지로 리디렉션
        return redirect(url_for('SearchDetail', movie_name=movie_name))
    elif len(Info) == 1:
        # 영화명이 유일한 경우, 바로 상세 페이지로 이동
        return render_template("search.html", name=movie_name, Att_name=Att_name, Info=Info, zip=zip, poster_url=poster_url)

    
@app.route('/home/Search/Detail/', methods=['GET'])
def SearchDetail():
    movie_name = request.args.get("movie_name")
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()

    # 영화코드으로 검색 결과 가져오기
    Info = cursor.execute(
        'SELECT MovieCd, 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉일자, 제작상태, 영화유형, 제작국가, 장르, 감독, 주연배우, 상영형태, 관람등급, 영화사, "영화사 분류", "영화사 대표" '
        'FROM movie_Info '
        'LEFT JOIN CompanyCd ON movie_Info.CompanyCd = CompanyCd.CompanyCd '
        'WHERE 영화명 = ? OR "영화명(영어)" = ?', 
        (movie_name, movie_name)).fetchall()
    db.close()

    # 영화 코드 목록과 함께 상세 페이지 렌더링
    return render_template('search_detail.html', Movie_table=Info)



@app.route('/movie_detail/<movie_code>')
def movie_detail(movie_code):
    print(f"Movie Code: {movie_code}")  # movie_code가 제대로 전달되는지 확인
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()

    # 영화 코드로 검색 결과 가져오기
    Info = cursor.execute(
        'SELECT MovieCd, 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉일자, 제작상태, 영화유형, 제작국가, 장르, 감독, 주연배우, 상영형태, 관람등급, 영화사, "영화사 분류", "영화사 대표" '
        'FROM movie_Info '
        'LEFT JOIN CompanyCd ON movie_Info.CompanyCd = CompanyCd.CompanyCd '
        'WHERE MovieCd = ?', 
        (movie_code,)).fetchall()
    db.close()

    if not Info:
        return "영화 정보가 없습니다."

    # KMDb API에서 포스터 URL 가져오기 (포스터가 없을 경우 빈 문자열을 반환)
    poster_url = get_poster_from_kmdb_Cd(movie_code) or ""

    # 속성 이름 리스트
    att_names = [
        "영화 코드", "영화명", "영화명(영어)", "제작연도", "상영시간", "개봉일자", 
        "제작상태", "영화유형", "제작국가", "장르", "감독", "주연배우", 
        "상영형태", "관람등급", "영화사", "영화사 분류", "영화사 대표"
    ]

    # 영화 정보 페이지로 전달 (포스터가 없으면 빈 문자열 전달)
    return render_template('movie_detail.html', 
                           movie=Info[0], 
                           att_names=att_names, 
                           poster_url=poster_url,
                           zip=zip,
                           name=Info[0][1])



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
    LEFT JOIN CompanyCd ON movie_Info.CompanyCd = CompanyCd.CompanyCd
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
    ORDER BY 개봉일자 DESC  -- 개봉일자를 기준으로 내림차순 정렬
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
        total_results=total_results,
        current_page=current_page,
        total_pages=total_pages,
        page_range=page_range,
        search_params=search_params,  # 검색 조건 추가
    )



if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)