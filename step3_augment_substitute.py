import random
import hgtk

from utils.hangul import choseong_adjacent, jungseong_adjacent

CHO = hgtk.letter.CHO
JOONG = hgtk.letter.JOONG


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


def generate_word_substitute_typo(word, typo_count=1):
    """단어에서 최대 typo_count개의 문자만 인접 키보드 위치 기반 오타로 변경"""
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
        result[pos] = substitute(word[pos])

    return ''.join(result)


# 테스트
if __name__ == "__main__":
    # 다양한 단어에 대한 오타 생성
    test_words = ["프로그래밍", "키보드", "한글입력", "인공지능", "자연어처리"]
    print("\n다양한 단어에 대한 오타 생성:")
    for word in test_words:
        for i in range(2):
            with_typos = generate_word_substitute_typo(word, typo_count=1)
            print(f"{word} -> {with_typos}")
