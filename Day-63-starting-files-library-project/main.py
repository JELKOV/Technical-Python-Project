from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
PyCharm 또는 IDE에서 빨간 밑줄이 표시된다면, 필요한 패키지를 설치하세요:

Windows:
python -m pip install -r requirements.txt

MacOS:
pip3 install -r requirements.txt

위 명령어는 프로젝트의 `requirements.txt` 파일에 있는 패키지를 설치합니다.
'''

# Flask 애플리케이션 초기화
app = Flask(__name__)

# SQLAlchemy 기반 클래스 생성
class Base(DeclarativeBase):
    pass

# 데이터베이스 URI 설정 (SQLite 사용)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"

# SQLAlchemy 확장 생성 및 초기화
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Book 테이블 모델 정의
class Book(db.Model):
    # 기본 키 필드 (id)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # 책 제목 필드 (문자열, 최대 길이 250, 고유값)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # 저자 필드 (문자열, 최대 길이 250)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    # 평점 필드 (실수형)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Flask 애플리케이션 컨텍스트에서 테이블 생성
with app.app_context():
    db.create_all()  # 데이터베이스에 테이블 스키마를 생성합니다.

# 기본 라우트: 책 목록 조회
@app.route('/')
def home():
    # 모든 책 데이터를 읽어옵니다. 제목 순서로 정렬
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # .scalars()를 사용해 행이 아닌 요소만 가져옵니다.
    all_books = result.scalars()
    # index.html 템플릿에 책 데이터를 전달합니다.
    return render_template("index.html", books=all_books)

# 새 책 추가 라우트
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # 폼 데이터를 통해 새 책 생성
        new_book = Book(
            title=request.form["title"],  # 사용자가 입력한 제목
            author=request.form["author"],  # 사용자가 입력한 저자
            rating=request.form["rating"]  # 사용자가 입력한 평점
        )
        db.session.add(new_book)  # 세션에 추가
        db.session.commit()  # 데이터베이스에 변경 사항 저장
        return redirect(url_for('home'))  # 홈 화면으로 리디렉션
    return render_template("add.html")  # GET 요청 시 추가 페이지 렌더링

# 책 평점 수정 라우트
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # 폼 데이터에서 책 ID 가져오기
        book_id = request.form["id"]
        # ID를 기반으로 책 조회 (없으면 404 에러)
        book_to_update = db.get_or_404(Book, book_id)
        # 평점 업데이트
        book_to_update.rating = request.form["rating"]
        db.session.commit()  # 변경 사항 저장
        return redirect(url_for('home'))  # 홈 화면으로 리디렉션
    # GET 요청 시 ID로 선택된 책 조회
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    # 선택된 책 데이터를 edit_rating.html에 전달
    return render_template("edit_rating.html", book=book_selected)

# 책 삭제 라우트
@app.route("/delete")
def delete():
    # URL 매개변수에서 책 ID 가져오기
    book_id = request.args.get('id')
    # ID로 책 조회 (없으면 404 에러)
    book_to_delete = db.get_or_404(Book, book_id)
    # 선택된 책 삭제
    db.session.delete(book_to_delete)
    db.session.commit()  # 변경 사항 저장
    return redirect(url_for('home'))  # 홈 화면으로 리디렉션

# 애플리케이션 실행
if __name__ == "__main__":
    app.run(debug=True)  # 디버그 모드로 실행 (오류 발생 시 디버깅 가능)
