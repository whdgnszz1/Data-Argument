import random
from utils.hangul import decompose_hangul, compose_hangul, choseong_adjacent, jungseong_adjacent


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


def substitute(char):
    """키보드에서 인접한 키를 눌러 발생하는 오타 생성"""
    if not (0xAC00 <= ord(char) <= 0xD7A3):  # 한글인지 확인
        return char

    # 한글 분리
    cho, jung, jong = decompose_hangul(char)

    # 초성, 중성, 종성 중 무작위로 하나 선택
    part_to_change = random.choice(['cho', 'jung', 'jong'])

    if part_to_change == 'cho' and cho in choseong_adjacent and choseong_adjacent[cho]:
        # 초성을 인접한 키로 변경
        new_cho = random.choice(choseong_adjacent[cho])
        return compose_hangul(new_cho, jung, jong)

    elif part_to_change == 'jung' and jung in jungseong_adjacent and jungseong_adjacent[jung]:
        # 중성을 인접한 키로 변경
        new_jung = random.choice(jungseong_adjacent[jung])
        return compose_hangul(cho, new_jung, jong)

    elif part_to_change == 'jong':
        # 종성 추가/제거/변경
        if jong == 0:  # 종성이 없는 경우, 1-27 중에서 랜덤 추가
            new_jong = random.randint(1, 27)
        else:  # 종성이 있는 경우, 0(제거) 또는 다른 종성으로 변경
            new_jong = random.choice([0] + [j for j in range(1, 28) if j != jong])
        return compose_hangul(cho, jung, new_jong)

    return char  # 변경 불가능한 경우
