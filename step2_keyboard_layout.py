import random
from utils.hangul import decompose_hangul, compose_hangul

# 두벌식 표준 키보드 기준 초성(자음) 인접키 매핑
# 키보드 배열: ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ / ㅁㄴㅇㄹㅎㅗㅓㅏㅣ / ㅋㅌㅊㅍㅠㅜㅡ
# 키보드 배열: qwertyuiop / asdfghjkl / zxcvbnm
choseong_adjacent = {
    # ㄱ(r): ㄷ, ㅅ, ㅇ, ㄹ, ㅎ
    0: [3, 9, 11, 5, 18],
    # ㄲ: ㄱ과 동일한 위치의 쌍자음
    1: [3, 9, 11, 5, 18],
    # ㄴ(s): ㅂ, ㅈ, ㄷ, ㅁ, ㅇ, ㅋ, ㅌ ,ㅊ
    2: [7, 12, 3, 6, 11, 15, 16, 14],
    # ㄷ(e): ㅈ, ㄱ, ㄴ, ㅇ, ㄹ
    3: [12, 0, 2, 11, 5],
    # ㄸ: ㄷ과 동일한 위치의 쌍자음
    4: [12, 0, 2, 11, 5],
    # ㄹ(f): ㄷ, ㄱ, ㅅ, ㅇ, ㅎ, ㅊ, ㅍ
    5: [3, 0, 9, 11, 18, 14, 17],
    # ㅁ(a): ㅂ, ㅈ, ㄴ, ㅋ, ㅌ
    6: [7, 12, 2, 15, 16],
    # ㅂ(q): ㅈ, ㅁ, ㄴ
    7: [12, 6, 2],
    # ㅃ: ㅂ과 동일한 위치의 쌍자음
    8: [12, 6, 2],
    # ㅅ(t): ㄱ, ㄹ, ㅎ
    9: [0, 5, 18],
    # ㅆ: ㅅ과 동일한 위치의 쌍자음
    10: [0, 5, 18],
    # ㅇ(d): ㅈ, ㄷ, ㄱ, ㄴ, ㄹ, ㅌ ,ㅊ ,ㅍ
    11: [12, 3, 0, 2, 5, 16, 14, 17],
    # ㅈ(w): ㅂ, ㄷ, ㅁ, ㄴ, ㅇ
    12: [7, 3, 6, 2, 11],
    # ㅉ: ㅈ과 동일한 위치의 쌍자음
    13: [7, 3, 6, 2, 11],
    # ㅊ(c): ㄴ, ㅇ, ㄹ, ㅌ, ㅍ
    14: [2, 11, 5, 16, 17],
    # ㅋ(z): ㅁ, ㄴ, ㅌ
    15: [6, 2, 16],
    # ㅌ(x): ㅁ, ㄴ, ㅇ, ㅋ, ㅊ
    16: [6, 2, 11, 15, 14],
    # ㅍ(v): ㅇ, ㄹ, ㅎ, ㅊ
    17: [11, 5, 18, 14],
    # ㅎ(g): ㄱ, ㅅ, ㄹ, ㅍ
    18: [0, 9, 5, 17]
}

# 두벌식 표준 키보드 기준 중성(모음) 인접키 매핑
# 키보드 배열: ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ / ㅁㄴㅇㄹㅎㅗㅓㅏㅣ / ㅋㅌㅊㅍㅠㅜㅡ
# 키보드 배열: qwertyuiop / asdfghjkl / zxcvbnm
jungseong_adjacent = {
    # ㅏ(k): ㅕ, ㅑ, ㅐ, ㅓ, ㅣ, ㅡ
    0: [4, 6, 1, 2, 8, 19],
    # ㅐ(o): ㅑ, ㅔ, ㅏ, ㅣ
    1: [6, 3, 0, 8],
    # ㅓ(j): ㅛ, ㅕ, ㅑ, ㅗ, ㅜ, ㅡ
    2: [12, 4, 6, 14, 15, 19],
    # ㅔ(p): ㅐ, ㅣ
    3: [1, 8],
    # ㅕ(y): ㅛ, ㅑ, ㅗ, ㅓ, ㅏ
    4: [12, 6, 14, 2, 0],
    # ㅖ: ㅐ, ㅣ
    5: [1, 8],
    # ㅑ(i): ㅕ, ㅐ, ㅓ, ㅏ, ㅣ
    6: [4, 1, 2, 0, 8],
    # ㅒ: ㅑ, ㅔ, ㅏ, ㅣ
    7: [6, 3, 0, 8],
    # ㅣ(l): ㅑ, ㅐ, ㅔ, ㅏ
    8: [6, 1, 3, 0],
    # ㅛ(u): ㅕ, ㅗ, ㅓ
    12: [4, 14, 2],
    # ㅗ(h): ㅛ, ㅕ, ㅓ, ㅠ, ㅜ
    14: [12, 4, 2, 20, 15],
    # ㅜ(n): ㅗ, ㅓ, ㅠ, ㅡ
    15: [14, 2, 20, 19],
    # ㅠ(b): ㅗ, ㅜ
    20: [14, 15],
    # ㅡ(m): ㅓ, ㅏ, ㅜ
    19: [2, 0, 15]
}


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


def generate_word_typo(word, typo_count=1):
    """단어에서 최대 typo_count개의 문자만 인접 키보드 위치 기반 오타로 변경"""
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
        # substitute 함수를 사용하여 인접 키 기반 오타 생성
        result[pos] = substitute(word[pos])

    return ''.join(result)


# 테스트
if __name__ == "__main__":
    print(f"초성 0(ㄱ)의 인접 키: {choseong_adjacent[0]}")
    print(f"중성 0(ㅏ)의 인접 키: {jungseong_adjacent[0]}")

    # 여러 단어에 대한 테스트
    test_words = ["프로그래밍", "키보드", "한글입력", "인공지능", "자연어처리"]
    print("\n다양한 단어에 대한 오타 생성:")
    for word in test_words:
        for i in range(2):
            with_typos = generate_word_typo(word, typo_count=1)
            print(f"{word} -> {with_typos}")
