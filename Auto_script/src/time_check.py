from datetime import datetime, time


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    print(check_time)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


# Original test case from OP
print(is_time_between(time(9, 30), time(10, 5)))

# Test case when range crosses midnight
print(is_time_between(time(15, 40), time(16, 50)))
