FILENAME = 'contests.csv'
CONTEST_DURATION_SECONDS = 60
CONTEST_PAUSE_SECONDS = 60
CONTEST_MIN_BET = 10
CONTEST_MAX_BET = 10000

# https://streamelements.com/dashboard/account/channels
STREAMELEMENT_ACCOUNT_ID = ''
STREAMELEMENT_JWT_TOKEN = ''

CACHE_SIZE = 1
CSV_FORMAT = {
    'START_ROW_INDEX': 1,
    'QUESTION_COL_INDEX': 0,
    'RESPONSE_COL_INDEX': 1,
    'CHOICES_COL_INDEXES': [1, 2, 3]
}

API_ENDPOINTS = {
    'POST_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}',
    'START_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/start',
    'CLOSE_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/winner',
}
