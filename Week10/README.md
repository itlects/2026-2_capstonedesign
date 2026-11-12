# 10주차: MySQL 실행부터 웹 CRUD까지

## 구현 결과와 학습목표
브라우저에서 프로젝트 목록을 보고 새 프로젝트를 등록한 뒤, 이름·상태를 수정하고 삭제합니다. 새로고침 후에도 MySQL 데이터가 유지되는지 확인합니다.

- mysqld(서버), mysql(접속 클라이언트), Flask(웹 서버)의 역할을 설명한다.
- SQL의 SELECT/INSERT/UPDATE/DELETE를 웹 요청과 연결한다.
- HTML form → Flask → SQL → MySQL → HTML 응답 흐름을 설명한다.

## 개발환경
Windows 10/11, MySQL Community Server 8.0.46 ZIP, MySQL Workbench 8(선택), Python 3.11 이상(권장 3.12), VS Code, Chrome/Edge. CMD 기준 명령입니다. Java/Tomcat은 이 Flask 예제에서 사용하지 않습니다.

## 1. MySQL 서버 실행 (CMD A)
이미 초기화된 MySQL을 사용합니다. 아래 설치 경로가 다르면 실제 경로로 바꿉니다.

```bat
cd /d C:\Programs\devtools\db\MySQL\mysql-8.0.46-winx64\bin
mysqld --version
mysqld --console
```

`ready for connections`, 포트 `3306`을 확인하고 이 창은 열어 둡니다. 명령 입력 프롬프트가 돌아오지 않는 것은 서버가 실행 중이기 때문입니다. `mysqld --console`만으로 웹 페이지가 열리지는 않습니다.

설정 파일이 자동으로 읽히지 않는 설치는 첫 번째 옵션으로 파일을 지정합니다.

```bat
mysqld --defaults-file="C:\Programs\devtools\db\MySQL\mysql-8.0.46-winx64\my.ini" --console
```

서비스로 이미 실행 중이면 중복 실행하지 않습니다. `services.msc`에서 실행 여부를 확인합니다. 기존 데이터 폴더에 `--initialize`를 다시 실행하지 않습니다. 최초 ZIP 설치만 별도의 초기화가 필요하며, 처음 생성된 임시 root 암호를 안전하게 보관하고 로그인 후 변경합니다.

## 2. DB와 실습 계정 준비 (CMD B)
프로젝트를 `C:\capstone\Week10`에 압축 해제했다고 가정합니다.

```bat
cd /d C:\Programs\devtools\db\MySQL\mysql-8.0.46-winx64\bin
mysql -u root -p --default-character-set=utf8mb4
```

mysql 프롬프트에서 실행합니다. `create_user.sql`의 CHANGE_ME를 본인 암호로 먼저 변경합니다.

```sql
SOURCE C:/capstone/Week10/sql/schema.sql;
SOURCE C:/capstone/Week10/sql/create_user.sql;
USE capstone_week10;
SELECT * FROM projects;
SELECT VERSION();
```

예상 결과: 스마트 화분(계획), 교실 환경 모니터(진행) 2건. 샘플 SQL은 최초 1회 사용합니다. 이후 초기화 목적으로 재실행하지 않습니다.

## 3. 웹 실행 (CMD C)

```bat
cd /d C:\capstone\Week10
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
notepad .env
```

`.env`의 DB_PASSWORD를 실습 계정 암호와 일치시키고 SECRET_KEY를 임의의 긴 문자열로 바꾼 뒤 저장합니다. `.env`는 GitHub에 올리지 않습니다.

```bat
python app.py
```

브라우저 주소: http://127.0.0.1:5000

## 4. 예제와 설명 순서 (3시간 운영안)

| 시간 | 실습 | 확인 결과 |
|---|---|---|
| 0~25분 | 서버·클라이언트 구분, mysqld 실행 | ready for connections |
| 25~50분 | DB·테이블·계정 생성, SELECT | 한글 샘플 2건 |
| 50~75분 | Flask 설치, 목록 페이지 | MySQL 데이터가 웹에 표시 |
| 75~110분 | 등록·수정·삭제 | 데이터 변화가 SQL에서도 확인 |
| 110~140분 | 팀 프로젝트에 적용 | 필드 1개와 화면 설계 추가 |
| 140~150분 | 검증·결과 정리 | 캡처와 결과표 작성 |

### 예제 1: 조회
`app.py`의 `index()`를 읽습니다. `GET /` → `SELECT` → `fetchall()` → `render_template()` 순서입니다. `templates/index.html`의 반복문이 각 행을 화면으로 바꿉니다.

### 예제 2: 등록
화면에 `스마트 출석 시스템`, 상태 `계획`을 입력하고 등록합니다. `POST /projects`에서 `request.form`을 읽고 `%s`에 값을 별도로 전달합니다. 사용자 값을 SQL 문자열에 직접 이어 붙이지 않습니다. commit으로 저장한 후 redirect하여 새로고침에 의한 중복 등록을 줄입니다.

### 예제 3: 수정·삭제
해당 행의 상태를 `완료`로 바꾸고 저장합니다. `WHERE id=%s`가 선택한 행만 수정하게 합니다. 삭제 버튼을 누르고 확인한 뒤 해당 행이 사라지는지 확인합니다. 상태 변경은 POST, 양식 토큰 검사는 위조 요청을 줄이기 위한 장치입니다. 이 예제는 로그인 없는 로컬 수업용이며 공개 서비스에는 인증·권한 관리가 추가되어야 합니다.

## 5. 학생 워크북
1. MySQL 버전과 ready for connections 로그를 캡처한다.
2. 초기 목록 2건을 웹과 SQL에서 확인한다.
3. `스마트 출석 시스템`을 등록하고 새로고침한다.
4. 이름을 `스마트 출석 시스템 v2`, 상태를 `완료`로 바꾼다.
5. 해당 행만 삭제하고 초기 데이터 2건이 유지되는지 확인한다.
6. 제목을 공백만 입력하여 등록이 거부되는지 확인한다.
7. 웹 서버를 종료·재실행하고 DB가 유지되는지 확인한다.
8. 팀 프로젝트에서 필요한 필드 1개(예: 담당 팀)를 정하고 DB·서버·화면에서 변경할 부분을 표로 작성한다.

| 항목 | 기대 결과 | 실제 결과 | 증거 |
|---|---|---|---|
| 조회 | 한글 2건 | 직접 기록 | 화면/SQL |
| 등록 | 3건 | 직접 기록 | 화면/SQL |
| 수정 | 선택한 행만 변경 | 직접 기록 | 화면/SQL |
| 삭제 | 다시 2건 | 직접 기록 | 화면/SQL |
| 재실행 | 데이터 유지 | 직접 기록 | 화면 |

제출 연습 산출물: 화면 캡처, 결과표, 수정한 코드, README(실행법). 비밀번호·가상환경 폴더를 제외합니다. 포스터 제출은 별도 노션 안내를 따릅니다.

## 6. 종료와 오류 해결
웹 서버는 CMD C에서 Ctrl+C. MySQL은 별도 CMD에서 정상 종료합니다.

```bat
mysqladmin -u root -p shutdown
```

| 증상 | 확인 및 조치 |
|---|---|
| 3306 사용 중 / bind 오류 | 기존 서비스·mysqld 확인, 중복 서버 실행 방지 |
| data directory 오류 | my.ini의 basedir/datadir과 실제 경로 확인 |
| Access denied 1045 | 사용자·암호·계정 host 확인, root 접속과 앱 계정 구분 |
| Unknown database/table | schema.sql 실행 여부와 .env DB_NAME 확인 |
| Connection refused | mysqld 실행과 DB_PORT 확인 |
| ModuleNotFoundError | 가상환경 활성화 후 python -m pip install -r requirements.txt |
| 한글 깨짐 | SQL·HTML UTF-8 저장, utf8mb4 접속 확인 |
| CSRF 오류 | 페이지를 새로 열고 다시 제출, 실행 중 SECRET_KEY 변경 금지 |

## 복습문제
1. mysqld와 mysql의 차이는? → 서버와 접속 클라이언트.
2. mysqld 실행 후 웹이 바로 열리지 않는 이유는? → HTTP 요청을 처리하는 웹 서버가 별도로 필요하다.
3. commit의 목적은? → 변경 내용을 트랜잭션에 확정한다.
4. UPDATE에서 WHERE를 빠뜨리면? → 모든 행이 수정될 수 있다.
5. SQL에 입력값을 직접 이어 붙이면 생기는 문제는? → SQL 삽입과 문법 오류 위험.

## 공식 참고자료
- https://dev.mysql.com/doc/mysql-windows-excerpt/8.0/en/windows-start-command-line.html
- https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
- https://flask.palletsprojects.com/en/stable/installation/

## 검증 범위
Python 문법, Flask 템플릿 렌더링과 요청 흐름·입력 검증을 로컬에서 확인합니다. 이 실행 환경에는 MySQL 서버가 없으므로 Windows MySQL 8.0.46의 실제 DB 연동은 위 워크북 순서로 확인해야 합니다.
