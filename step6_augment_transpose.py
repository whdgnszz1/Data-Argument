import random
import hgtk


def decompose_sentence(sentence):
    """
    문장을 자모 단위로 분해하는 함수

    Args:
        sentence (str): 입력 문장

    Returns:
        list: (자모 타입, 자모 문자) 튜플의 리스트
    """
    jamos = []
    for char in sentence:
        if hgtk.checker.is_hangul(char):
            cho, jung, jong = hgtk.letter.decompose(char)
            jamos.append(('cho', cho))
            jamos.append(('jung', jung))
            if jong != '':  # 종성이 있는 경우
                jamos.append(('jong', jong))
        else:
            jamos.append(('char', char))  # 한글 외 문자는 그대로 추가
    return jamos


def recompose_jamos(jamos):
    """
    자모 리스트를 다시 한글 문자로 조합

    Args:
        jamos (list): (자모 타입, 자모 문자) 튜플 리스트

    Returns:
        str: 조합된 문자열
    """
    result = []
    i = 0

    while i < len(jamos):
        # 초성+중성+종성 또는 초성+중성 조합 시도
        if i + 1 < len(jamos) and jamos[i][0] == 'cho' and jamos[i + 1][0] == 'jung':
            cho = jamos[i][1]
            jung = jamos[i + 1][1]
            jong = ''

            # 종성이 있는지 확인
            if i + 2 < len(jamos) and jamos[i + 2][0] == 'jong':
                jong = jamos[i + 2][1]
                i += 3
            else:
                i += 2

            # 한글 조합 시도
            try:
                combined = hgtk.letter.compose(cho, jung, jong)
                result.append(combined)
            except Exception:
                # 조합 실패 시 개별 자모 추가 대신 채움 문자 사용
                if cho in hgtk.const.CHOSUNG:
                    # 초성 채움 문자 사용 (ㅇ + 해당 초성)
                    try:
                        result.append(hgtk.letter.compose(cho, 'ㅏ', ''))
                    except:
                        result.append(cho)  # 실패하면 그대로 추가
                else:
                    result.append(cho)

                if jung in hgtk.const.JUNGSUNG:
                    # 중성은 'ㅇ'과 결합
                    try:
                        result.append(hgtk.letter.compose('ㅇ', jung, ''))
                    except:
                        result.append(jung)  # 실패하면 그대로 추가
                else:
                    result.append(jung)

                if jong:
                    if jong in hgtk.const.JONGSUNG:
                        try:
                            # 종성은 'ㅇ'+'ㅏ'+종성으로 결합
                            result.append(hgtk.letter.compose('ㅇ', 'ㅏ', jong))
                        except:
                            result.append(jong)  # 실패하면 그대로 추가
                    else:
                        result.append(jong)
        else:
            # 일반 문자나 단일 자모는 그대로 추가
            result.append(jamos[i][1])
            i += 1

    return ''.join(result)


def transpose_jamo(word):
    """
    단어의 자모를 분해하고, 인접한 자모를 교환한 뒤 다시 합치는 함수

    Args:
        word (str): 원본 단어

    Returns:
        str: 자모 교환 후 재구성된 단어
    """
    jamo_sequence = decompose_sentence(word)
    if len(jamo_sequence) < 2:
        return word

    # 자모 교환
    i = random.randint(0, len(jamo_sequence) - 2)
    jamo_sequence[i], jamo_sequence[i + 1] = jamo_sequence[i + 1], jamo_sequence[i]

    # 자모 재구성
    return recompose_jamos(jamo_sequence)


def generate_word_transpose_typo(word, typo_count=1):
    """
    단어에서 최대 typo_count번의 자모 위치 교환

    Args:
        word (str): 원본 단어
        typo_count (int): 교환 횟수

    Returns:
        str: 오타가 포함된 단어
    """
    result = word
    for _ in range(typo_count):
        result = transpose_jamo(result)
    return result


# 테스트 코드
if __name__ == "__main__":
    test_words = ["안녕하세요", "만남을", "학교에", "반갑습니다"]

    print("자모 위치 교환 테스트:")
    for word in test_words:
        for i in range(3):
            typo_result = generate_word_transpose_typo(word, typo_count=1)
            print(f"{word} -> {typo_result}")
