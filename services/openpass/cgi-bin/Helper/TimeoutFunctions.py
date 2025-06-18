#!/usr/bin/python3

import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def long_running_function():
    import time
    time.sleep(2)  # Simulates a long-running task
    return 'Hello'

def run_with_timeout(func, params, timeout):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        result = func(*params)
    except TimeoutException:
        result = "TIMEOUT"
    finally:
        signal.alarm(0)  # Disable the alarm
    return result

if __name__ == '__main__':
    print(run_with_timeout(long_running_function, [], 4))