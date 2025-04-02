from utils.generators import augment_sentence

if __name__ == "__main__":
    sentence = "안녕하세요"

    for _ in range(10):
        result = augment_sentence(sentence, prob=1)
        print(result)
