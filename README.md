🎬 영화 정보 검색 및 관리 시스템

영화진흥위원회(KOBIS) Open API에서 수집한 영화·영화사 데이터를 SQLite에 구축하고, Flask 기반 웹 페이지에서 검색·조회·관리할 수 있도록 구현한 데이터베이스 프로젝트입니다.

영화 제목 검색뿐 아니라 장르, 감독, 제작 국가, 영화사, 개봉일, 관람등급을 조합한 상세 검색을 지원하며, KMDb API를 연동해 영화 포스터도 함께 제공합니다.

📌 주요 기능

1. 영화 제목 검색

한글 또는 영문 영화명 검색

영화 상세 정보와 포스터 조회

같은 제목의 영화가 여러 개일 경우 영화 코드별 선택 화면 제공

2. 상세 조건 검색

다음 조건을 조합해 영화를 검색할 수 있습니다.

장르

개봉일 범위

제작 국가

감독

영화사

관람등급

검색 결과는 개봉일 기준 내림차순으로 정렬되며, 페이지당 10개씩 표시됩니다.

3. 영화 및 영화사 정보 관리

영화 정보 등록·조회·수정·삭제

영화사 정보 등록·조회·수정·삭제

영화 코드 및 영화사 코드 중복 검사

영화 등록·수정 시 영화사 코드 존재 여부 검증

영화사 삭제 시 연결된 영화의 영화사 코드를 NULL로 변경

4. 영화 스크랩

관심 영화 스크랩

마이페이지에서 스크랩 목록 조회

스크랩 항목 삭제

브라우저 localStorage를 활용한 데이터 유지

5. 영화 데이터 수집 및 가공

KOBIS Open API의 XML 응답 파싱

페이지 단위 영화·영화사 데이터 수집

영화 코드 기반 상세 정보 추가 조회

Pandas를 활용한 CSV 변환

수집 데이터를 SQLite 데이터베이스로 구성

🗃️ 데이터베이스

저장소에 포함된 Movie_Info.db 기준 데이터 규모입니다.

테이블

설명

데이터 수

movie_Info

영화 기본 및 상세 정보

102,824건

CompanyCd

영화사 정보

13,353건

ERD

erDiagram
    COMPANY ||--o{ MOVIE : "CompanyCd"

    COMPANY {
        INTEGER CompanyCd PK
        TEXT company_name
        TEXT company_category
        TEXT ceo_name
    }

    MOVIE {
        TEXT movieCd PK
        TEXT movie_name
        TEXT movie_name_en
        INTEGER production_year
        NUM running_time
        INTEGER release_date
        TEXT production_status
        TEXT movie_type
        TEXT country
        TEXT genre
        TEXT director
        TEXT actors
        TEXT screening_type
        TEXT rating
        INTEGER CompanyCd FK
    }

movie_Info.CompanyCd는 CompanyCd.CompanyCd를 참조하며, 영화사가 삭제되면 해당 외래키는 NULL로 변경됩니다.

🔄 시스템 구성

flowchart LR
    A[KOBIS Open API] --> B[XML 파싱]
    B --> C[Pandas 데이터 가공]
    C --> D[CSV]
    D --> E[SQLite Database]
    E --> F[Flask Server]
    F --> G[Jinja2 Web UI]

    H[KMDb Open API] --> I[영화 포스터 조회]
    I --> F

🛠️ 기술 스택

구분

기술

Language

Python, HTML, CSS, JavaScript

Backend

Flask

Database

SQLite

Data Processing

Pandas

API

KOBIS Open API, KMDb Open API

Data Format

XML, JSON, CSV

Frontend

Jinja2 Template, Browser Local Storage

📂 프로젝트 구조

DB_Project/
├── project.py                  # Flask 웹 서버 및 검색·CRUD 로직
├── Movie_Info.db               # 영화·영화사 통합 데이터베이스
├── MakeCSV.py                  # KOBIS 영화 코드 및 영화명 수집
├── MakeCSV_Info.py             # 영화 코드 기반 상세 정보 수집
├── MakeCP.py                   # 영화사 정보 수집
├── CheckXML.py                 # KOBIS XML 응답 구조 확인
├── movieCd.csv                 # 영화 코드 데이터
├── movie_Info.csv              # 영화 상세 정보 데이터
├── CompanyCd.csv               # 영화사 정보 데이터
├── saveCSV/                    # 연도별 영화 코드 수집 결과
├── templates/
│   ├── home.html               # 메인 및 상세 검색 화면
│   ├── Search.html             # 단일 영화 검색 결과
│   ├── search_detail.html      # 동명 영화 선택 화면
│   ├── movie_detail.html       # 영화 상세 정보
│   ├── Advanced_Search.html    # 상세 검색 결과 및 페이지네이션
│   ├── CRUD.html               # 영화 정보 관리
│   ├── CRUD_company.html       # 영화사 정보 관리
│   └── my_page.html            # 스크랩 목록
└── static/
    ├── Icon.jpg
    └── MIcon.ico

🚀 실행 방법

1. 저장소 복제

git clone https://github.com/Wangjaepil/DB_Project.git
cd DB_Project

2. 가상환경 생성 및 활성화

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

3. 패키지 설치

웹 애플리케이션 실행:

pip install flask requests

데이터 수집 스크립트까지 실행하는 경우:

pip install pandas

4. API 키 설정

다음 파일에서 본인이 발급받은 API 키를 설정해야 합니다.

project.py: KMDb API 키

MakeCSV.py: KOBIS API 키

MakeCSV_Info.py: KOBIS API 키

MakeCP.py: KOBIS API 키

공개 저장소에서는 API 키를 코드에 직접 작성하지 않고 환경변수로 관리하는 것을 권장합니다.

5. 서버 실행

python project.py

브라우저에서 다음 주소로 접속합니다.

http://127.0.0.1:5000

Linux와 macOS는 파일명 대소문자를 구분하므로, project.py의 데이터베이스 경로를 실제 파일명인 Movie_Info.db로 통일해야 합니다.

🔍 핵심 구현 내용

조건 기반 동적 SQL 생성

사용자가 선택한 검색 조건만 SQL의 WHERE 절에 추가하고, 바인딩 파라미터를 사용해 장르·감독·영화사·개봉일·관람등급을 조합 검색하도록 구현했습니다.

JOIN을 활용한 통합 조회

영화 테이블과 영화사 테이블을 CompanyCd로 LEFT JOIN하여 영화 기본 정보와 제작·배급사 정보를 한 번에 조회합니다.

데이터 무결성 관리

movieCd와 CompanyCd를 기본키로 지정

영화 등록 시 참조할 영화사 코드의 존재 여부 확인

외래키에 ON DELETE SET NULL 정책 적용

SQL 파라미터 바인딩을 활용한 데이터 처리

대용량 검색 결과 페이지네이션

LIMIT과 OFFSET을 이용해 검색 결과를 페이지당 10개로 분할하고, 현재 페이지를 기준으로 페이지 번호를 구성했습니다.

외부 API 연동

KOBIS API: 영화 코드, 영화 상세 정보, 영화사 정보 수집

KMDb API: 영화명 또는 영화 코드를 기준으로 포스터 조회

💡 개선 방향

API 키 환경변수 분리 및 기존 노출 키 폐기

데이터베이스 접근 로직을 별도 모듈로 분리

영화명 부분 검색 및 자동완성 기능 추가

사용자 계정 기반 서버 측 스크랩 저장

반응형 UI 및 검색 결과 카드 디자인 개선

테스트 코드와 requirements.txt 추가

📄 데이터 출처

영화진흥위원회 KOBIS Open API

한국영상자료원 KMDb Open API
