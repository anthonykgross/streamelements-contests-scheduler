from settings import settings

import time

from models import Runner, Cache
from utils import CSVReader, HttpClient

http_client = HttpClient(
    settings.API_ENDPOINTS,
    settings.STREAMELEMENT_ACCOUNT_ID,
    settings.STREAMELEMENT_JWT_TOKEN,
)
csv_reader = CSVReader(
    settings.FILENAME,
    settings.CSV_FORMAT
)
cache = Cache(settings.CACHE_SIZE)

runner = Runner(
    csv_reader.get_contests(),
    cache,
    http_client,
    settings.CONTEST_MIN_BET,
    settings.CONTEST_MAX_BET,
    settings.CONTEST_DURATION_SECONDS,
)

nb_seconds_to_bet = round(settings.CONTEST_DURATION_SECONDS * 0.75)
nb_seconds_rest = settings.CONTEST_DURATION_SECONDS-nb_seconds_to_bet

while True:
    runner.next_contest()
    time.sleep(nb_seconds_to_bet)
    runner.bet(settings.CONTEST_BET)
    time.sleep(nb_seconds_rest)
    runner.complete_contest()
    time.sleep(settings.CONTEST_PAUSE_SECONDS)
