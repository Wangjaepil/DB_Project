from flask import Flask, render_template, request, redirect
import sqlite3
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)

api_key = "b435355aedd0abd28466ab96ff2297cf"  # 발급받은 API 키
find_code_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.xml" #영화 코드를 가져올 수 있는 URL
movie_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml" #영화 정보를 가져올 수 있는 URL

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
    Att_name = [ATName[1] for ATName in Attribute_name][1:]
    Info = cursor.execute('SELECT 영화명, "영화명(영어)", 제작연도, 상영시간, 개봉연도, 제작상태, 영화유형, 제작국가,' 
                          '장르, 감독, 주연배우, 상영형태, 관람등급, 영화사 FROM movie_Info WHERE 영화명=? or "영화명(영어)"=?', 
                          (movie_name, movie_name,)).fetchall()
    db.close()
    return render_template("search.html", name=movie_name, Att_name=Att_name, Info=Info, zip=zip)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)