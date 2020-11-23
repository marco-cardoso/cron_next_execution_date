from cron import CRON


def read_cron_cmd():
    try:
        expression = input()
        cron = CRON(expression)
        return cron
    except EOFError:
        return None
