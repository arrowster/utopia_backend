

def print_running_time(start_time, end_time):
    start_seconds = start_time.tm_hour * 3600 + start_time.tm_min * 60 + start_time.tm_sec
    end_seconds = end_time.tm_hour * 3600 + end_time.tm_min * 60 + end_time.tm_sec

    total_seconds = end_seconds - start_seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return print(f'총 수집 시간: {hours}:{minutes}:{seconds}')
