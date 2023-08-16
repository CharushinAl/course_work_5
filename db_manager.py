import psycopg2


class DBCreate:

    def __init__(self, params: dict):
        """Инициализация соединения и курсора по параметрам из config."""

        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_tables(self) -> None:
        """Создает таблицы работодатели и вакансии."""

        self.cur.execute("""
                        CREATE TABLE employers 
                        (
                            employer_id int,
                            employer_name varchar NOT NULL,
                            description varchar,
                            url varchar,
                        
                            CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
                        )
                    """)

        self.cur.execute("""
                       CREATE TABLE vacancies
                       (
                            vacancy_id serial,
                            employer_id int,
                            vacancy_name varchar,
                            published_date date,
                            url varchar,
                            requirement varchar,
                            responsibility varchar,
                            experience varchar(25),
                            employment varchar,
                            salary_from int DEFAULT 0,
                            salary_to int DEFAULT 0,
                        
                            CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id),
                            CONSTRAINT fk_employers_employer_id FOREIGN KEY (employer_id) 
                            REFERENCES employers(employer_id)
                        )
                   """)


class DBManager(DBCreate):

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        self.cur.execute("""
                            SELECT employers.employer_name, COUNT(vacancies.vacancy_id)
                            AS count_vacancies FROM employers
                            INNER JOIN vacancies USING(employer_id) GROUP BY employers.employer_name
                        """)
        rows = self.cur.fetchall()
        return rows

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cur.execute("""
                            SELECT employers.employer_name, vacancy_name, salary_from, salary_to, vacancies.url
                            FROM vacancies INNER JOIN employers USING(employer_id)
                        """)
        rows = self.cur.fetchall()
        return rows

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        self.cur.execute("""
                            SELECT AVG(salary_from), AVG(salary_to) FROM vacancies
                        """)
        rows = self.cur.fetchall()
        return rows

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        self.cur.execute("""
                            SELECT * FROM vacancies WHERE (salary_from + salary_to) / 2 > 
                            (SELECT AVG((salary_from + salary_to) / 2)
                            FROM vacancies)
                        """)
        rows = self.cur.fetchall()
        return rows

    def get_vacancies_with_keyword(self, key_word: str):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например “python”.
        """
        self.cur.execute(f"""
                            SELECT * FROM vacancies WHERE vacancy_name ILIKE '%{key_word}%'
                        """)
        rows = self.cur.fetchall()
        return rows
