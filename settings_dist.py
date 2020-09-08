FILENAME = 'contests.csv'
CONTEST_DURATION_SECONDS = 5 * 60
CONTEST_PAUSE_SECONDS = 5 * 60
CONTEST_BET = 100
CONTEST_MIN_BET = 10
CONTEST_MAX_BET = 10000

# https://streamelements.com/dashboard/account/channels
STREAMELEMENT_ACCOUNT_ID = ''
STREAMELEMENT_JWT_TOKEN = ''

CACHE_SIZE = 5
CSV_FORMAT = {
    'START_ROW_INDEX': 1,
    'QUESTION_COL_INDEX': 0,
    'RESPONSE_COL_INDEX': 1,
    'OPTIONS_COL_INDEXES': [1, 2, 3]
}

API_ENDPOINTS = {
    'LIST_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}',
    'POST_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}',
    'START_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/start',
    'WINNER_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/winner',
    'BET_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/bet',
    'REFUND_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/refund',
    'CLOSE_CONTEST': 'https://api.streamelements.com/kappa/v2/contests/${ACCOUNT_ID}/${CONTEST_ID}/close',
}
