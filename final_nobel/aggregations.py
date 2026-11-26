from typing import Callable
from statistics import mean, median


def calculate_statistic(
    data: list[dict], attribute: str, statistic: Callable
) -> float | None:
    """Принимает список словарей, название атрибута и функцию агрегации.
    Возвращает результат агрегации без учёта пропусков
    или None при отсутствии значений."""
    values = []
    for record in data:
        if record[attribute] is not None:
            if not isinstance(record[attribute], (int, float)) or isinstance(
                record[attribute], bool
            ):
                raise TypeError('Значение должно быть числом')
            values.append(record[attribute])
    if not values:
        return None
    return statistic(values)


def calculate_mean(data: list[dict], attribute: str) -> float | None:
    """Возвращает среднее значение указанного атрибута."""
    return calculate_statistic(data, attribute, mean)


def calculate_median(data: list[dict], attribute: str) -> float | None:
    """Возвращает медианное значение указанного атрибута."""
    return calculate_statistic(data, attribute, median)


def calculate_max(data: list[dict], attribute: str) -> float | None:
    """Возвращает максимальное значение указанного атрибута."""
    return calculate_statistic(data, attribute, max)


def calculate_min(data: list[dict], attribute: str) -> float | None:
    """Возвращает минимальное значение указанного атрибута."""
    return calculate_statistic(data, attribute, min)


def get_top_n(data: dict, n: int) -> dict:
    """Принимает словарь и количество элементов.
    Возвращает словарь с N наибольшими по значению элементами."""
    if n < 0:
        raise ValueError('Нужно передавать неотрицательный n')
    return dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:n])
