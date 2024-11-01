from config import config
from loguru import logger as lg
import psycopg2
from psycopg2 import pool
import os


# Класс БД
class Database:
    # Инициализация
    def __init__(self):
        try:
            # Пытаемся подключиться к базе данных
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=os.environ["POSTGRES_HOST"],
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                database=os.environ["POSTGRES_DB"],
                port=os.environ["POSTGRES_PORT"],
            )
            lg.info("SYSTEM - Connection to database complete")

        except Exception as e:
            # В случае сбоя подключения будет выведено сообщение в STDOUT
            lg.error("ERROR - Can`t establish connection to database")
            return

        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                                CREATE TABLE IF NOT EXISTS users (  
                                    id int,
                                    name VARCHAR(255),
                                    last_msg_id  VARCHAR(255),
                                    lang VARCHAR(255)
                                )"""
                    )
                    cursor.execute(
                        f"""
                                CREATE TABLE IF NOT EXISTS admin (  
                                    tokens_all VARCHAR(255),
                                    tokens_today VARCHAR(255),
                                    users_count VARCHAR(255),
                                    requests_today VARCHAR(255),
                                    requests_all VARCHAR(255)
                                )"""
                    )
                    cursor.execute(f"SELECT FROM admin")
                    if cursor.fetchone() is None:
                        cursor.execute(
                            "INSERT INTO admin VALUES (%s, %s, %s, %s, %s)",
                            ("0", "0", "0", "0", "0"),
                        )

        finally:
            self.release_connection(connection)

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, connection):
        self.connection_pool.putconn(connection)

    # Запись нового пользователя -> users
    def recording(self, id, name):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT id FROM users WHERE id = '{id}'")
                    if cursor.fetchone() is None:
                        cursor.execute(
                            "INSERT INTO users VALUES (%s, %s, %s, %s)",
                            (id, name, "0", "rus"),
                        )
        finally:
            self.release_connection(connection)

    # Проверка на нового пользователя
    def isReg(self, id):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT id FROM users WHERE id = %s", (id,))
                    if cursor.fetchone() is None:
                        return False
                    else:
                        return True
        finally:
            self.release_connection(connection)

    # Обновить запись
    def update(self, id, table, object, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE {table} SET {object} = %s WHERE id = %s",
                        (
                            value,
                            id,
                        ),
                    )
        finally:
            self.release_connection(connection)

    # Получить запись
    def read(self, id, table, object):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT {object} FROM {table} WHERE id = %s", (id,))
                    result = cursor.fetchall()
                    return result[0][0]
        finally:
            self.release_connection(connection)

    # Обновить запись
    def update_tokens_all(self, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE admin SET tokens_all = %s",
                        (value,),
                    )
        finally:
            self.release_connection(connection)

    def update_tokens_today(self, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE admin SET tokens_today = %s",
                        (value,),
                    )
        finally:
            self.release_connection(connection)

    def update_users_count(self, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE admin SET users_count = %s",
                        (value,),
                    )
        finally:
            self.release_connection(connection)

    def update_requests_today(self, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE admin SET requests_today = %s",
                        (value,),
                    )
        finally:
            self.release_connection(connection)

    def update_requests_all(self, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE admin SET requests_all = %s",
                        (value,),
                    )
        finally:
            self.release_connection(connection)

    def get_users_count(self):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT COUNT(*) FROM user")
                    result = cursor.fetchall()
                    return result[0][0]
        finally:
            self.release_connection(connection)

    def read_admin(self, value):
        connection = self.get_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT {value} FROM admin")
                    result = cursor.fetchall()
                    return result[0][0]
        finally:
            self.release_connection(connection)
