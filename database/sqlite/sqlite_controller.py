import datetime
import os
import shutil
from pathlib import Path
from sqlite3 import OperationalError

from ..sql_alchemy_models import Base

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker

from database.db_interface import DBInterface
from database.sql_alchemy_models.users import User
from ..sql_alchemy_models.log import Log


class SQLiteControllerLocal(DBInterface):
    def __init__(self):
        self._db_path: Path = DBCreator().check_db_exists_or_create()
        self.engine: Engine = create_engine(f"sqlite:///{self._db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self._check_connection()

    # Connection

    def _check_connection(self):
        try:
            with self.engine.connect() as connection:
                # Execute a simple query to check the connection
                result = connection.execute(text('SELECT 1'))
                row = result.fetchone()
                if row and row[0] == 1:
                    print("Connection to SQLite database is successful.")
                else:
                    print("Failed to verify connection to SQLite database.")
        except OperationalError as e:
            # Handle connection errors
            print(f"Error connecting to SQLite database: {e}")

    # Actions

    def get_user_by_id(self, user_id: int):
        session = self.Session()
        user = session.query(User).filter_by(user_id=user_id).first()
        session.close()
        return user

    def save_new_user(self, user_id: int, user_name: str):
        session = self.Session()
        new_user = User(
            user_id=user_id,
            user_name=user_name,
            on_off=True,
            language=None
        )
        session.add(new_user)
        session.commit()
        session.close()

    def update_user(self, updated_user_model: User):
        session = self.Session()

        old_user_record = session.query(User).filter_by(user_id=updated_user_model.user_id).first()
        old_user_record.user_name = updated_user_model.user_name
        old_user_record.on_off = updated_user_model.on_off
        old_user_record.language = updated_user_model.language

        session.commit()
        session.close()

    def save_log(self, log_made_by: str, log_text: str):
        session = self.Session()

        new_log = Log(
            log_made_by=log_made_by,
            log_text=log_text,
            log_time=datetime.datetime.now()
        )
        session.add(new_log)
        session.commit()
        session.close()

    # Service


class DBCreator:
    def check_db_exists_or_create(self):
        database_path = self._get_path_to_file(os.getenv('DB_PATH'))

        if not os.path.exists(database_path):
            self._copy_example_db()

        return database_path

    def _get_path_to_file(self, file_path: str):
        script_dir_string = os.path.dirname(os.path.abspath(__file__))
        script_dir_path = Path(script_dir_string)
        your_file_path = script_dir_path / file_path

        return your_file_path

    def _copy_example_db(self):
        try:
            database_path = self._get_path_to_file(os.getenv('DB_PATH'))
            example_db_path = self._get_path_to_file(os.getenv('EXAMPLE_DB_PATH'))

            shutil.copyfile(example_db_path, database_path)
        except Exception as e:
            print(f"Error creating Database!:\n\n{e.__str__()}")
            quit()
