# 🎬 영화 정보 검색 및 관리 시스템

KOBIS Open API에서 수집한 영화·영화사 데이터를 SQLite에 저장하고, Flask 웹 페이지에서 검색하고 관리하는 데이터베이스 프로젝트입니다.

## 주요 기능

- 한글·영문 영화 제목 검색 및 상세 정보 조회
- 장르, 감독, 국가, 영화사, 개봉일, 관람등급 조건 검색
- KMDb API를 활용한 영화 포스터 조회
- 영화 및 영화사 정보 등록·수정·삭제
- 관심 영화 스크랩
- 검색 결과 페이지네이션

## 기술 스택

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Open API:** KOBIS, KMDb
- **Data Processing:** Pandas, XML, CSV

## 데이터베이스

- `movie_Info`: 영화 정보
- `CompanyCd`: 영화사 정보
- `CompanyCd`를 기준으로 영화와 영화사 데이터 연결

## 실행 방법

```bash
pip install flask requests pandas
python project.py
```

## 결과 화면
<img width="1425" height="1667" alt="DB_Project_homepage_full" src="https://github.com/user-attachments/assets/1d717794-0be8-453c-b6bd-f4cda5db0a84" />

<img width="1440" height="1200" alt="DB_Project_ironman_search_v2" src="https://github.com/user-attachments/assets/f8a55d78-d999-4997-9bd5-49fcd352b8a0" />

