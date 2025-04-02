import random
import hgtk

from utils.hangul import choseong_adjacent, jungseong_adjacent

CHO = hgtk.letter.CHO
JOONG = hgtk.letter.JOONG


def insert_jamo(char):
    """문자 뒤에 자음 또는 모음만 추가하는 함수"""
    # 자음(초성)과 모음(중성) 중 하나 선택
    jamo_type = random.choice(['cho', 'jung'])

    if jamo_type == 'cho':
        # 자음 중 하나 선택
        cho_idx = random.choice(list(choseong_adjacent.keys()))
        if cho_idx < len(CHO):
            return char + CHO[cho_idx]
    else:
        # 모음 중 하나 선택
        jung_idx = random.choice(list(jungseong_adjacent.keys()))
        if jung_idx < len(JOONG):
            return char + JOONG[jung_idx]

    return char  # 변경 불가능한 경우


def generate_word_insert_typo(word, typo_count=1):
    """단어에서 최대 typo_count개의 위치에 자음 또는 모음 삽입"""
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
        result[pos] = insert_jamo(word[pos])

    return ''.join(result)


# 테스트
if __name__ == "__main__":
    sentence = "안녕하세요"

    # generate_word_insert_typo 함수 테스트
    print("\n단어 단위 자음/모음 삽입 테스트:")
    for _ in range(3):
        typo_result = generate_word_insert_typo(sentence, typo_count=1)
        print(f"오타 예시: {typo_result}")
