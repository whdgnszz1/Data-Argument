import random
import hgtk

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

# 테스트
if __name__ == "__main__":
    # 단일 문자 테스트
    char = "나"
    cho, jung, jong = hgtk.letter.decompose(char)
    print(f"분리: 초성={cho}, 중성={jung}, 종성={jong}")
    new_char = hgtk.letter.compose(cho, jung, jong)
    print(f"조합: {new_char}")

    # 단어 테스트
    original = "안녕하세요"
    with_typos = generate_word_typo(original, typo_count=1)
    print(f"원본: {original}")
    print(f"오타(1개): {with_typos}")

    # 여러 번 실행하여 다양한 결과 확인
    for _ in range(5):
        with_typos = generate_word_typo(original, typo_count=1)
        print(f"오타 예시: {with_typos}")