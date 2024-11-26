from flask import Flask, render_template, request, redirect
import sqlite3
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/home/Search/', methods=['GET'])
def SearchMovie():
    movie_name = request.args.get("q")  # HTML 폼에서 전달된 'q' 값, 즉 이름 입력한 거를 가져옴
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(movie_Info)")
    Attribute_name = cursor.fetchall()
    Att_name = [ATName[1] for ATName in Attribute_name][1:] #movie_Info에서 첫번째 데이터는 영화코드라서 그거 빼고 추출하기 위한 코드
    Info = cursor.execute('SELECT 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉일자, 제작상태, 영화유형, 제작국가,' 
                          '장르, 감독, 주연배우, 상영형태, 관람등급, 영화사 FROM movie_Info WHERE 영화명=? or "영화명(영어)"=?', 
                          (movie_name, movie_name,)).fetchall()
    db.close()
    return render_template("search.html", name=movie_name, Att_name=Att_name, Info=Info, zip=zip)

@app.route('/home/Advanced_Search/')
def Advanced():
    Director = request.args.get("director")
    Country = request.args.get("country")
    Company = request.args.get("studio")
    Opdate_start = request.args.get("date_start")
    Opdate_end = request.args.get("date_end")
    WatchGrade = request.args.getlist("Grade")
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()
    query = '''
    SELECT 영화명, 장르, 개봉일자, 제작국가, 감독, 관람등급, 영화사
    FROM movie_Info
    WHERE 1=1
    '''

    grade_mapping = {
    "allG": ["전체관람가", "연소자관람가", "미성년자관람가","모든 관람객이 관람할 수 있는 등급"],
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
        query += " AND 개봉일자 >= ?"
        params.append(Opdate_start.replace("-", "")) #date형식으로 받았는데 데이터에는 int형식이라서 이걸로 바꿈
    if Opdate_end:
        query += " AND 개봉일자 <= ?"
        params.append(Opdate_end.replace("-", "")) #이것도 마찬가지
    if Country:
        query += " AND 제작국가=?"
        params.append(Country)
    if Director:
        query += " AND 감독=?"
        params.append(Director)
    if Company:
        query += " AND 영화사=?"
        params.append(Company)
    if gradeNm:
        query += " AND 관람등급 IN (" + ",".join(["?"] * len(gradeNm)) + ")"
        params.extend(gradeNm)
    Movie_table = cursor.execute(query, tuple(params)).fetchall()
    db.close()
    return render_template('Advanced_Search.html', Movie_table=Movie_table)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)