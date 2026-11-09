"""Реализация векторизаторов текста и извлечения ключевых слов."""
from math import log
from typing import Self, TypedDict


class VectorizerParams(TypedDict):
    """Описывает параметры векторизатора и их типы."""
    lowercase: bool
    ngram_size: int
    vocabulary: dict[str, int]


class CountVectorizer:
    """Преобразует тексты в матрицу количества вхождений слов."""

    def __init__(self, lowercase: bool = True,
                 ngram_size: int = 1,
                 vocabulary: dict[str, int] | None = None) -> None:
        if not isinstance(lowercase, bool):
            raise ValueError('lowercase должен быть булевым')
        if (
            not isinstance(ngram_size, int) or
            isinstance(ngram_size, bool) or
            ngram_size < 1
        ):
            raise ValueError('ngram_size '
                             'должен быть положительным целым числом')
        self.next_index: int
        self.next_index = 0
        self.vocabulary_: dict[str, int]
        if vocabulary is None:
            self.vocabulary_ = {}
        else:
            self.vocabulary = vocabulary
        self.lowercase: bool
        self.lowercase = lowercase
        self.ngram_size: int
        self.ngram_size = ngram_size

    def add_word(self, word: str) -> int:
        """Возвращает индекс слова и
        добавляет слово в словарь self.vocabulary_, если его там нет"""
        if not isinstance(word, str):
            raise ValueError('word должен быть строкой')
        if self.lowercase:
            word = word.lower()
        if word not in self.vocabulary_:
            self.vocabulary_[word] = self.next_index
            self.next_index += 1
            return self.next_index - 1
        return self.vocabulary_[word]

    def tokenize(self, text: str) -> list[str]:
        """Токенизирует текст, т.е. разбивает его
        на слова или n-граммы в зависимости от значения ngram_size."""
        if not isinstance(text, str):
            raise ValueError('text должен быть строкой')
        if self.lowercase:
            text = text.lower()
        tokens: list[str]
        tokens = text.split()
        if self.ngram_size > 1:
            ngrams: list[str]
            ngrams = []
            for position in range(0, len(tokens) - self.ngram_size + 1):
                ngrams.append(
                    ' '.join(tokens[position:position + self.ngram_size])
                )
            tokens = ngrams
        return tokens

    @staticmethod
    def test_corpus(corpus: list[str]) -> None:
        """Проверяет, что корпус является списком строк."""
        if (
            not isinstance(corpus, list) or
            not all(isinstance(text, str) for text in corpus)
        ):
            raise ValueError('corpus должен быть списком, состоящим из строк')

    def fit(self, corpus: list[str]) -> Self:
        """Обучает векторизатор на корпусе текстов и формирует словарь слов."""
        self.test_corpus(corpus)
        all_tokens: list[str] = []

        for text in corpus:
            all_tokens.extend(self.tokenize(text))
        if not all_tokens:
            raise ValueError('Обучение не удалось, '
                             'не создалось ни одного токена')
        self.vocabulary = {}
        for token in all_tokens:
            self.add_word(token)
        return self

    @staticmethod
    def test_len_vocabulary(vocabulary: dict[str, int]) -> None:
        """Проверяет, что словарь не пустой, т.е. векторизатор обучен."""
        if not vocabulary:
            raise RuntimeError('Сначала нужно обучить')

    def transform(self,
                  corpus: list[str]) -> list[list[float]] | list[list[int]]:
        """Преобразует корпус текстов в матрицу частот слов,
        т.е. подсчитывает количество вхождений каждого слова в текст."""
        self.test_corpus(corpus)
        self.test_len_vocabulary(self.vocabulary_)
        if not corpus:
            return []
        count_matrix: list[list[float]]
        count_matrix = []
        for text in corpus:
            counts: list[float]
            counts = []
            tokens: list[str]
            tokens = self.tokenize(text)
            for word in self.vocabulary_:
                counts.append(tokens.count(word))
            count_matrix.append(counts)
        return count_matrix

    def get_feature_names(self) -> list[str]:
        """Возвращает список слов из словаря векторизатора."""
        return list(self.vocabulary_.keys())

    def fit_transform(
            self,
            corpus: list[str]
            ) -> list[list[int]] | list[list[float]]:
        """Обучает векторизатор на корпусе текстов
        и возвращает матрицу частот слов."""
        self.fit(corpus)
        return self.transform(corpus)

    @property
    def vocabulary(self) -> dict[str, int]:
        """Возвращает словарь слов и их индексов."""
        return self.vocabulary_

    @vocabulary.setter
    def vocabulary(self,
                   vocabulary: dict[str, int]) -> None:
        """Проверяет переданный словарь и обновляет его,
        если ключи и индексы соответствуют условиям."""
        if (
            isinstance(vocabulary, dict) and
            all(isinstance(word, str) for word in vocabulary) and
            all(
                isinstance(index, int) and not isinstance(index, bool)
                for index in vocabulary.values()
            )
        ):
            vocabulary = dict(sorted(vocabulary.items(),
                                     key=lambda item: item[1]))
            if list(vocabulary.values()) == list(range(len(vocabulary))):
                self.next_index = len(vocabulary)
                self.vocabulary_ = vocabulary
            else:
                raise ValueError('Индексы должны идти по порядку')
        else:
            raise ValueError('Нужно ввести словарь, где ключи - строки, '
                             'а значения - неотрицательные числа')

    @vocabulary.deleter
    def vocabulary(self) -> None:
        """Очищает словарь векторизатора и сбрасывает счётчик индексов."""
        self.vocabulary_ = {}
        self.next_index = 0

    def to_dict(self) -> VectorizerParams:
        """Возвращает словарь с настройками векторизатора
        и копией словаря слов и их индексов."""
        param_dict: VectorizerParams
        param_dict = {'lowercase': self.lowercase,
                      'ngram_size': self.ngram_size,
                      'vocabulary': self.vocabulary_.copy()}
        return param_dict

    @classmethod
    def from_dict(cls, param_dict: VectorizerParams) -> Self:
        """Проверяет переданные параметры и создаёт
        новый векторизатор с этими настройками."""
        expected_keys: set[str]
        expected_keys = {'lowercase',
                         'ngram_size',
                         'vocabulary'}
        if not isinstance(param_dict, dict):
            raise ValueError('Нужно передать словарь')
        actual_keys: set[str]
        actual_keys = set(list(param_dict.keys()))
        if actual_keys != expected_keys:
            raise ValueError('Переданы не те параметры, '
                             'можно передать только '
                             'lowercase, ngram_size, vocabulary')
        return cls(**param_dict)


class BinaryVectorizer(CountVectorizer):
    """Преобразует тексты в матрицу наличия слов,
    где 1 - слово присутствует, 0 - отсутствует."""

    def transform(self, corpus: list[str]) -> list[list[int]]:
        """Преобразует корпус текстов в бинарную матрицу,
        т.е. отмечает наличие каждого слова значением 1 или 0."""
        self.test_corpus(corpus)
        self.test_len_vocabulary(self.vocabulary_)
        if not corpus:
            return []
        binary_matrix: list[list[int]]
        binary_matrix = []
        for text in corpus:
            tokens = set(self.tokenize(text))
            binary_row: list[int]
            binary_row = []
            for word in self.vocabulary_:
                binary_row.append(1 if word in tokens else 0)
            binary_matrix.append(binary_row)
        return binary_matrix


class TfidfVectorizer(CountVectorizer):
    """Преобразует тексты в матрицу весов TF-IDF."""

    def __init__(self, lowercase: bool = True,
                 ngram_size: int = 1,
                 vocabulary: dict[str, int] | None = None,
                 use_idf: bool = True
                 ) -> None:
        super().__init__(lowercase, ngram_size, vocabulary)
        if not isinstance(use_idf, bool):
            raise ValueError('use_idf должен быть булевым')
        self.use_idf: bool
        self.use_idf = use_idf
        self._idf: list[float]
        self._idf = []

    def fit(self, corpus: list[str]) -> Self:
        """Обучает векторизатор на корпусе текстов
        и рассчитывает веса IDF, если выбрано use_idf=True."""
        super().fit(corpus)
        if self.use_idf:
            document_count: int
            document_count = len(corpus)
            document_frequencies: list[int]
            document_frequencies = [0] * len(self.vocabulary_)
            for text in corpus:
                unique_tokens: set[str]
                unique_tokens = set(self.tokenize(text))
                for word in unique_tokens:
                    if word in self.vocabulary_:
                        document_frequencies[self.vocabulary_[word]] += 1
            idf_weights: list[float]
            idf_weights = []
            for frequency in document_frequencies:
                idf_weights.append(
                    log((document_count + 1) / (frequency + 1)) + 1
                )
            self._idf = idf_weights
        else:
            self._idf = []
        return self

    def transform(self, corpus: list[str]) -> list[list[float]]:
        """Преобразует корпус текстов в матрицу весов TF-IDF
        или TF, если выбрано use_idf=False."""
        super().test_corpus(corpus)
        super().test_len_vocabulary(self.vocabulary_)
        if not corpus:
            return []
        weight_matrix: list[list[float]]
        weight_matrix = []
        for text in corpus:
            weights: list[float]
            weights = []
            tokens: list[str]
            tokens = self.tokenize(text)
            known_tokens: list[str]
            known_tokens = list(filter(lambda word: word in self.vocabulary_,
                                       tokens))
            for word in self.vocabulary_:
                tf: float
                if known_tokens:
                    tf = known_tokens.count(word) / len(known_tokens)
                else:
                    tf = 0
                if self.use_idf:
                    weights.append(tf * self._idf[self.vocabulary_[word]])
                else:
                    weights.append(tf)
            weight_matrix.append(weights)
        return weight_matrix

    @property
    def idf(self) -> list[float]:
        """Возвращает копию списка весов IDF."""
        return self._idf.copy()

    @classmethod
    def from_config(cls, config: dict[str, bool]) -> Self:
        """Проверяет переданные настройки и создаёт
        новый векторизатор с параметрами lowercase и use_idf."""
        allowed_keys: set[str]
        allowed_keys = {'lowercase',
                        'use_idf'}
        if not isinstance(config, dict):
            raise ValueError('Нужно передать словарь')
        if not set(config.keys()).issubset(allowed_keys):
            raise ValueError('Переданы неизвестные параметры, '
                             'можно передать только '
                             'lowercase, use_idf')
        return cls(lowercase=config.get('lowercase', True),
                   use_idf=config.get('use_idf', True)
                   )


class KeywordExtractor:
    """Извлекает из текстов ключевые слова на основе их весов."""

    def __init__(self, vectorizer: CountVectorizer, top_n: int = 3) -> None:
        self.vectorizer: CountVectorizer
        self.vectorizer = vectorizer
        self.top_n: int
        self.top_n = top_n

    def fit(self, corpus: list[str]) -> Self:
        """Обучает переданный векторизатор на корпусе текстов,
        т.е. вызывает метод fit у переданного векторизатора."""
        self.vectorizer.fit(corpus)
        return self

    def extract(self,
                corpus: list[str]) -> list[list[tuple[str, int | float]]]:
        """Извлекает из каждого текста до top_n ключевых слов
        с положительными весами и сортирует их по весу и алфавиту."""
        keywords_by_text: list[list[tuple[str, int | float]]]
        keywords_by_text = []
        weight_matrix: list[list[int]] | list[list[float]]
        weight_matrix = self.vectorizer.transform(corpus)
        for row_index in range(len(corpus)):
            weighted_words: list[tuple[str, int | float]]
            weighted_words = []
            feature_names: list[str]
            feature_names = self.vectorizer.get_feature_names()
            for column_index, word in enumerate(feature_names):
                weight: int | float
                weight = weight_matrix[row_index][column_index]
                if weight > 0:
                    weighted_words.append((word, weight))
            sorted_words: list[tuple[str, int | float]]
            sorted_words = sorted(weighted_words,
                                  key=lambda item: (-item[1], item[0]))
            keywords_by_text.append(sorted_words[:self._top_n])
        return keywords_by_text

    @property
    def top_n(self) -> int:
        """Возвращает текущее значение top_n."""
        return self._top_n

    @top_n.setter
    def top_n(self, top_n: int) -> None:
        """Проверяет переданное значение top_n и обновляет его,
        если это положительное целое число."""
        if (
            not isinstance(top_n, int)
            or isinstance(top_n, bool)
            or top_n <= 0
        ):
            raise ValueError('top_n должен быть положительным числом')
        self._top_n = top_n


def demo() -> None:
    """Демонстрирует работу векторизаторов и извлечения ключевых слов
    на трёх сценариях проверки."""
    # Обучающие сообщения
    TRAIN_CORPUS: list[str]
    TRAIN_CORPUS = ["Марс сигнал сигнал",
                    "Марс пыль",
                    "Марс сигнал антенна"
                    ]

    # Сообщения для проверки
    CHECK_CORPUS: list[str]
    CHECK_CORPUS = ["СИГНАЛ шум сигнал",
                    "антенна пыль",
                    "марс марс марс",
                    "комета",
                    ""
                    ]

    # Сценарий 1 - TF-IDF
    tfidf: TfidfVectorizer
    tfidf = TfidfVectorizer.from_config({})
    tfidf_matrix: list[list[int]] | list[list[float]]
    tfidf_matrix = tfidf.fit_transform(TRAIN_CORPUS)
    check_matrix: list[list[float]]
    check_matrix = tfidf.transform(CHECK_CORPUS)
    print(f'Слова: {tfidf.get_feature_names()}')
    print(f'idf: {tfidf.idf}')
    print('Матрица tfidf для TRAIN_CORPUS:', *tfidf_matrix, sep='\n')
    print('Матрица tfidf для CHECK_CORPUS:', *check_matrix, sep='\n')
    idf_copy: list[float]
    idf_copy = tfidf.idf
    idf_copy.clear()
    print(f'idf после очистки: {tfidf.idf}')

    # Сценарий 2 - настройки и повторное обучение
    tf_vectorizer: TfidfVectorizer
    tf_vectorizer = TfidfVectorizer.from_config({'lowercase': False,
                                                 'use_idf': False})
    corpus: list[str]
    corpus = ['Марс марс', 'МАРС сигнал']
    tf_matrix: list[list[int]] | list[list[float]]
    tf_matrix = tf_vectorizer.fit_transform(corpus)
    print(f'Слова: {tf_vectorizer.get_feature_names()}')
    print(f'idf: {tf_vectorizer.idf}')
    print('Матрица TF:', *tf_matrix, sep='\n')
    tfidf.fit(['Венера облака'])
    print(f'Слова после переобучения: {tfidf.get_feature_names()}')
    print(f'idf после переобучения: {tfidf.idf}')
    print('Матрица tfidf после переобучения: '
          f'{tfidf.transform(["Марс Венера облака"])}')

    # Сценарий 3 - KeywordExtractor
    extractor: KeywordExtractor
    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(TRAIN_CORPUS)
    print('Ключевые слова при top_n=2:')
    print(extractor.extract(CHECK_CORPUS))
    extractor.top_n = 1
    print('Ключевые слова при top_n=1:')
    print(extractor.extract(CHECK_CORPUS))
    try:
        extractor.top_n = 0
    except ValueError as error:
        print(f'Ошибка при top_n=0: {error}')


if __name__ == '__main__':
    demo()
