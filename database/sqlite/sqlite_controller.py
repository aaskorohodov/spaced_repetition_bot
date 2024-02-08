import datetime
import os
import shutil
import sqlite3

from database.db_interface import DBInterface
from database.request_options import RequestOptions
from database.sqlite.query_maker import QueryMaker


class SQLiteControllerLocal(DBInterface):
    def __init__(self):
        self._possible_operations = ['read', 'white', 'update']
        self._possible_types = {
            'INT': int,
            'TEXT': str,
            'BOOLEAN': bool,
            'TIMESTAMP': datetime.datetime
        }

        self._db_path = DBCreator().check_db_exists_or_create()
        self._connect()
        self._check_connection()

        self._connection: sqlite3.Connection

        self._db_structure = self._get_database_structure()

    def _connect(self):
        try:
            self._connection = sqlite3.connect(self._db_path)
            print("Connected to SQLite database")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database:\n\n{e.__str__()}")
            quit()

    def _check_connection(self):
        if self._connection is None or not self._is_connection_alive():
            self._connect()

    def _is_connection_alive(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except sqlite3.Error:
            return False

    def _get_database_structure(self):
        self._check_connection()

        cursor = self._connection.cursor()

        tables_and_columns_raw = {}
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            tables_and_columns_raw[table_name] = {col[1]: col[2] for col in columns}

        tables_and_columns_cleaned = self._convert_types_to_python(tables_and_columns_raw)
        return tables_and_columns_cleaned

    def _convert_types_to_python(self, tables_and_columns: dict) -> dict:
        converted_tables_and_columns = {}
        for table_name, table_structure in tables_and_columns.items():
            converted_tables_and_columns[table_name] = {}

            for column_name, column_type_with_parameters in table_structure.items():
                column_type = self._clear_type_from_parameters(column_type_with_parameters)
                if column_type not in self._possible_types:
                    raise ValueError(
                        f'Unexpected field type ({column_type_with_parameters}) encountered! Check your DB!'
                    )
                converted_tables_and_columns[table_name][column_name] = self._possible_types[column_type]

        return converted_tables_and_columns

    def _clear_type_from_parameters(self, raw_field_type: str) -> str:
        return raw_field_type.split(' ')[0]

    # Actions

    def read(self, request_options: RequestOptions) -> list[tuple] | tuple:
        self._check_connection()
        self._check_request_options(request_options)
        query = QueryMaker.make_query(request_options)
        cursor = self._connection.cursor()
        cursor.execute(query)

        if request_options.get_all_results:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        cursor.close()

        return result

    def write(self, request_options: RequestOptions):
        pass

    def update(self, request_options: RequestOptions):
        pass

    def _check_request_options(self, request_options: RequestOptions) -> None:
        self._check_where_too_look(request_options)
        self._check_what_to_look_for(request_options)
        self._check_where_clause(request_options)
        self._check_operation_type(request_options)

    def _check_where_too_look(self, request_options: RequestOptions) -> None:
        if request_options.where_to_look not in self._db_structure:
            raise LookupError(f'Requested table {request_options.where_to_look} was not found in DB!')

    def _check_what_to_look_for(self, request_options: RequestOptions) -> None:
        if request_options.what_to_look_for:
            requested_table_structure = self._db_structure[request_options.where_to_look]
            if request_options.what_to_look_for not in requested_table_structure:
                raise LookupError(f'You are trying to find column {request_options.what_to_look_for} in '
                                  f'{request_options.where_to_look}, and there is no such column there!')

    def _check_where_clause(self, request_options: RequestOptions) -> None:
        if request_options.where_clause:
            requested_table_structure = self._db_structure[request_options.where_to_look]
            for column_name, data in request_options.where_clause.items():
                if column_name not in requested_table_structure:
                    raise LookupError(f'Column {column_name} was not found in DB!')
                column_type = requested_table_structure[column_name]
                if not isinstance(data, column_type):
                    raise ValueError(f'You are trying to save {type(data)} into column of type {column_type}!')

    def _check_operation_type(self, request_options: RequestOptions) -> None:
        if request_options.operation_type not in self._possible_operations:
            raise ValueError(f'You are trying to execute operation {request_options.operation_type}, '
                             f'while {self.__str__()} only supports: {self._possible_operations}')


class DBCreator:
    def check_db_exists_or_create(self):
        database_path = os.environ.get('DB_PATH')
        if not os.path.exists(database_path):
            self._copy_example_db()

        return database_path

    def _copy_example_db(self):
        try:
            database_path = os.environ.get('DB_PATH')
            example_db_path = os.environ.get('EXAMPLE_DB_PATH')

            self._check_paths_provided(database_path, example_db_path)

            shutil.copyfile(example_db_path, database_path)
        except Exception as e:
            print(f"Error creating Database!:\n\n{e.__str__()}")
            quit()

    def _check_paths_provided(self, *paths):
        for path in paths:
            if not path:
                raise ValueError(f'Some of the paths was empty!')
