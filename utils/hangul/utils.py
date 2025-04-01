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
