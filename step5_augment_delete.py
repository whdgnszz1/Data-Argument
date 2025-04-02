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


def delete_jamo(jamos):
    """
    자모 리스트에서 랜덤하게 하나의 자모를 삭제

    Args:
        jamos (list): (자모 타입, 자모 문자) 튜플 리스트

    Returns:
        list: 삭제 후 남은 자모 리스트
    """
    if len(jamos) <= 1:
        return []  # 자모가 하나 이하면 삭제 후 빈 리스트 반환
    delete_position = random.randint(0, len(jamos) - 1)
    return [j for i, j in enumerate(jamos) if i != delete_position]


def recompose_jamos(jamos):
    """
    자모 리스트를 다시 한글 문자로 조합

    Args:
        jamos (list): (자모 타입, 자모 문자) 튜플 리스트

    Returns:
        str: 조합된 문자열 (문자와 독립 자모 혼합)
    """
    result = []
    i = 0
    while i < len(jamos):
        if (i + 1 < len(jamos) and
                jamos[i][0] == 'cho' and
                jamos[i + 1][0] == 'jung'):
            cho = jamos[i][1]
            jung = jamos[i + 1][1]
            if i + 2 < len(jamos) and jamos[i + 2][0] == 'jong':
                jong = jamos[i + 2][1]
                try:
                    combined = hgtk.letter.compose(cho, jung, jong)
                    result.append(combined)
                    i += 3
                except hgtk.exception.CompositionError:
                    result.append(cho)
                    i += 1
            else:
                try:
                    combined = hgtk.letter.compose(cho, jung, '')
                    result.append(combined)
                    i += 2
                except hgtk.exception.CompositionError:
                    result.append(cho)
                    i += 1
        else:
            result.append(jamos[i][1])
            i += 1
    return ''.join(result)


def generate_word_delete_typo(word):
    """
    단어에서 랜덤하게 하나의 자모를 삭제하여 오타 생성

    Args:
        word (str): 원본 단어

    Returns:
        str: 오타가 포함된 단어
    """
    jamos = decompose_sentence(word)
    if len(jamos) <= 1:
        return ''  # 자모가 하나 이하면 삭제 후 빈 문자열 반환
    jamos_deleted = delete_jamo(jamos)
    return recompose_jamos(jamos_deleted)


# 테스트
if __name__ == "__main__":
    sentence = "안녕하세요"
    print("\n단어 단위 자모 삭제 테스트")
    for _ in range(3):
        typo_result = generate_word_delete_typo(sentence)
        print(f"오타 예시: {typo_result}")
