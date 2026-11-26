import pytest
from prizes_configs import prize_processor


# Проверка премий
def test_prize_processor():
    """Обработка данных премий."""
    processor = prize_processor()
    assert processor([{'awardYear': '2000'}])[0]['award_year'] == 2000
    assert processor([{}])[0]['award_year'] is None
    assert processor([]) == []


def test_prize_processor_error():
    """Некорректное значение года."""
    processor = prize_processor()
    with pytest.raises(ValueError):
        processor([{'awardYear': 'abc'}])
