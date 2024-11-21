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
    db = sqlite3.connect('.//movie_Info.db')
    cursor = db.cursor()
    query = '''
    SELECT 영화명, 장르, 제작국가, 감독, 관람등급, 영화사
    FROM movie_Info
    WHERE 1=1
    '''
    params = []
    if Country:
        query += " AND 제작국가=?"
        params.append(Country)
    if Director:
        query += " AND 감독=?"
        params.append(Director)
    if Company:
        query += " AND 영화사=?"
        params.append(Company)
    Movie_table = cursor.execute(query, tuple(params)).fetchall()

    db.close()
    return render_template('Advanced_Search.html', Movie_table=Movie_table)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)