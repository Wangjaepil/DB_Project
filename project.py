from flask import Flask, render_template, request, redirect
import sqlite3
import xml.etree.ElementTree as ET

app = Flask(__name__)

api_key = "1"  # 발급받은 API 키
base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.xml" #영화 코드를 가져올 수 있는 URL

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/home/Search/', methods=['GET'])
def SearchMovie():
    movie_name = request.args.get("q")  # HTML 폼에서 전달된 'q' 값을 가져옴
    return render_template("search.html", movie_name=movie_name)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)