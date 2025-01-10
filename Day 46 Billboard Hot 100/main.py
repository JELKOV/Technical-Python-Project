from bs4 import BeautifulSoup
import requests
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API 설정
CLIENT_ID = "https://developer.spotify.com/dashboard" # JELKOV 확인
CLIENT_SECRET = "https://developer.spotify.com/dashboard" # JELKOV 확인
REDIRECT_URI = "http://localhost:8000/callback"

# 빌보드 차트 날짜 입력 및 유효성 검사
while True:
    when_billboard = input("몇년 빌보드 차트를 찾고 싶나요 (YYYY-MM-DD)? ")
    try:
        datetime.strptime(when_billboard, "%Y-%m-%d")
        print(f"올바른 날짜입니다: {when_billboard}")
        break
    except ValueError:
        print("유효하지 않은 날짜 형식입니다. YYYY-MM-DD 형식으로 다시 입력해주세요.")

# 빌보드 차트 스크래핑
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}
response = requests.get(f"https://www.billboard.com/charts/hot-100/{when_billboard}/", headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 노래 제목 가져오기
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print("빌보드 핫 100 노래 제목:")
for idx, song in enumerate(song_names, 1):
    print(f"{idx}. {song}")

# Spotify 인증
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-private"
)
sp = spotipy.Spotify(auth_manager=sp_oauth)
print("Spotify 인증 완료!")

# Spotify에서 노래 검색 및 트랙 ID 가져오기
spotify_track_ids = []
for song in song_names:
    result = sp.search(q=song, type="track", limit=1)
    try:
        track_id = result["tracks"]["items"][0]["id"]
        spotify_track_ids.append(track_id)
        print(f"'{song}' 트랙 ID: {track_id}")
    except IndexError:
        print(f"'{song}' 트랙을 Spotify에서 찾을 수 없습니다.")

# Spotify 플레이리스트 생성
user_id = sp.current_user()["id"]
playlist_name = f"Billboard Hot 100 ({when_billboard})"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description="빌보드 핫 100 차트 노래")
print(f"플레이리스트 생성 완료: {playlist_name}")

# 플레이리스트에 트랙 추가
if spotify_track_ids:
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=spotify_track_ids)
    print("플레이리스트에 트랙 추가 완료!")
else:
    print("추가할 트랙이 없습니다.")
