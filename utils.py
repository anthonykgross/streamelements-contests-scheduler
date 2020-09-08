import csv
import json
import requests

from models import Contest, Choice


class HttpClient:
    def __init__(self, endpoints, account_id, token):
        self.__token = token
        self.__endpoint_post_contest = str(endpoints['POST_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_start_contest = str(endpoints['START_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_winner_contest = str(endpoints['WINNER_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_bet_contest = str(endpoints['BET_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_list_contest = str(endpoints['LIST_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_refund_contest = str(endpoints['REFUND_CONTEST']).replace('${ACCOUNT_ID}', account_id)
        self.__endpoint_close_contest = str(endpoints['CLOSE_CONTEST']).replace('${ACCOUNT_ID}', account_id)

    def get_headers(self):
        return {
            'Authorization': "Bearer "+self.__token,
            'Content-Type': "application/json",
        }

    def refund(self):
        endpoint = self.__endpoint_list_contest
        response = requests.get(endpoint, headers=self.get_headers())
        if response.status_code == 200:
            data = response.json()

            for contest in data['contests']:
                if contest['state'] == 'running':
                    url = self.__endpoint_close_contest.replace('${CONTEST_ID}', contest['_id'])
                    requests.delete(url, headers=self.get_headers())
                    url = self.__endpoint_refund_contest.replace('${CONTEST_ID}', contest['_id'])
                    requests.delete(url, headers=self.get_headers())

    def post_contest(self, contest):
        endpoint = self.__endpoint_post_contest
        return requests.post(endpoint, data=json.dumps(contest.to_data_endpoint()), headers=self.get_headers())

    def bet_contest(self, contest, amount, option_id):
        endpoint = self.__endpoint_bet_contest.replace('${CONTEST_ID}', contest.id)
        data = {
            'amount': amount,
            'optionId': option_id
        }
        return requests.post(endpoint, data=json.dumps(data), headers=self.get_headers())

    def start_contest(self, contest):
        endpoint = self.__endpoint_start_contest.replace('${CONTEST_ID}', contest.id)
        return requests.put(endpoint, headers=self.get_headers())

    def close_contest(self, contest):
        endpoint = self.__endpoint_winner_contest.replace('${CONTEST_ID}', contest.id)
        response = contest.options[contest.response_index]
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

        for index in self.__csv_format['OPTIONS_COL_INDEXES']:
            option = Choice()
            option.title = row[index]
            contest.options.append(option)

            if index == self.__csv_format['RESPONSE_COL_INDEX']:
                contest.response_index = len(contest.options)-1

        if contest.response_index is None:
            raise Exception('Response index must be in the options list')

        return contest
