import random


def decompose_hangul(char):
    """한글 문자를 초성, 중성, 종성으로 분리"""
    if not (0xAC00 <= ord(char) <= 0xD7A3):
        return char
    code = ord(char) - 0xAC00
    jongseong = code % 28
    jungseong = ((code - jongseong) // 28) % 21
    choseong = ((code - jongseong) // 28) // 21
    return choseong, jungseong, jongseong


def compose_hangul(choseong, jungseong, jongseong):
    """초성, 중성, 종성을 조합하여 한글 문자 생성"""
    return chr(0xAC00 + (choseong * 21 + jungseong) * 28 + jongseong)


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


# 테스트
if __name__ == "__main__":
    char = "나"
    cho, jung, jong = decompose_hangul(char)
    print(f"분리: 초성={cho}, 중성={jung}, 종성={jong}")
    new_char = compose_hangul(cho, jung, jong)
    print(f"조합: {new_char}")

    original = "안녕하세요"
    with_typos = generate_word_typo(original, typo_count=1)
    print(f"원본: {original}")
    print(f"오타(1개): {with_typos}")

    # 여러 번 실행하여 다양한 결과 확인
    for _ in range(5):
        with_typos = generate_word_typo(original, typo_count=1)
        print(f"오타 예시: {with_typos}")