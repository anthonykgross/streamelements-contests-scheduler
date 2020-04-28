import csv
import json

import requests

from models import Contest, Choice

r = requests.get('https://api.github.com/user', auth=('user', 'pass'))


class HttpClient:
    def __init__(self, endpoints, account_id, token):
        self.__token = token
        self.__endpoint_post_contest = str(endpoints['POST_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_start_contest = str(endpoints['START_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_close_contest = str(endpoints['CLOSE_CONTEST']).replace('${ACCOUNT_ID}', account_id)

    def get_headers(self):
        return {
            'Authorization': "Bearer "+self.__token,
            'Content-Type': "application/json",
        }

    def post_contest(self, contest):
        endpoint = self.__endpoint_post_contest
        return requests.post(endpoint, data=json.dumps(contest.to_data_endpoint()), headers=self.get_headers())

    def start_contest(self, contest):
        endpoint = self.__endpoint_start_contest.replace('${CONTEST_ID}', contest.id)
        return requests.put(endpoint, headers=self.get_headers())

    def close_contest(self, contest):
        endpoint = self.__endpoint_close_contest.replace('${CONTEST_ID}', contest.id)
        response = contest.choices[contest.response_index]
        data = {"winnerId": response.id}
        return requests.put(endpoint, data=json.dumps(data), headers=self.get_headers())


class CSVReader:
    def __init__(self, filename, csv_format):
        self.__filename = filename
        self.__csv_format = csv_format

    def get_contests(self):
        contests = []
        with open(self.__filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

            for index in range(self.__csv_format['START_ROW_INDEX'], len(rows)):
                row = rows[index]
                contest = self.__row_to_contest(row)
                contests.append(contest)
        return contests

    def __row_to_contest(self, row):
        contest = Contest()
        contest.title = row[self.__csv_format['QUESTION_COL_INDEX']]

        for index in self.__csv_format['CHOICES_COL_INDEXES']:
            choice = Choice()
            choice.title = row[index]
            contest.choices.append(choice)

            if index == self.__csv_format['RESPONSE_COL_INDEX']:
                contest.response_index = len(contest.choices)-1

        if contest.response_index is None:
            raise Exception('Response index must be in the choices list')

        return contest