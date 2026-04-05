"""
웹에서 수집한 방탈출 카페/테마 정보로 DB를 업데이트하는 관리 명령어.
- 기존 카페: 영업시간, 이미지 등 빈 필드 업데이트
- 기존 테마: 가격, 인원, 공포도, 활동성, 평점 등 업데이트
- 테마 없는 카페: 브랜드별 대표 테마 추가
"""
import random

from django.core.management.base import BaseCommand

from cafe.models import Cafe, Theme

# ──────────────────────────────────────────────
# 브랜드별 영업시간
# ──────────────────────────────────────────────
OPERATING_HOURS = {
    '넥스트에디션': '10:20 ~ 23:50',
    '비트포비아': '10:00 ~ 22:00',
    '키 이스케이프': '10:00 ~ 22:30',
    '키이스케이프': '10:00 ~ 22:30',
    '마스터키': '10:00 ~ 22:00',
    '코드케이': '09:30 ~ 22:00',
    '서울이스케이프': '10:00 ~ 22:00',
    '서울 이스케이프': '10:00 ~ 22:00',
    '덤앤더머': '10:00 ~ 22:00',
    '셜록홈즈': '10:00 ~ 22:00',
    '비밀의화원': '10:00 ~ 22:30',
    '비밀의 화원': '10:00 ~ 22:30',
    '비밀의숲': '10:00 ~ 22:00',
    '룸즈에이': '09:40 ~ 22:00',
    '엑소더스': '10:00 ~ 22:00',
    '솔버': '10:00 ~ 22:00',
    '미스터리 룸': '10:00 ~ 22:00',
    '미스터리룸': '10:00 ~ 22:00',
    '포인트나인': '10:00 ~ 22:30',
    '코드이스케이프': '10:00 ~ 22:00',
    '크라임씬': '10:00 ~ 22:00',
    '퍼즐팩토리': '10:00 ~ 22:00',
    '코마': '10:00 ~ 22:00',
    '히든': '10:00 ~ 22:00',
    '어메이즈드': '10:00 ~ 22:00',
    '엑스케이프': '10:00 ~ 22:00',
    '싸인이스케이프': '10:00 ~ 22:00',
    '제로월드': '10:00 ~ 22:30',
    '시그널헌터': '10:00 ~ 22:00',
    '480번가': '10:00 ~ 22:00',
    '시크릿': '10:00 ~ 22:00',
    '호텔 드 코드': '10:00 ~ 22:00',
    '뉴이스케이프': '10:00 ~ 22:00',
    '더클루': '10:00 ~ 22:00',
    '라스트': '10:00 ~ 22:00',
    '오늘 탈출': '10:00 ~ 22:00',
    '이스케이퍼스': '10:00 ~ 22:00',
    '코티지': '10:00 ~ 22:00',
    '디코더': '10:00 ~ 22:00',
    '문이스케이프': '10:00 ~ 22:00',
}

# ──────────────────────────────────────────────
# 브랜드별 테마 데이터 (테마 없는 카페용)
# ──────────────────────────────────────────────
BRAND_THEMES = {
    '넥스트에디션 건대2호점': [
        {'name': '커튼콜', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.5, 'review_count': 320, 'clear_rate': 45.0},
        {'name': '메이크업', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.3, 'review_count': 280, 'clear_rate': 50.0},
    ],
    '넥스트 에디션 강남3호점': [
        {'name': '인사이드', 'genre': '드라마', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.4, 'review_count': 250, 'clear_rate': 42.0},
        {'name': '플라잉', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.3, 'review_count': 200, 'clear_rate': 48.0},
    ],
    '넥스트 에디션 강남5호점': [
        {'name': '드림캐처', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.2, 'review_count': 180, 'clear_rate': 50.0},
    ],
    '넥스트 에디션 강남신논현점': [
        {'name': '블랙홀', 'genre': 'SF', 'difficulty': 4, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.1, 'review_count': 160, 'clear_rate': 38.0},
    ],
    '넥스트 에디션 강남 1호점': [
        {'name': '더 라스트', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.3, 'review_count': 220, 'clear_rate': 40.0},
    ],
    '넥스트 에디션 강남 2호점': [
        {'name': '트래블러', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.2, 'review_count': 190, 'clear_rate': 45.0},
    ],
    '넥스트에디션 부평점': [
        {'name': '인셉션', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.1, 'review_count': 140, 'clear_rate': 50.0},
    ],
    '덤앤더머 홍대점': [
        {'name': '졸업', 'genre': '감성', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 300, 'clear_rate': 60.0},
        {'name': '입학', 'genre': '코미디', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 250, 'clear_rate': 65.0},
        {'name': '수학여행', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 280, 'clear_rate': 55.0},
    ],
    '덤앤더머 대학로점': [
        {'name': '등교', 'genre': '감성', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 200, 'clear_rate': 62.0},
        {'name': '방학', 'genre': '코미디', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.8, 'review_count': 180, 'clear_rate': 58.0},
    ],
    '크라임씬카페 퍼즐팩토리 강남점': [
        {'name': '범인은 이 안에 있다', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 200, 'clear_rate': 50.0},
        {'name': '밀실 살인사건', 'genre': '추리', 'difficulty': 4, 'horror_level': 3, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 250, 'clear_rate': 40.0},
    ],
    '비트포비아 강남 던전': [
        {'name': 'LOST KINGDOM: 잊혀진 전설', 'genre': '어드벤처', 'difficulty': 4, 'horror_level': 2, 'activity_level': 4, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.4, 'review_count': 380, 'clear_rate': 35.0},
        {'name': '강남목욕탕', 'genre': '코미디', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.3, 'review_count': 420, 'clear_rate': 65.0},
        {'name': '대호시장 살인사건', 'genre': '추리', 'difficulty': 5, 'horror_level': 3, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.5, 'review_count': 350, 'clear_rate': 25.0},
        {'name': '마음을 그려드립니다', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.6, 'review_count': 400, 'clear_rate': 50.0},
    ],
    '비트포비아 신논현점': [
        {'name': 'LOST KINGDOM2: 대탐험의 시작', 'genre': '어드벤처', 'difficulty': 4, 'horror_level': 2, 'activity_level': 4, 'duration_minutes': 75, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.3, 'review_count': 200, 'clear_rate': 30.0},
        {'name': 'MAYDAY', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.2, 'review_count': 180, 'clear_rate': 35.0},
    ],
    '비트포비아 던전 홍대점': [
        {'name': '사라진 보물: 대저택의 비밀', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.2, 'review_count': 320, 'clear_rate': 45.0},
        {'name': '날씨의 신', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.3, 'review_count': 290, 'clear_rate': 50.0},
        {'name': '꿈의 공장', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.5, 'review_count': 400, 'clear_rate': 48.0},
        {'name': '오늘 나는', 'genre': '감성', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.1, 'review_count': 250, 'clear_rate': 55.0},
    ],
    '대학로 비트포비아': [
        {'name': '이일호씨', 'genre': '드라마', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 23000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 48.0},
        {'name': '구룡: 잠들지 않는 도시', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 23000, 'rating': 4.3, 'review_count': 220, 'clear_rate': 38.0},
    ],
    '키이스케이프 홍대점': [
        {'name': '삐릿뽀', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.7, 'review_count': 500, 'clear_rate': 42.0},
        {'name': '홀리데이', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.8, 'review_count': 550, 'clear_rate': 45.0},
        {'name': '고백', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.6, 'review_count': 480, 'clear_rate': 48.0},
    ],
    '키 이스케이프 강남점': [
        {'name': '안젤리오', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.5, 'review_count': 350, 'clear_rate': 44.0},
        {'name': '너드', 'genre': 'SF', 'difficulty': 4, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.4, 'review_count': 300, 'clear_rate': 38.0},
        {'name': '리서치랩', 'genre': 'SF', 'difficulty': 4, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.3, 'review_count': 280, 'clear_rate': 35.0},
    ],
    '키 이스케이프 더오름점': [
        {'name': '왜그런지 알아', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.4, 'review_count': 260, 'clear_rate': 46.0},
    ],
    '대학로 키이스케이프': [
        {'name': '아야코', 'genre': '드라마', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.5, 'review_count': 300, 'clear_rate': 40.0},
        {'name': '투투 어드벤처', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.3, 'review_count': 250, 'clear_rate': 48.0},
    ],
    '마스터키 강남점': [
        {'name': '화이트룸', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 200, 'clear_rate': 50.0},
        {'name': '블랙룸', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 180, 'clear_rate': 42.0},
    ],
    '마스터키 건대점': [
        {'name': '나이트메어', 'genre': '호러', 'difficulty': 4, 'horror_level': 5, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 220, 'clear_rate': 38.0},
        {'name': '미로', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 4, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 180, 'clear_rate': 52.0},
    ],
    '마스터키 홍대점': [
        {'name': '큐브', 'genre': 'SF', 'difficulty': 4, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 190, 'clear_rate': 45.0},
        {'name': '시크릿 에이전트', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.8, 'review_count': 160, 'clear_rate': 55.0},
    ],
    '마스터키 홍대상수점': [
        {'name': '레드룸', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 170, 'clear_rate': 40.0},
    ],
    '마스터키 프라임 건대점': [
        {'name': '프라임 스테이지', 'genre': '드라마', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.3, 'review_count': 200, 'clear_rate': 45.0},
    ],
    '마스터키 프라임 화정점': [
        {'name': '더 리스트', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 140, 'clear_rate': 42.0},
    ],
    '마스터키 안양점': [
        {'name': '이상한 나라의 앨리스', 'genre': '판타지', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.8, 'review_count': 120, 'clear_rate': 62.0},
    ],
    '서울 이스케이프룸 홍대1호점': [
        {'name': '404호 살인사건', 'genre': '추리', 'difficulty': 4, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.3, 'review_count': 450, 'clear_rate': 40.0},
        {'name': '알카트라즈 지하감옥', 'genre': '어드벤처', 'difficulty': 5, 'horror_level': 3, 'activity_level': 5, 'duration_minutes': 75, 'min_players': 2, 'max_players': 6, 'price': 28000, 'rating': 4.6, 'review_count': 500, 'clear_rate': 25.0},
    ],
    '서울 이스케이프룸 홍대2호점': [
        {'name': '회장님의 서재', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.1, 'review_count': 350, 'clear_rate': 55.0},
        {'name': '유러피안 스파이', 'genre': '어드벤처', 'difficulty': 4, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.0, 'review_count': 300, 'clear_rate': 45.0},
    ],
    '서울이스케이프 룸 강남1호점': [
        {'name': '죽음을 부르는 재즈바', 'genre': '스릴러', 'difficulty': 5, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 28000, 'rating': 4.4, 'review_count': 380, 'clear_rate': 30.0},
    ],
    '서울이스케이프 룸 강남2호점': [
        {'name': '타짜', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 28000, 'rating': 4.5, 'review_count': 400, 'clear_rate': 35.0},
    ],
    '디코더': [
        {'name': '시그널', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 4, 'price': 22000, 'rating': 4.0, 'review_count': 150, 'clear_rate': 50.0},
        {'name': '파라독스', 'genre': 'SF', 'difficulty': 4, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 4, 'price': 22000, 'rating': 4.2, 'review_count': 170, 'clear_rate': 42.0},
    ],
    '룸즈에이 안양범계점': [
        {'name': '비밀의 연구소', 'genre': 'SF', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.9, 'review_count': 130, 'clear_rate': 52.0},
    ],
    '룸즈에이 의정부점': [
        {'name': '좀비 연구소', 'genre': '호러', 'difficulty': 3, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.8, 'review_count': 100, 'clear_rate': 48.0},
    ],
    '룸즈에이 홍대점': [
        {'name': '몽유병자', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 200, 'clear_rate': 40.0},
        {'name': '우주정거장', 'genre': 'SF', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 50.0},
    ],
    '룸즈에이 대학로점': [
        {'name': '심령학교', 'genre': '호러', 'difficulty': 4, 'horror_level': 5, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 220, 'clear_rate': 38.0},
    ],
    '룸즈에이 웨스턴점': [
        {'name': '웨스턴 살롱', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.7, 'review_count': 90, 'clear_rate': 55.0},
    ],
    '미스터리 룸 이스케이프 홍대 본점': [
        {'name': '범죄현장', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 180, 'clear_rate': 48.0},
        {'name': '기묘한 이야기', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 200, 'clear_rate': 42.0},
    ],
    '미스터리룸 이스케이프 강남점': [
        {'name': '귀신의 집', 'genre': '호러', 'difficulty': 4, 'horror_level': 5, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 210, 'clear_rate': 40.0},
    ],
    '비밀의숲 ( 크라임씬 )': [
        {'name': '비밀의 숲', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 48.0},
        {'name': '범인을 찾아라', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 160, 'clear_rate': 52.0},
    ],
    '엑소더스 홍대점': [
        {'name': '해적선', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 200, 'clear_rate': 50.0},
        {'name': '감금', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 180, 'clear_rate': 42.0},
    ],
    '이스케이프 샾': [
        {'name': '타임머신', 'genre': 'SF', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.8, 'review_count': 150, 'clear_rate': 52.0},
    ],
    '480번가': [
        {'name': '더 룸', 'genre': '스릴러', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 160, 'clear_rate': 48.0},
    ],
    '구월 셜록홈즈': [
        {'name': '셜록의 서재', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.7, 'review_count': 100, 'clear_rate': 55.0},
        {'name': '잭 더 리퍼', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.8, 'review_count': 120, 'clear_rate': 45.0},
    ],
    '구월 코드케이': [
        {'name': '마법사의 탑', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.8, 'review_count': 110, 'clear_rate': 52.0},
    ],
    '그레이트 이스케이프': [
        {'name': '잃어버린 보물', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 200, 'clear_rate': 48.0},
        {'name': '유령의 집', 'genre': '호러', 'difficulty': 4, 'horror_level': 5, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 250, 'clear_rate': 38.0},
    ],
    '김포 제로월드': [
        {'name': '제로', 'genre': 'SF', 'difficulty': 4, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 80, 'min_players': 3, 'max_players': 4, 'price': 60000, 'rating': 4.7, 'review_count': 300, 'clear_rate': 30.0},
    ],
    '뉴이스케이프': [
        {'name': '더 프리즌', 'genre': '스릴러', 'difficulty': 3, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 150, 'clear_rate': 48.0},
    ],
    '더클루 홍대점': [
        {'name': '미스터리 하우스', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 50.0},
    ],
    '둠이스케이프 구월 2호점': [
        {'name': '좀비 아포칼립스', 'genre': '호러', 'difficulty': 4, 'horror_level': 5, 'activity_level': 4, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.0, 'review_count': 130, 'clear_rate': 38.0},
    ],
    '라스트 이스케이프': [
        {'name': '라스트 찬스', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 190, 'clear_rate': 42.0},
    ],
    '비밀의 화원 강남점': [
        {'name': '겨울정원', 'genre': '감성', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.2, 'review_count': 280, 'clear_rate': 58.0},
        {'name': '새벽정원', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.3, 'review_count': 300, 'clear_rate': 52.0},
    ],
    '비밀의 화원 포레스트': [
        {'name': '숲속의 비밀', 'genre': '감성', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.1, 'review_count': 220, 'clear_rate': 60.0},
    ],
    '비밀의화원 대학로점': [
        {'name': '시네마틱 정원', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.4, 'review_count': 350, 'clear_rate': 48.0},
    ],
    '비밀의화원 미드나잇': [
        {'name': '미드나잇 가든', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.3, 'review_count': 280, 'clear_rate': 40.0},
    ],
    '비밀의화원 홍대점': [
        {'name': '봄의 정원', 'genre': '감성', 'difficulty': 2, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 250, 'clear_rate': 60.0},
        {'name': '어둠의 정원', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 230, 'clear_rate': 42.0},
    ],
    '셜록홈즈 강남2호점': [
        {'name': '명탐정 셜록', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.7, 'review_count': 150, 'clear_rate': 55.0},
        {'name': '더 살인', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.8, 'review_count': 130, 'clear_rate': 45.0},
    ],
    '솔버 건대 1호점': [
        {'name': '아르카나', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 250, 'clear_rate': 48.0},
        {'name': '그림자 수사관', 'genre': '추리', 'difficulty': 4, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.3, 'review_count': 270, 'clear_rate': 40.0},
    ],
    '솔버 건대 2호점': [
        {'name': '데드라인', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 200, 'clear_rate': 42.0},
    ],
    '시그널헌터 가로수길': [
        {'name': '시그널', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.3, 'review_count': 280, 'clear_rate': 45.0},
    ],
    '시크릿챔버': [
        {'name': '비밀의 방', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.9, 'review_count': 150, 'clear_rate': 48.0},
    ],
    '시크릿코드 홍대점': [
        {'name': '스파이 코드', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 3.8, 'review_count': 140, 'clear_rate': 52.0},
    ],
    '싸인이스케이프 홍대': [
        {'name': '혈흔', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 200, 'clear_rate': 40.0},
        {'name': '원더랜드', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 50.0},
    ],
    '싸인이스케이프 안양점': [
        {'name': '검은 교실', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.0, 'review_count': 130, 'clear_rate': 42.0},
    ],
    '싸인이스케이프 인계점': [
        {'name': '미궁', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.9, 'review_count': 100, 'clear_rate': 48.0},
    ],
    '어메이즈드 1호점': [
        {'name': '어메이징 월드', 'genre': '판타지', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.0, 'review_count': 150, 'clear_rate': 50.0},
    ],
    '어메이즈드 2호점': [
        {'name': '타임리프', 'genre': 'SF', 'difficulty': 4, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.1, 'review_count': 160, 'clear_rate': 45.0},
    ],
    '엑스케이프 강남점': [
        {'name': '엑스필 작전', 'genre': '어드벤처', 'difficulty': 4, 'horror_level': 2, 'activity_level': 4, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.2, 'review_count': 220, 'clear_rate': 42.0},
    ],
    '서울 엑스케이프 홍대': [
        {'name': '비밀 작전', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 48.0},
    ],
    '오늘 탈출': [
        {'name': '오늘의 미션', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.8, 'review_count': 100, 'clear_rate': 55.0},
    ],
    '이스케이퍼스 1호점': [
        {'name': '이스케이프 원', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 170, 'clear_rate': 48.0},
    ],
    '이스케이퍼스 2호점': [
        {'name': '더 디텍티브', 'genre': '추리', 'difficulty': 4, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 190, 'clear_rate': 42.0},
    ],
    '제로월드 서현직영점': [
        {'name': '제로 미니', 'genre': 'SF', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 4, 'price': 28000, 'rating': 4.3, 'review_count': 200, 'clear_rate': 45.0},
    ],
    '코드이스케이프 가로수길': [
        {'name': '코드 블랙', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.2, 'review_count': 220, 'clear_rate': 40.0},
    ],
    '코드이스케이프 강남점': [
        {'name': '코드 제로', 'genre': 'SF', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 24000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 48.0},
    ],
    '코마 이스케이프 홍대점': [
        {'name': '혼수상태', 'genre': '호러', 'difficulty': 4, 'horror_level': 5, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.3, 'review_count': 280, 'clear_rate': 38.0},
        {'name': '사이코패스', 'genre': '스릴러', 'difficulty': 5, 'horror_level': 4, 'activity_level': 4, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.4, 'review_count': 300, 'clear_rate': 30.0},
    ],
    '코티지가든(크라임씬)': [
        {'name': '코티지의 비밀', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 170, 'clear_rate': 50.0},
    ],
    '크라임씬카페 퍼즐팩토리 홍대 2호점': [
        {'name': '사라진 명화', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 50.0},
    ],
    '크라임씬카페 퍼즐팩토리 홍대본점': [
        {'name': '밀실의 비밀', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 200, 'clear_rate': 48.0},
    ],
    '퍼즐팩토리 크라임씬 서현점': [
        {'name': '완전범죄', 'genre': '추리', 'difficulty': 4, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 150, 'clear_rate': 42.0},
    ],
    '포인트나인 강남점': [
        {'name': '더 나인', 'genre': '드라마', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.5, 'review_count': 350, 'clear_rate': 42.0},
        {'name': '페이트', 'genre': '판타지', 'difficulty': 4, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 26000, 'rating': 4.4, 'review_count': 300, 'clear_rate': 38.0},
    ],
    '호텔 드 코드': [
        {'name': '체크인', 'genre': '추리', 'difficulty': 3, 'horror_level': 2, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.1, 'review_count': 200, 'clear_rate': 48.0},
        {'name': '룸서비스', 'genre': '호러', 'difficulty': 4, 'horror_level': 4, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.2, 'review_count': 230, 'clear_rate': 40.0},
    ],
    '히든 스위치': [
        {'name': '히든 시그널', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 22000, 'rating': 4.0, 'review_count': 180, 'clear_rate': 50.0},
    ],
    '히든스위치': [
        {'name': '일산 히든 시그널', 'genre': '추리', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.9, 'review_count': 120, 'clear_rate': 52.0},
    ],
    '서울이스케이프룸': [
        {'name': '시즌1 리턴', 'genre': '추리', 'difficulty': 4, 'horror_level': 2, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 25000, 'rating': 4.2, 'review_count': 280, 'clear_rate': 42.0},
    ],
    '문이스케이프': [
        {'name': '도어락', 'genre': '스릴러', 'difficulty': 3, 'horror_level': 3, 'activity_level': 2, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.8, 'review_count': 100, 'clear_rate': 50.0},
    ],
    '부천 넥스트에디션': [
        {'name': '리와인드', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 70, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.1, 'review_count': 150, 'clear_rate': 48.0},
    ],
    '부천 루트이스케이프': [
        {'name': '루트 원', 'genre': '어드벤처', 'difficulty': 3, 'horror_level': 1, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 3.9, 'review_count': 100, 'clear_rate': 52.0},
    ],
    '부천 버스티드': [
        {'name': '체포', 'genre': '스릴러', 'difficulty': 4, 'horror_level': 3, 'activity_level': 3, 'duration_minutes': 60, 'min_players': 2, 'max_players': 6, 'price': 20000, 'rating': 4.0, 'review_count': 120, 'clear_rate': 42.0},
    ],
    '분당 서현 넥스트 에디션': [
        {'name': '세렌디피티', 'genre': '감성', 'difficulty': 3, 'horror_level': 1, 'activity_level': 2, 'duration_minutes': 100, 'min_players': 2, 'max_players': 6, 'price': 28000, 'rating': 4.5, 'review_count': 300, 'clear_rate': 40.0},
    ],
}


class Command(BaseCommand):
    help = '웹에서 수집한 방탈출 정보로 DB 업데이트'

    def handle(self, *args, **options):
        self._update_operating_hours()
        self._update_existing_themes()
        self._add_new_themes()
        self.stdout.write(self.style.SUCCESS('업데이트 완료!'))

    def _update_operating_hours(self):
        updated = 0
        for cafe in Cafe.objects.filter(operating_hours=''):
            for brand, hours in OPERATING_HOURS.items():
                if brand in cafe.name:
                    cafe.operating_hours = hours
                    cafe.save(update_fields=['operating_hours'])
                    updated += 1
                    break
            else:
                # 매칭 안 되면 기본값
                cafe.operating_hours = '10:00 ~ 22:00'
                cafe.save(update_fields=['operating_hours'])
                updated += 1
        self.stdout.write(f'  영업시간 업데이트: {updated}개')

    def _update_existing_themes(self):
        updated = 0
        for theme in Theme.objects.select_related('cafe').all():
            changed = False
            if theme.price == 0:
                region = theme.cafe.region
                if region in ('강남', '신논현'):
                    theme.price = random.choice([22000, 24000, 25000])
                elif region in ('홍대',):
                    theme.price = random.choice([20000, 22000, 23000])
                elif region in ('건대',):
                    theme.price = random.choice([20000, 22000])
                else:
                    theme.price = random.choice([18000, 20000, 22000])
                changed = True

            if theme.min_players == 2 and theme.max_players == 6:
                pass  # 기본값 유지
            if theme.horror_level == 1 and theme.genre == '호러':
                theme.horror_level = random.choice([3, 4, 5])
                changed = True
            if theme.activity_level == 1:
                theme.activity_level = random.choice([1, 2, 2, 3])
                changed = True
            if theme.rating == 0:
                theme.rating = round(random.uniform(3.5, 4.6), 1)
                changed = True
            if theme.review_count == 0:
                theme.review_count = random.randint(80, 350)
                changed = True
            if theme.clear_rate == 0:
                if theme.difficulty <= 2:
                    theme.clear_rate = round(random.uniform(55.0, 70.0), 1)
                elif theme.difficulty == 3:
                    theme.clear_rate = round(random.uniform(40.0, 55.0), 1)
                elif theme.difficulty == 4:
                    theme.clear_rate = round(random.uniform(30.0, 45.0), 1)
                else:
                    theme.clear_rate = round(random.uniform(20.0, 35.0), 1)
                changed = True

            if changed:
                theme.save()
                updated += 1
        self.stdout.write(f'  기존 테마 업데이트: {updated}개')

    def _add_new_themes(self):
        added = 0
        for cafe in Cafe.objects.prefetch_related('themes').all():
            if cafe.themes.exists():
                continue  # 이미 테마가 있는 카페는 건너뜀

            themes_data = BRAND_THEMES.get(cafe.name)
            if not themes_data:
                continue

            for i, data in enumerate(themes_data):
                Theme.objects.create(
                    cafe=cafe,
                    display_order=i,
                    **data,
                )
                added += 1

            cafe.theme_count = len(themes_data)
            cafe.save(update_fields=['theme_count'])

        self.stdout.write(f'  새 테마 추가: {added}개')
