from utils import transformation_list_employers, transformation_list_vacancies, append_data_db
from employers import Employers
from db_manager import DBManager
from config import read_config

import psycopg2


def main():
    # получение параметров соединения
    params = read_config()
    # создание экземпляра класса работающего с АПИ ХХ
    emp = Employers()
    # получение информации из АПИ и ее преобразование в утилитах
    employers = transformation_list_employers(emp.get_info_employers())
    vacancies = transformation_list_vacancies(emp.get_info_vacancies())

    try:
        # создание экземпляра класса работающего с бд
        db_manager = DBManager(params)
        # создание таблиц
        db_manager.create_tables()
        # заполнение таблиц обработанными данными
        append_data_db(params, employers, vacancies)
    except psycopg2.OperationalError as e:
        exit(f'{e}Неверные данные!')

    while True:

        print('\nВедите цифру для получения необходимых данных')
        print('Все компании и количество вакансий - 1')
        print('Все вакансии с указанием названия компании, вакансии, зарплаты и ссылки - 2')
        print('Среднюю зарплату по вакансиям - 3')
        print('Все вакансии, у которых зарплата выше средней по всем вакансиям - 4')
        print('Найти вакансии с определенным именем - 5')
        print('Закончить работу - Стоп(stop)')
        user_input = input()

        if user_input == '1':
            for row in db_manager.get_companies_and_vacancies_count():
                print(row)
        elif user_input == '2':
            for row in db_manager.get_all_vacancies():
                print(row)
        elif user_input == '3':
            for row in db_manager.get_avg_salary():
                print(f'от {round(row[0])} до {round(row[1])}')
        elif user_input == '4':
            for row in db_manager.get_vacancies_with_higher_salary():
                print(row)
        elif user_input == '5':
            job_name = input('Название вакансии: ')
            for row in db_manager.get_vacancies_with_keyword(job_name):
                print(row)
        elif user_input.lower() == 'стоп' or 'stop':
            break
        else:
            print('Некорректный ввод!')
            continue

    db_manager.cur.close()
    db_manager.conn.close()


if __name__ == '__main__':
    main()
