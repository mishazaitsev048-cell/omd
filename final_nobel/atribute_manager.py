from typing import Callable


def add_attribute(
    data: list[dict], attribute: str, calculation: Callable
) -> list[dict]:
    """Принимает список словарей, название нового атрибута
    и функцию расчёта его значения.
    Возвращает список словарей с добавленным атрибутом."""
    updated_data = []
    for record in data:
        new_record = record.copy()
        new_record[attribute] = calculation(new_record)
        updated_data.append(new_record)
    return updated_data
