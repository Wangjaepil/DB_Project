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
    db = sqlite3.connect('./DB_Project/movie.db')
    cursor = db.cursor()
    Info = cursor.execute('SELECT 영화명, 제작연도, 국적, 유형, 장르, 제작상태, 감독, 제작사  FROM Movie_Search WHERE 영화명=?', (movie_name,)).fetchall()
    db.close()
    return render_template("search.html", name=movie_name, Imformation=Info)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)