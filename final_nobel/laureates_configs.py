from prizes_configs import prize_processor
from json_dict_processing import create_processor
from typing import Callable


def process_year(year_string: str) -> int | None:
    """Принимает строку даты в формате YYYY-MM-DD.
    Возвращает год в виде целого числа или None,
    если год извлечь невозможно."""
    if not isinstance(year_string, str):
        raise TypeError('Нужно передать строку')
    if year_string[:4].isdigit():
        if len(year_string) == 4:
            return int(year_string)
        if (
            len(year_string) == 10
            and year_string[4] == '-'
            and year_string[7] == '-'
        ):
            if year_string[5:7].isdigit() and year_string[8:].isdigit():
                return int(year_string[:4])
    return None


CONFIG_PERSON = {
    'id': ['id'],
    'name': ['knownName', 'en'],
    'gender': ['gender'],
    'birth_year': (['birth', 'date'], process_year),
    'country_birth': ['birth', 'place', 'country', 'en'],
    'country_now': ['birth', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], prize_processor())
}

CONFIG_ORG = {
    'id': ['id'],
    'name': ['orgName', 'en'],
    'founded_year': (['founded', 'date'], process_year),
    'country_founded': ['founded', 'place', 'country', 'en'],
    'country_now': ['founded', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], prize_processor())
}


def person_processor() -> Callable:
    """Возвращает процессор для обработки данных лауреатов-людей."""
    return create_processor(CONFIG_PERSON)


def org_processor() -> Callable:
    """Возвращает процессор для обработки данных лауреатов-организаций."""
    return create_processor(CONFIG_ORG)
