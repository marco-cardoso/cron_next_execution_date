import pytest
from datetime import datetime
from cron_next_execution_date.utils import argument_reader


def test_validate_current_time_re():
    assert argument_reader.__validate_current_time_re("16:00") is True
    assert argument_reader.__validate_current_time_re("00:00") is True
    assert argument_reader.__validate_current_time_re("0:00") is True
    assert argument_reader.__validate_current_time_re("100:00") is False
    assert argument_reader.__validate_current_time_re("99:00") is True
    assert argument_reader.__validate_current_time_re("00:99") is True
    assert argument_reader.__validate_current_time_re("0:0") is False
    assert argument_reader.__validate_current_time_re("") is False
    assert argument_reader.__validate_current_time_re("sadaldam") is False


def test_get_time_components():
    assert argument_reader.__get_time_components("16:00") == argument_reader.Time(hour=16, minute=0)
    assert argument_reader.__get_time_components("0:00") == argument_reader.Time(hour=0, minute=0)
    assert argument_reader.__get_time_components("00:00") == argument_reader.Time(hour=0, minute=0)


def test_get_current_datetime():

    now = datetime.now()

    dt = argument_reader.get_current_datetime("12:00")
    assert ((dt.hour == 12) and (dt.minute == 0) and (dt.day == now.day) and (dt.month == now.month) and (dt.year == now.year))

    dt = argument_reader.get_current_datetime("00:00")
    assert ((dt.hour == 0) and (dt.minute == 0) and (dt.day == now.day) and (dt.month == now.month) and (
                dt.year == now.year))

    with pytest.raises(ValueError):
        argument_reader.get_current_datetime("32:00")

    with pytest.raises(ValueError):
        argument_reader.get_current_datetime("52:00")
