import psycopg2


def transformation_list_employers(employers: list) -> list:
    """
    Сохранение в кортеж информации необходимой для заполнения таблицы.
    :param employers: list работодателей
    :return: tuple с обработанными данными работодателей
    """
    return [(int(emp['id']), emp['name'], emp['description'], emp['site_url']) for emp in employers]


def transformation_list_vacancies(vacancies: list) -> list:
    """
        Сохранение в кортеж информации необходимой для заполнения таблицы.
        :param vacancies: list вакансий
        :return: tuple с обработанными данными вакансий
        """
    data = []
    for v in vacancies:
        if v['salary'] is not None:
            salary_from = v['salary']['from']
            salary_to = v['salary']['to']
        else:
            salary_from = None
            salary_to = None
        data.append(
            [v['employer']['id'], v['name'], v['published_at'],
             v['alternate_url'], v['snippet']['requirement'],
             v['snippet']['responsibility'], v['experience']['name'],
             v['employment']['name'], salary_from, salary_to]
        )
    return data


def append_data_db(database: str, user: str, password: str, employers: list, vacancies: list) -> None:
    """
       Запись данных в БД
       :param database: str имя базы данных
       :param user: str логин пользователя базы данных
       :param password: str пароль пользователя базы данных
       :param employers: list of tuples
       :param vacancies: list of tuples
       :return: None
       """
    with psycopg2.connect(host='localhost', database=database, user=user, password=password) as conn:
        with conn.cursor() as cur:
            for emp in employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s, %s, %s)", emp)
            for v in vacancies:
                cur.execute('INSERT INTO vacancies (employer_id, vacancy_name, published_date,\
                                url, requirement, responsibility, experience, employment, salary_from, salary_to)\
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', v)
