import requests
import pytz
from datetime import datetime, time


def load_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    result = requests.get(url).json()
    pages = result.get('number_of_pages')
    for page in range(pages):
        url = 'https://devman.org/api/challenges/solution_attempts/?page={}'.format(page + 1)
        result = requests.get(url).json()
        yield result.get('records')


def localize_time(timestamp, timezone):
    timezone = pytz.timezone(timezone)
    utc_submission_time = datetime.utcfromtimestamp(timestamp)
    local_submission_time = timezone.localize(utc_submission_time)
    return local_submission_time


def is_midnighter(timestamp):
    midnight = time(0, 0)
    morning = time(6, 0)
    return midnight <= timestamp <= morning


def get_midnighters(page):
    midnighters = dict()
    for record in page:
        timestamp = record.get('timestamp')
        timezone = record.get('timezone')
        username = record.get('username')
        if not timestamp:
            continue
        timestamp = float(timestamp)
        local_submission_time = localize_time(timestamp, timezone)
        if is_midnighter(local_submission_time.time()):
            midnighters[username] = [timezone, local_submission_time]
    return midnighters


def output_midnighters_to_console(midnighters):
    for user, time_info in midnighters.items():
        timezone, submission_time = time_info
        pretty_time = submission_time.strftime('%d-%m-%Y %H:%M:%S')
        print('User {0} submitted at {1} from {2}'.format(user, pretty_time, timezone))


if __name__ == '__main__':
    for page in load_attempts():
        midnighters = get_midnighters(page)
        output_midnighters_to_console(midnighters)
