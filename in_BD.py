import parse_news
import parse_vacancies
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Создание подключения к БД
def db_connection():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="admin",
                                host="localhost",
                                port="5432",
                                database="site")
        return conn
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# Закрытие подключения к БД
def db_conn_close():
    connection = db_connection()
    connection.close()


# Создание базы данных
def db_created():
    try:
        connection = db_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = 'create database site'
        cursor.execute(sql_create_database)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# ------------------------------------------------------------------Вакансии---------------------------------------------------------
# Создание таблицы Вакансий
def bd_create_table_vacancies():
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = """CREATE TABLE vacancies
                              (ИД INT PRIMARY KEY     NOT NULL,
                              Источник           TEXT,
                              Дата_публикации    timestamp,
                              Вакансия           TEXT,
                              Ссылка             TEXT,
                              ЗП_мин             numeric,
                              ЗП_макс            numeric,
                              Валюта             TEXT,
                              Компания           TEXT,
                              Компания_ссылка    TEXT,
                              Картинка           TEXT,
                              Описание           TEXT,
                              Требования         TEXT,
                              Опыт               TEXT); """

        # Выполнение команды
        cursor.execute(create_table_query)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# Загрузка данных из json в postgresql
def bd_loads_vacancies():
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для заполнения таблицы vacancies
        insert_vacancies = """INSERT INTO vacancies (ИД, Источник, Дата_публикации, Вакансия, Ссылка, ЗП_мин, ЗП_макс,
        Валюта, Компания, Компания_ссылка, Картинка, Описание, Требования, Опыт)
                                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

        for t in parse_vacancies.all_pars_vac():
            values = (
                [(t["ИД"], t["Источник"], t["Дата публикации"], t["Вакансия"], t["Ссылка"], t["ЗП мин"], t["ЗП макс"],
                  t["Валюта"], t["Компания"], t["Компания_ссылка"], t["Картинка"], t["Описание"], t["Требования"],
                  t["Опыт"])])
            # executemany() для вставки нескольких строк
            cursor.executemany(insert_vacancies, values)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# Обновление таблицы вакансий
def bd_update_vacancies():
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = """CREATE TABLE IF NOT EXISTS vacancies_new
                              (ИД INT PRIMARY KEY            NOT NULL,
                              Источник           TEXT,
                              Дата_публикации    timestamp,
                              Вакансия           TEXT,
                              Ссылка             TEXT,
                              ЗП_мин             numeric,
                              ЗП_макс            numeric,
                              Валюта             TEXT,
                              Компания           TEXT,
                              Компания_ссылка    TEXT,
                              Картинка           TEXT,
                              Описание           TEXT,
                              Требования         TEXT,
                              Опыт               TEXT); """

        # Создаем новую таблицу
        cursor.execute(create_table_query)
        # Заполняем новую таблицу
        insert_vacancies = """INSERT INTO vacancies_new (ИД, Источник, Дата_публикации, Вакансия, Ссылка, ЗП_мин,
        ЗП_макс, Валюта, Компания, Компания_ссылка, Картинка, Описание, Требования, Опыт) VALUES (%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s)"""

        for t in parse_vacancies.all_pars_vac():
            values = (
                [(t["ИД"], t["Источник"], t["Дата публикации"], t["Вакансия"], t["Ссылка"], t["ЗП мин"], t["ЗП макс"],
                  t["Валюта"], t["Компания"], t["Компания_ссылка"], t["Картинка"], t["Описание"], t["Требования"],
                  t["Опыт"])])
            # executemany() для вставки нескольких строк
            cursor.executemany(insert_vacancies, values)

        # Добавляем в таблицу Вакансий только новые значения
        insert_new_vacancies = """INSERT INTO vacancies SELECT * FROM vacancies_new n
            WHERE not exists (SELECT 1 FROM vacancies v WHERE v.ИД = n.ИД)"""
        cursor.execute(insert_new_vacancies)

        # Обновляем существующие вакансии
        update_vacancies = """UPDATE vacancies v SET
                            ("Источник", "Дата_публикации", "Вакансия", "Ссылка", "ЗП_мин", "ЗП_макс",
                            "Валюта", "Компания", "Компания_ссылка", "Картинка", "Описание", "Требования", "Опыт") =
                            (SELECT "Источник", "Дата_публикации", "Вакансия", "Ссылка", "ЗП_мин", "ЗП_макс",
                            "Валюта", "Компания", "Компания_ссылка", "Картинка", "Описание", "Требования", "Опыт"
                             FROM vacancies_new n
                             WHERE v."ИД" = n."ИД")
                             WHERE exists (SELECT 1 FROM vacancies_new n WHERE v."ИД" = n."ИД")"""
        cursor.execute(update_vacancies)

        # Удаляем новую таблицу
        delete_tables = """DROP TABLE vacancies_new"""
        cursor.execute(delete_tables)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# ------------------------------------------------------------------Новости---------------------------------------------------------
# Создание таблицы Новостей
def bd_create_table_news():
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = """CREATE TABLE news
                              (ИД serial PRIMARY KEY,
                              Источник           TEXT,
                              Дата_публикации    timestamp,
                              Статья             TEXT,
                              Ссылка             TEXT,                             
                              Картинка           TEXT,
                              Архив              INT); """

        # Выполнение команды
        cursor.execute(create_table_query)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# Загрузка данных из json в postgresql
def bd_loads_news():
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для заполнения таблицы vacancies
        insert_news = """INSERT INTO news (Источник, Дата_публикации, Статья, Ссылка, Картинка)
                                      VALUES (%s,%s,%s,%s,%s) """

        for t in parse_news.all_pars_site():
            values = ([(t["Источник"], t["Дата публикации"], t["Статья"], t["Ссылка"], t["Картинка"])])
            # executemany() для вставки нескольких строк
            cursor.executemany(insert_news, values)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# Обновление таблицы вакансий
def bd_update_news():
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = """CREATE TABLE news_new
                              (ИД serial PRIMARY KEY,
                              Источник           TEXT,
                              Дата_публикации    timestamp,
                              Статья             TEXT,
                              Ссылка             TEXT,                             
                              Картинка           TEXT); """

        # Создаем новую таблицу
        cursor.execute(create_table_query)
        # Заполняем новую таблицу
        insert_news = """INSERT INTO news_new (Источник, Дата_публикации, Статья, Ссылка, Картинка)
                                      VALUES (%s,%s,%s,%s,%s) """

        for t in parse_news.all_pars_site():
            values = ([(t["Источник"], t["Дата публикации"], t["Статья"], t["Ссылка"], t["Картинка"])])
            # executemany() для вставки нескольких строк
            cursor.executemany(insert_news, values)

        # Добавляем в таблицу Новостей только новые значения
        insert_new_news = """INSERT INTO news ("Источник", "Дата_публикации", "Статья", "Ссылка", "Картинка") 
                             SELECT "Источник", "Дата_публикации", "Статья", "Ссылка", "Картинка"
                             FROM news_new n
                             WHERE not exists (SELECT 1 FROM news v WHERE v.Статья = n.Статья)"""
        cursor.execute(insert_new_news)

        # Удаляем новую таблицу
        delete_tables = """DROP TABLE news_new"""
        cursor.execute(delete_tables)

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def insert_in_archive(name):
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Заполняем новую таблицу

        # Добавляем в таблицу Новостей только новые значения
        insert_new_news = """UPDATE news n SET Архив = 1
                            WHERE n.Статья= %s"""
        cursor.execute(insert_new_news, (name,))

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def delete_from_archive(name):
    try:
        connection = db_connection()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Заполняем новую таблицу

        # Добавляем в таблицу Новостей только новые значения
        insert_new_news = """UPDATE news n SET Архив = NULL
                             WHERE n.ИД= %s"""
        cursor.execute(insert_new_news, (name,))

        connection.commit()
        db_conn_close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


