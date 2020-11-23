import pytest
from cron_execution_dates.utils import cron_reader


def test_valid_hour():
    assert cron_reader.valid_hour(-2) is False
    assert cron_reader.valid_hour(24) is False
    assert cron_reader.valid_hour(44) is False
    assert cron_reader.valid_hour(4) is True
    assert cron_reader.valid_hour(0) is True
    assert cron_reader.valid_hour(23) is True


def test_valid_minute():
    assert cron_reader.valid_minute(-2) is False
    assert cron_reader.valid_minute(67) is False
    assert cron_reader.valid_minute(30) is True
    assert cron_reader.valid_minute(20) is True


def test_validate_cron_cmd():
    cmd = "* * /bin/test.sh"
    cron = cron_reader.CRON(cmd)
    assert cron.minute == "*"
    assert cron.hour == "*"

    cmd = "*       * /bin/test.sh"
    cron = cron_reader.CRON(cmd)
    assert cron.minute == "*"
    assert cron.hour == "*"

    cmd = "* *       /bin/test.sh"
    cron = cron_reader.CRON(cmd)
    assert cron.minute == "*"
    assert cron.hour == "*"

    cmd = "35 * /bin/test.sh"
    cron = cron_reader.CRON(cmd)
    assert cron.minute == "35"
    assert cron.hour == "*"

    cmd = "* 5 /bin/test.sh"
    cron = cron_reader.CRON(cmd)
    assert cron.minute == "*"
    assert cron.hour == "5"

    cmd = "5 5 /bin/test.sh"
    cron = cron_reader.CRON(cmd)
    assert cron.minute == "5"
    assert cron.hour == "5"

    cmd = "95 5 /bin/test.sh"
    with pytest.raises(ValueError):
        cron_reader.CRON(cmd)

    cmd = "* 25 /bin/test.sh"
    with pytest.raises(ValueError):
        cron_reader.CRON(cmd)

    cmd = "* -2 /bin/test.sh"
    with pytest.raises(AttributeError):
        cron_reader.CRON(cmd)

    cmd = "* -2 /"
    with pytest.raises(AttributeError):
        cron_reader.CRON(cmd)

    cmd = "* * /dasda@xa@!#^DA "
    with pytest.raises(ValueError):
        cron_reader.CRON(cmd)

    cmd = "*  /dasda@xa@!#^DA "
    with pytest.raises(AttributeError):
        cron_reader.CRON(cmd)

