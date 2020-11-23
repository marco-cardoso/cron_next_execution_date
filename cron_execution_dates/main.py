from utils import argument_reader, cron_reader

if __name__ == "__main__":
    time_arg = argument_reader.get_current_time_arg()
    current_datetime = argument_reader.get_current_datetime(time_arg)

    cron = cron_reader.read_cron_cmd()
    while cron is not None:
        cron = cron_reader.read_cron_cmd()
