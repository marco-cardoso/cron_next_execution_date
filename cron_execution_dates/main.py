import datetime
from cron import CRON
from utils import argument_reader, output


def read_cron_cmd(current_datetime : datetime):
    try:
        expression = input()
        cron = CRON(expression, current_datetime=current_datetime)
        return cron
    except EOFError:
        return None


if __name__ == "__main__":
    time_arg = argument_reader.get_current_time_str()
    current_dt = argument_reader.get_current_datetime(time_arg)

    cron_exp = read_cron_cmd(current_dt)
    while cron_exp is not None:

        nxt_exe_day_msg = output.format_output(cron_exp)
        output.print_output(nxt_exe_day_msg)

        cron_exp = read_cron_cmd(current_dt)
