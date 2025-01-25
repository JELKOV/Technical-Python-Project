from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Regexp, NumberRange
import requests
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# 데이터 베이스 URI 설정 (SQLite 사용)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
# SQLAlchemy 경고 제거
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# The Movie Database API 정보
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# CREATE DB
class Base(DeclarativeBase):
    pass

# SQLAlchemy 확장 생성 및 초기화
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movies(db.Model):
    # 기본키 필드
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # TMDB ID
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    # 영화 제목 필드
    title: Mapped[String] = mapped_column(String(250), nullable=False)
    # 출시일 필드
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    # 영화 설명 필드
    description: Mapped[String] = mapped_column(String(500), nullable=False)
    # 평점 필드
    rating: Mapped[Float] = mapped_column(Float, nullable=True)
    # 랭킹 필드
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    # 리뷰 필드
    review: Mapped[String] = mapped_column(String(500), nullable=False)
    # 이미지 필드
    img_url: Mapped[String] = mapped_column(String(500), nullable=False)

#### Flask 애플리케이션 컨텍스트에서 테이블 생성 ####
# 아래 코드는 Flask 애플리케이션 컨텍스트 내에서 데이터베이스 테이블을 생성하거나 삭제하는 용도로 사용됩니다.
# 프로젝트 초기 설정이나 데이터베이스 구조 변경 시 실행합니다.

# with app.app_context():
#
#     # 1. 기존 데이터베이스 스키마 삭제 (필요한 경우 실행)
#     db.drop_all()  # 데이터베이스의 모든 테이블을 삭제합니다.
#
#     # 2. 데이터베이스에 새로운 스키마 생성
#     db.create_all()  # 모델에 정의된 테이블 구조를 데이터베이스에 생성합니다.
#
#     #### 초기 데이터 추가 (선택적으로 실행) ####
#     # 아래는 예제 데이터를 데이터베이스에 추가하는 코드입니다.
#     new_movie = Movies(
#         title="Phone Booth",  # 영화 제목
#         year=2002,  # 개봉 연도
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,  # 평점
#         ranking=10,  # 순위
#         review="My favourite character was the caller.",  # 리뷰
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"  # 포스터 이미지 URL
#     )
#
#     # 3. 새 항목을 데이터베이스에 추가
#     db.session.add(new_movie)  # 영화 데이터를 데이터베이스 세션에 추가
#     db.session.commit()  # 변경사항을 데이터베이스에 저장


class RateMovieForm(FlaskForm):
    # 평점 필드: 0~10 범위의 숫자만 허용
    rating = FloatField(
        label='Your Rating Out of 10',
        validators=[
            DataRequired(message="Rating is required."),
            NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")  # 숫자 범위 검증
        ]
    )
    # 리뷰 필드
    review = StringField(
        label='Your Review',
        validators=[DataRequired(message="Review is required.")]
    )
    # 제출 버튼
    submit = SubmitField('Done')

class AddMovieForm(FlaskForm):
    # 제목 검색 입력
    title_search = StringField(label='Title', validators=[DataRequired()])
    # 제목 입력
    submit = SubmitField('Add Movie')

# 홈 페이지 라우트
@app.route("/")
def home():
    # 1. Movies 테이블에서 모든 영화 데이터를 평점 기준으로 내림차순 정렬하여 가져오기
    movies = Movies.query.order_by(Movies.rating.desc()).all()
    # 2. 정렬된 영화 데이터에 순위를 부여
    for index, movie in enumerate(movies, start=1):  # 순위는 1부터 시작
        movie.ranking = index
    # 3. 변경된 순위 데이터를 데이터베이스에 커밋 (저장)
    db.session.commit()
    # 4. 데이터를 `ranking` 기준으로 역순 정렬
    sorted_movies = sorted(movies, key=lambda x: x.ranking, reverse=True)  # `ranking` 기준 역순
    # 5. 정렬된 영화 데이터를 index.html로 전달
    return render_template("index.html", movies=sorted_movies)


# 영화 수정 페이지 라우트
@app.route("/edit", methods=["GET", "POST"])  # GET: 폼 표시, POST: 폼 제출 처리
def edit():
    # RateMovieForm 클래스의 인스턴스 생성 (수정 폼)
    edit_form = RateMovieForm()

    # 쿼리 매개변수 'id'에서 영화 ID 가져오기 (예: /edit?id=1)
    movie_id = request.args.get("id")

    # ID를 기반으로 Movies 테이블에서 해당 영화 레코드 가져오기
    movie = db.session.get(Movies, movie_id)

    # 폼이 제출되고 유효성 검사를 통과한 경우 (POST 요청)
    if edit_form.validate_on_submit():
        # 영화의 평점 데이터를 폼에서 입력받은 값으로 업데이트
        movie.rating = float(edit_form.rating.data)
        # 영화의 리뷰 데이터를 폼에서 입력받은 값으로 업데이트
        movie.review = edit_form.review.data
        # 변경사항을 데이터베이스에 커밋 (저장)
        db.session.commit()
        # 수정이 완료되면 홈 페이지로 리다이렉트
        return redirect(url_for('home'))

    # 폼과 영화 데이터를 edit.html 템플릿에 전달하여 렌더링
    return render_template("edit.html", movie=movie, form=edit_form)

# 영화 삭제 라우트
@app.route("/delete")
def delete():
    # 쿼리 매개변수 'id'에서 영화 ID 가져오기 (예: /edit?id=1)
    movie_id = request.args.get("id")
    # DB에서 책 조회 없으면 404 에러
    movie_db_search = db.get_or_404(Movies, movie_id)
    # DB에서 삭제
    db.session.delete(movie_db_search)
    # 변경사항 저장
    db.session.commit()
    return redirect(url_for('home'))

# 영화 추가 라우트
@app.route("/add", methods=["GET", "POST"])
def add():
    # 영화 추가 폼 생성
    add_form = AddMovieForm()

    # 폼 제출 처리
    if add_form.validate_on_submit():
        # 사용자가 입력한 영화 제목 가져오기
        movie_title = add_form.title_search.data

        # The Movie Database API에 요청하여 영화 검색
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,  # API 키 파라미터
            "query": movie_title,  # 검색 쿼리
            "include_adult": False,  # 성인 콘텐츠 제외
            "language": "en-US",  # 언어 설정
            "page": 1  # 페이지 설정
        }
        response = requests.get(url, params=params)

        # API 응답 데이터 가져오기
        if response.status_code == 200:  # 요청 성공 확인
            data = response.json().get("results", [])
            if not data:  # 검색 결과가 없는 경우
                # 검색 결과가 없음을 사용자에게 알림
                return render_template("select.html", movies=[], message="검색 결과가 없습니다. 다른 제목을 시도해 보세요.")
            else:
                # 검색된 영화 데이터를 select.html로 전달
                return render_template("select.html", movies=data)
        else:
            # API 호출 실패 시 에러 출력
            print(f"Error: {response.status_code}, {response.text}")
            return render_template("select.html", movies=[], message="API 요청 중 오류가 발생했습니다. 나중에 다시 시도해 주세요.")

    # 추가 페이지 렌더링
    return render_template("add.html", form=add_form)

# 영화 선택 처리 라우트
@app.route("/select", methods=["POST"])
def select_movie():
    # 선택된 영화 ID 가져오기
    movie_id = request.form.get("movie_id")

    if not movie_id:
        # 영화를 선택하지 않은 경우
        return render_template("select.html", movies=[], message="영화를 선택하지 않았습니다. 다시 선택해 주세요.")

    # The Movie Database API에서 선택된 영화의 상세 데이터 가져오기
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params={
        "api_key": TMDB_API_KEY
    })
    movie_data = response.json()

    # 상세 데이터에서 필요한 정보 추출
    tmdb_id = movie_data.get("id")  # TMDB에서 제공하는 고유 영화 ID
    title = movie_data.get("title")
    year = movie_data.get("release_date", "Unknown")[:4] if movie_data.get("release_date") else "Unknown"
    description = movie_data.get("overview", "No description available.")
    img_url = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}" if movie_data.get("poster_path") else ""

    # 중복 확인: TMDB의 영화 ID를 기준으로 데이터베이스에서 확인
    existing_movie = Movies.query.filter_by(tmdb_id=tmdb_id).first()
    if existing_movie:
        # 이미 존재하는 영화라면 메시지를 표시하고 홈으로 리다이렉트
        return redirect(url_for("home", message=f"'{title}'는 이미 데이터베이스에 존재합니다."))

    # 새로운 영화 항목 생성 및 데이터베이스에 저장
    new_movie = Movies(
        tmdb_id=tmdb_id,        # TMDB 영화 ID
        title=title,            # 영화 제목
        year=int(year) if year.isdigit() else None,  # 개봉 연도 (숫자로 변환)
        description=description,# 영화 설명
        img_url=img_url,        # 포스터 이미지 URL
        review="",              # 기본 리뷰 값
        rating=None,            # 기본 평점 값
        ranking=None            # 기본 순위 값
    )
    db.session.add(new_movie)
    db.session.commit()

    # 수정 페이지로 리다이렉트 (새로 추가된 영화 ID 사용)
    return redirect(url_for("edit", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
