from utils import transformation_list_employers, transformation_list_vacancies, append_data_db
from employers import Employers
from db_manager import DBManager
import psycopg2


def main():
    emp = Employers()
    employers = transformation_list_employers(emp.get_info_employers())
    vacancies = transformation_list_vacancies(emp.get_info_vacancies())

    user = input('Привет! Напиши данные для входа в базу данных \nИмя пользователя: ')
    password = input('Пароль: ')
    database = input('Название базы данных: ')
    try:

        db_manager = DBManager(database, user, password)
        db_manager.create_database()
        append_data_db(database, user, password, employers, vacancies)
    except psycopg2.OperationalError as e:
        exit(f'{e}Неверные данные!')

    while True:
        user_input = input('Напиши номер данных, которые необходимо вывести?\n\
Все компании и количество вакансий - 1\n\
Все вакансии с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию - 2\n\
Среднюю зарплату по вакансиям - 3\n\
Все вакансии, у которых зарплата выше средней по всем вакансиям - 4\n\
Найти вакансии с определенным именем - 5\n\
Закончить работу - Стоп\n')

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
            print('Неверные данные!')

    db_manager.cur.close()
    db_manager.conn.close()


if __name__ == '__main__':
    main()
