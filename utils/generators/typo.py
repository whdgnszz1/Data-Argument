import random
import hgtk
from utils.hangul import choseong_adjacent, jungseong_adjacent

CHO = hgtk.letter.CHO
JOONG = hgtk.letter.JOONG


def generate_typo(char):
    """한글 문자에 오타를 생성하는 함수"""
    # 한글 범위 체크
    if 0xAC00 <= ord(char) <= 0xD7A3:
        # 한글 분리
        cho, jung, jong = hgtk.letter.decompose(char)

        # 랜덤으로 오타 유형 선택
        typo_type = random.choice(['cho', 'jung', 'jong'])

        if typo_type == 'cho':
            # 초성 변경: CHO 리스트에서 다음 초성으로 이동
            cho_idx = (hgtk.letter.CHO.index(cho) + 1) % len(hgtk.letter.CHO)
            cho = hgtk.letter.CHO[cho_idx]
        elif typo_type == 'jung':
            # 중성 변경: JOONG 리스트에서 다음 중성으로 이동
            jung_idx = (hgtk.letter.JOONG.index(jung) + 1) % len(hgtk.letter.JOONG)
            jung = hgtk.letter.JOONG[jung_idx]
        elif typo_type == 'jong':
            if jong:  # 종성이 있는 경우
                jong_idx = (hgtk.letter.JONG.index(jong) + 1) % len(hgtk.letter.JONG)
                jong = hgtk.letter.JONG[jong_idx]
            else:
                # 종성이 없는 경우, 랜덤 종성 추가 (빈 종성 제외)
                jong = random.choice(hgtk.letter.JONG[1:])

        # 변형된 한글 조합
        return hgtk.letter.compose(cho, jung, jong)
    return char


def generate_word_typo(word, typo_count=1):
    """단어에서 최대 typo_count개의 문자만 오타로 변경"""
    if not word:
        return word

    # 한글 문자의 위치 찾기
    hangul_indices = [i for i, char in enumerate(word) if 0xAC00 <= ord(char) <= 0xD7A3]

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
    cho, jung, jong = hgtk.letter.decompose(char)

    # 기본적으로 기존 자모 유지
    new_cho = cho
    new_jung = jung
    new_jong = jong

    # 초성, 중성, 종성 중 무작위로 하나 선택
    part_to_change = random.choice(['cho', 'jung', 'jong'])

    if part_to_change == 'cho':
        # 초성을 인접한 키로 변경
        cho_idx = CHO.index(cho)
        if cho_idx in choseong_adjacent:
            new_cho_idx = random.choice(choseong_adjacent[cho_idx])
            new_cho = CHO[new_cho_idx]

    elif part_to_change == 'jung':
        # 중성을 인접한 키로 변경
        jung_idx = JOONG.index(jung)
        if jung_idx in jungseong_adjacent:
            new_jung_idx = random.choice(jungseong_adjacent[jung_idx])
            new_jung = JOONG[new_jung_idx]

    elif part_to_change == 'jong':
        # 종성 추가/제거/변경
        if jong == '':  # 종성이 없는 경우, 랜덤 종성 추가
            new_jong = random.choice(hgtk.letter.JONG[1:])  # 빈 종성 제외
        else:
            # 종성이 있는 경우, 제거하거나 다른 종성으로 변경
            new_jong = random.choice([''] + [j for j in hgtk.letter.JONG if j != jong and j != ''])

    # 변형된 한글 조합
    try:
        return hgtk.letter.compose(new_cho, new_jung, new_jong)
    except hgtk.exception.CompositionError:
        return char  # 조합 불가능한 경우 원래 문자 반환
