!!cleanimport requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

# MongoDB에 연결
link = os.getenv('LINK')
client_host = os.getenv('CLIENT')
client_port = int(os.getenv('PORT')) 
db_name = os.getenv('DATABASE')
client = MongoClient(client_host, client_port)
db = client[db_name]

# 웹브라우저의 User-Agent를 명시하고, 웹페이지 데이터를 서버에 요청해 메모리로 가져옴
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36' 
}
response = requests.get(link, headers=headers)

if response.status_code == 200:
    # HTML에 BeautifulSoup을 사용해 텍스트를 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 곡 제목과 가수 정보가 포함된 부모 요소 추출
    song_info = soup.select('div.wrap_song_info')

    # 데이터 저장 카운트 초기화 
    save_count = 0

    # 각 곡 정보 추출
    for info in song_info:
        # 곡 제목 추출 1번째 자식만.
        song_select = info.select_one('div.rank01 a:nth-child(1)')
        song = song_select.text.strip() if song_select else None

        # 가수 정보 추출
        singer_select = info.select('div.rank02 a')
        singers = ",".join(sorted(set([singer.text.strip() for singer in singer_select]))) if singer_select else None

        if song and singers:  

            doc = {
                'song': song,
                'singer': singers
            }

            # MongoDB에 데이터 저장
            db.songs.insert_one(doc)
            save_count += 1

    # 저장 완료 메시지 출력
    print(f'{save_count}개의 곡이 저장되었습니다.')

# 인터넷 오류 등의 이유로 요청 실패시 상태 코드 출력
else:
    print(f'요청 실패: {response.status_code}')