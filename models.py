import random
from builtins import print


class Choice:
    def __init__(self):
        self.id = None
        self.title = ''
        self.command = ''

    def to_data_endpoint(self):
        d = {
            'title': self.title,
            'command': self.command,
        }

        return d


class Contest:
    def __init__(self):
        self.id = None
        self.title = ''
        self.min_bet = 0
        self.max_bet = 0
        self.duration = 0
        self.response_index = None
        self.options = []
        self.shuffle_options_index = []

    def to_data_endpoint(self):
        d = {
            'title': self.title,
            'minBet': self.min_bet,
            'maxBet': self.max_bet,
            'duration': self.duration,
            'options': []
        }

        if self.id is not None:
            d['_id'] = self.id

        self.shuffle_options_index = list(range(len(self.options)))
        random.shuffle(self.shuffle_options_index)

        i = 1
        for index in self.shuffle_options_index:
            option = self.options[index]
            option.command = str(i)
            i += 1
            d['options'].append(option.to_data_endpoint())

        return d

    def update_from_endpoint_response(self, json):
        self.id = json['_id']
        for index in range(len(json['options'])):
            real_index = self.shuffle_options_index[index]
            option = self.options[real_index]
            option.id = json['options'][index]['_id']


class Runner:
    def __init__(self, contests, cache, http_client, min_bet, max_bet, contest_duration):
        self.__contests = contests
        self.__cache = cache
        self.__http_client = http_client
        self.__current_contest = None
        self.__min_bet = min_bet
        self.__max_bet = max_bet
        self.__contest_duration = contest_duration

    def __get_random(self, min, max):
        rate = 1000
        max *= rate
        rnd = random.randrange(min, max)

        if rnd > 0:
            rnd = round(
                rnd / rate
            )
        return rnd

    def __get_random_contest(self):
        rnd = self.__get_random(0, len(self.__contests) - 1)

        while self.__cache.exists(rnd):
            rnd = self.__get_random(0, len(self.__contests) - 1)

        self.__cache.add(rnd)
        return self.__contests[rnd]

    def bet(self, amount):
        print('> Bet contest : %s' % amount)

        rnd = self.__get_random(0, len(self.__current_contest.options) - 1)
        option_id = self.__current_contest.options[rnd].id
        self.__http_client.bet_contest(self.__current_contest, amount, option_id)

    def next_contest(self):
        print('> Next contest : ')
        self.__current_contest = self.__get_random_contest()
        self.__current_contest.min_bet = self.__min_bet
        self.__current_contest.max_bet = self.__max_bet
        self.__current_contest.duration = round(self.__contest_duration / 60)

        print('%s' % self.__current_contest.title)
        response = self.__http_client.post_contest(self.__current_contest)

        if response.status_code == 200:
            self.__current_contest.update_from_endpoint_response(response.json())
            self.__http_client.start_contest(self.__current_contest)

    def complete_contest(self):
        print('> Contest completed !')
        self.__http_client.close_contest(self.__current_contest)


class Cache:
    def __init__(self, size):
        if size <= 0:
            size = -1

        self.size = size
        self.cache = []

    def exists(self, value):
        return value in self.cache

    def add(self, value):
        self.cache.append(value)
        self.__keep_latest_values()

    def remove(self, value):
        for v in self.cache:
            index = self.cache.index(v)
            if value == self.cache[index]:
                del self.cache[index]

    @property
    def length(self):
        return len(self.cache)

    def __keep_latest_values(self):
        self.cache = self.cache[-1 * self.size:]
