from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from cafe.models import Cafe


AREA_HINTS = (
    ('홍대', '홍대'),
    ('강남', '강남'),
    ('건대', '건대'),
    ('신촌', '신촌'),
    ('종로', '종로'),
    ('잠실', '잠실'),
    ('부평', '부평'),
    ('안양', '안양'),
    ('수원', '수원'),
    ('김포', '김포'),
    ('일산', '일산'),
    ('인천', '인천'),
)


def _extract_area_label(cafe):
    combined = f'{cafe.name} {cafe.address}'
    for keyword, label in AREA_HINTS:
        if keyword in combined:
            return label

    parts = (cafe.address or '').replace('(', ' ').replace(')', ' ').split()
    if len(parts) >= 2:
        candidate = parts[1].rstrip(',')
        if candidate in {'방탈출카페', '특별시', '광역시'} and len(parts) >= 3:
            candidate = parts[2].rstrip(',')
        return candidate

    return '기타'


def _estimate_rating(cafe, theme_total, genre_count, avg_difficulty):
    base_score = 3.75
    theme_signal = min(cafe.theme_count, 12) * 0.05
    detail_signal = min(theme_total, 6) * 0.04
    variety_signal = min(genre_count, 4) * 0.03
    difficulty_signal = 0

    if avg_difficulty is not None:
        difficulty_signal = max(0, 0.09 - abs(avg_difficulty - 3.1) * 0.04)

    return round(min(4.9, base_score + theme_signal + detail_signal + variety_signal + difficulty_signal), 1)


def _estimate_review_count(cafe, theme_total, genre_count):
    return max(12, cafe.theme_count * 9 + theme_total * 7 + genre_count * 5)


def _difficulty_label(avg_difficulty):
    if avg_difficulty is None:
        return '정보 없음'
    if avg_difficulty <= 2.5:
        return '입문'
    if avg_difficulty <= 3.7:
        return '보통'
    return '고난도'


def _serialize_cafe(cafe):
    themes = list(cafe.themes.all())
    genres = sorted({theme.genre for theme in themes if theme.genre})
    difficulties = [theme.difficulty for theme in themes if theme.difficulty]
    durations = [theme.duration_minutes for theme in themes if theme.duration_minutes]
    avg_difficulty = round(sum(difficulties) / len(difficulties), 1) if difficulties else None
    avg_duration = round(sum(durations) / len(durations)) if durations else None

    # 실제 테마 평점/리뷰 데이터가 있으면 사용, 없으면 추정값
    real_ratings = [theme.rating for theme in themes if theme.rating > 0]
    real_reviews = sum(theme.review_count for theme in themes)
    if real_ratings:
        rating = round(sum(real_ratings) / len(real_ratings), 1)
    else:
        rating = _estimate_rating(cafe, len(themes), len(genres), avg_difficulty)
    review_count = real_reviews if real_reviews else _estimate_review_count(cafe, len(themes), len(genres))

    # 지역: DB에 있으면 사용, 없으면 주소에서 추출
    region = cafe.region or _extract_area_label(cafe)

    reservation_url = next(
        (theme.reservation_url for theme in themes if theme.reservation_url),
        cafe.website,
    )

    return {
        'id': cafe.id,
        'name': cafe.name,
        'address': cafe.address,
        'phone': cafe.phone,
        'theme_count': cafe.theme_count,
        'website': cafe.website,
        'image_url': cafe.image_url,
        'latitude': cafe.latitude,
        'longitude': cafe.longitude,
        'operating_hours': cafe.operating_hours,
        'description': cafe.description,
        'detail_url': reverse('cafe:cafe_detail', args=[cafe.id]),
        'reservation_url': reservation_url,
        'region': region,
        'rating': rating,
        'review_count': review_count,
        'genres': genres,
        'theme_names': [theme.name for theme in themes],
        'theme_preview': [theme.name for theme in themes[:4]],
        'has_theme_data': bool(themes),
        'detail_theme_count': len(themes),
        'avg_difficulty': avg_difficulty,
        'difficulty_label': _difficulty_label(avg_difficulty),
        'avg_duration': avg_duration,
        'themes': [
            {
                'name': theme.name,
                'poster_url': theme.poster_url,
                'genre': theme.genre,
                'difficulty': theme.difficulty,
                'horror_level': theme.horror_level,
                'activity_level': theme.activity_level,
                'duration_minutes': theme.duration_minutes,
                'min_players': theme.min_players,
                'max_players': theme.max_players,
                'price': theme.price,
                'rating': theme.rating,
                'review_count': theme.review_count,
                'clear_rate': theme.clear_rate,
                'reservation_url': theme.reservation_url,
            }
            for theme in themes
        ],
    }


def _build_map_context(**overrides):
    cafes = Cafe.objects.prefetch_related('themes').all()
    cafe_payload = sorted(
        (_serialize_cafe(cafe) for cafe in cafes),
        key=lambda cafe: (-cafe['rating'], -cafe['review_count'], -cafe['theme_count'], cafe['name']),
    )

    context = {
        'kakao_maps_key': settings.KAKAO_MAPS_API_KEY,
        'cafe_payload': cafe_payload,
        'default_sort': 'recommended',
        'default_min_rating': '0',
        'page_heading': '방탈출 지도 탐색',
        'page_description': '카페 규모, 테마 성격, 난이도, 탐색 평점을 한 번에 비교하세요.',
    }
    context.update(overrides)
    return context


def map_search(request):
    return render(request, 'maps/map_search.html', _build_map_context())


def map_best(request):
    return render(
        request,
        'maps/map_best.html',
        _build_map_context(
            default_sort='rating',
            default_min_rating='4.2',
            page_heading='방탈출 베스트 큐레이션',
            page_description='탐색 평점과 테마 밀도가 높은 카페를 빠르게 추려보세요.',
        ),
    )
