import pytest
from datetime import datetime
from ..utils import output, argument_reader
from ..cron import CRON


def test_get_execution_day_str():
    exe_day = output.get_execution_day_str(28, 29)
    assert exe_day == "tomorrow"

    exe_day = output.get_execution_day_str(28, 28)
    assert exe_day == "today"

    exe_day = output.get_execution_day_str(1, 1)
    assert exe_day == "today"

    with pytest.raises(ValueError):
        output.get_execution_day_str(1, 3)


def test_get_msg():
    dt = datetime(2020, 11, 23, 10, 0, 0)
    file = "/bin/test.sh"
    day = "today"

    msg = output.get_msg(dt, day, file)
    assert msg == f"10:00 {day} - {file}"

    dt = datetime(2020, 11, 23, 1, 0, 0)

    msg = output.get_msg(dt, day, file)
    assert msg == f"01:00 {day} - {file}"


def test_format_output():
    file = "/bin/test.sh"
    exp = f"* * {file}"
    curent_dt = argument_reader.get_current_datetime("14:00")
    cron = CRON(exp, curent_dt)

    nxt_exe_dt = cron.next_execution_date
    cur_dt = cron.current_date

    exe_day = output.get_execution_day_str(cur_dt.day, nxt_exe_dt.day)
    assert output.format_output(cron) == f"14:01 {exe_day} - {file}"
