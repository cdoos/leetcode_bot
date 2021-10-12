import requests
import json
from query.query_config import URL, HEADERS, QUERY_PROFILE, QUERY_RECENT_SUBMISSION
from datetime import datetime, timedelta


def getuser(username: str) -> str:
    try:
        data = getprofile(username)
        return 'Username: ' + username + \
               '\nEasy: ' + str(data[1]) + \
               '\nMedium: ' + str(data[2]) + \
               '\nHard: ' + str(data[3]) + \
               '\nAll: ' + str(data[4]) + \
               '\nRecent Submission: ' + str(data[5])
    except ValueError as e:
        return str(e)


def getprofile(username: str) -> tuple:
    query = QUERY_PROFILE
    query['variables']['username'] = username
    response = json.loads(requests.post(url=URL, headers=HEADERS, data=json.dumps(query)).text)
    if 'errors' in response:
        raise ValueError('Profile ' + username + ' does not exist!')
    data = response['data']['matchedUser']['submitStats']['acSubmissionNum']
    query = QUERY_RECENT_SUBMISSION
    query['variables']['username'] = username
    response = json.loads(requests.post(url=URL, headers=HEADERS, data=json.dumps(query)).text)
    response = response['data']['recentSubmissionList']
    if len(response) > 0:
        response = response[0]
        date = datetime.fromtimestamp(int(response['timestamp'])) + timedelta(hours=6)
        recent_submission = response['title'] + ' (' + str(date) + ') '
    else:
        recent_submission = '-'
    return username, data[1]['count'], data[2]['count'], data[3]['count'], data[0]['count'], recent_submission
