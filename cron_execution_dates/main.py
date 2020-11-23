from cron_execution_dates.utils import argument_reader

if __name__ == "__main__":
    time_arg = argument_reader.get_current_time_arg()
    current_datetime = argument_reader.get_current_datetime(time_arg)

    cron_cmd = argument_reader.read_cron_cmd()
    while cron_cmd is not None:
        cron_cmd = argument_reader.read_cron_cmd()
