import random
from utils.hangul.utils import decompose_hangul, compose_hangul


def generate_typo(char):
    # 한글 분리
    if 0xAC00 <= ord(char) <= 0xD7A3:
        cho, jung, jong = decompose_hangul(char)

        # 랜덤으로 오타 유형 선택
        typo_type = random.choice(['cho', 'jung', 'jong'])

        if typo_type == 'cho' and cho < 18:  # 초성 변경
            cho = (cho + 1) % 19
        elif typo_type == 'jung' and jung < 20:  # 중성 변경
            jung = (jung + 1) % 21
        elif typo_type == 'jong':  # 종성 변경/제거
            jong = (jong + 1) % 28

        # 변형된 한글 조합
        return compose_hangul(cho, jung, jong)
    return char


def generate_word_typo(word, typo_count=1):
    """단어에서 최대 typo_count개의 문자만 오타로 변경"""
    if not word:
        return word

    # 한글 문자의 위치 찾기
    hangul_indices = []
    for i, char in enumerate(word):
        if 0xAC00 <= ord(char) <= 0xD7A3:
            hangul_indices.append(i)

    # 한글이 없으면 원본 반환
    if not hangul_indices:
        return word

    # 오타로 변경할 위치 선택 (최대 typo_count개)
    typo_positions = random.sample(hangul_indices, min(typo_count, len(hangul_indices)))

    # 결과 문자열 생성
    result = list(word)
    for pos in typo_positions:
        result[pos] = generate_typo(word[pos])

    return ''.join(result)
