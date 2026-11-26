import pytest
from laureates_configs import process_year, person_processor, org_processor


# Проверка извлечения года
def test_process_year():
    """Извлечение года из строки."""
    assert process_year('2000-00-00') == 2000
    assert process_year('2000') == 2000
    assert process_year('20') is None
    assert process_year('abc') is None
    assert process_year('') is None
    assert process_year('2000-aa-bb') is None
    assert process_year('2000abc') is None
    # С одной строны должна возвращать None,
    # а с другой как будто и можно достать год.
    # Пропишем, чтобы позвращала None.


def test_process_year_errors():
    """Переданы неверные типы."""
    for value in [2000, None, [], {}]:
        with pytest.raises(TypeError):
            process_year(value)


# Проверка обработки человека
def test_person_processor():
    """Обработка данных человека."""
    processor = person_processor()
    data = {'birth': {'date': '2000-01-01'}}
    assert processor(data)['birth_year'] == 2000
    assert processor({})['birth_year'] is None


# Проверка обработки организации
def test_org_processor():
    """Обработка данных организации."""
    processor = org_processor()
    data = {'founded': {'date': '1900-01-01'}}
    assert processor(data)['founded_year'] == 1900
    assert processor({})['founded_year'] is None
