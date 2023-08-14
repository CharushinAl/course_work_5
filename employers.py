import requests
import json


class Employers:

    # Список работодателей, id с сайта hh.ru
    employers_id = ['1740', '1122462', '1057', '3529', '1805417', '15478', '3388', '80', '3749373', '733']

    def get_info_employers(self) -> list:
        """
        Выводит список с описанием работодателей
        :return: list
        """
        data = []
        for i in self.employers_id:
            response = requests.get('https://api.hh.ru/employers/' + i)
            date_hh = response.content.decode()
            hh_json = json.loads(date_hh)
            data.append(hh_json)
        return data

    def get_info_vacancies(self) -> list:
        """
        Выводит список вакансий от заданных работодателей
        :return: list
        """
        data = []
        for i in self.employers_id:
            response = requests.get('https://api.hh.ru/vacancies', params={'employer_id': i, 'per_page': 100})
            # job_hh = response.content.decode()
            # job_json = json.loads(job_hh)
            # info.append(job_json)
            row_data = response.json()['items']  # json method requests
            data.extend(row_data)
        return data
