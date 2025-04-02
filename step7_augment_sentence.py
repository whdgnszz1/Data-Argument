import random
import hgtk
from utils.generators import substitute, insert_jamo, delete_jamo, transpose_jamo, decompose_sentence, recompose_jamos

CHO = hgtk.letter.CHO
JOONG = hgtk.letter.JOONG


def augment_sentence(sentence, prob=0.1):
    """
    다양한 오타 생성 방법을 무작위로 선택하여 문장을 증강하는 함수

    Args:
        sentence (str): 원본 문장
        prob (float): 증강 확률

    Returns:
        str: 증강된 문장
    """
    # 문장을 단어 단위로 분리
    words = sentence.split()
    # 사용 가능한 증강 방법들
    methods = ['substitute', 'insert_jamo', 'delete_jamo', 'transpose_jamo']
    augmented_words = []

    for word in words:
        # 랜덤으로 증강 방법 하나 선택
        method = random.choice(methods)

        if method == 'substitute':
            # 각 문자에 대해 prob 확률로 substitute 적용
            augmented_word = ''.join(
                substitute(char) if random.random() < prob else char
                for char in word
            )
        elif method == 'insert_jamo':
            # 각 문자 뒤에 prob 확률로 자음/모음 추가
            augmented_word = ''
            for char in word:
                augmented_word += char
                if random.random() < prob:
                    augmented_word += insert_jamo(char)[-1]  # 마지막 문자(추가된 자모)만 사용
            augmented_word = augmented_word.rstrip()
        elif method == 'delete_jamo':
            # 단어를 자모 단위로 분해 후 삭제
            jamos = decompose_sentence(word)
            if random.random() < prob and jamos:
                jamos = delete_jamo(jamos)
            augmented_word = recompose_jamos(jamos)
        elif method == 'transpose_jamo':
            # prob 확률로 자모 교환
            augmented_word = transpose_jamo(word) if random.random() < prob else word

        augmented_words.append(augmented_word)

    # 증강된 단어들을 다시 문장으로 조합
    return ' '.join(augmented_words)


if __name__ == "__main__":
    sentence = "안녕하세요"
    result = augment_sentence(sentence, prob=0.3)
    print(f"원본: {sentence}, 증강: {result}")

    # 여러 번 실행하여 다양한 방법의 증강 결과 확인
    print("\n다양한 증강 방법 예시:")
    for _ in range(8):
        result = augment_sentence(sentence, prob=0.3)
        print(f"증강 예시: {result}")

    # 각 증강 방법별 결과 확인
    print("\n각 증강 방법별 결과:")
    methods = {
        "인접 키 대체 (substitute)": lambda s, p: ' '.join(
            ''.join(substitute(c) if random.random() < p else c for c in w) for w in s.split()),
        "자음/모음 삽입 (insert_jamo)": lambda s, p: ' '.join(
            ''.join(c + (insert_jamo(c)[-1] if random.random() < p else '') for c in w).rstrip() for w in s.split()),
        "자모 삭제 (delete_jamo)": lambda s, p: ' '.join(
            recompose_jamos(delete_jamo(decompose_sentence(w)) if random.random() < p else decompose_sentence(w)) for w
            in s.split()),
        "자모 위치 교환 (transpose_jamo)": lambda s, p: ' '.join(
            transpose_jamo(w) if random.random() < p else w for w in s.split())
    }

    for name, method in methods.items():
        for _ in range(2):
            result = method(sentence, 0.3)
            print(f"{name}: {result}")
