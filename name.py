import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 LINK 값 가져오기
link = os.getenv('LINK')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
response = requests.get(link, headers=headers)

if response.status_code == 200:
    # HTML에  BeautifulSoup을 사용해 텍스트를 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # select() 메서드로 범위 지정
    songs = soup.select('div.wrap_song_info div.rank01 a')

    # 1위부터 순서대로 페이지에 있는 모든 제목 출력
    for rank, name in enumerate(songs, start=1):
        title = name.text.strip()
        print(f"{rank}위: {title}")

# 인터넷 오류 등의 이유로 요청 실패시 상태 코드 출력
else:
    print(f'요청 실패: {response.status_code}')