from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


# Define the LogTable model
class LogTable(Base):
    __tablename__ = "log_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    log_level = Column(String(50))
    message = Column(Text)


class DatabaseManager:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_tables(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def write_log(self, log_level, message):
        if "log_table" in self.get_tables():
            session = self.Session()
            new_log = LogTable(log_level=log_level, message=message)
            session.add(new_log)
            session.commit()
            session.close()
            print("Log entry added.")
        else:
            print("Log table does not exist.")

    def read_logs(self):
        if "log_table" in self.get_tables():
            session = self.Session()
            logs = session.query(LogTable).all()
            session.close()
            return logs
        else:
            print("Log table does not exist.")
            return None


if __name__ == "__main__":
    import os

    DB_USR = os.environ.get("DB_USR", "sa")
    DB_PWD = os.environ.get("DB_PWD", "password123!")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "LogDatabase")
    DB_DRIVER = os.environ.get("DB_DRIVER", "ODBC+Driver+17+for+SQL+Server")

    DATABASE_URL = (
        f"mssql+pyodbc://{DB_USR}:{DB_PWD}@{DB_HOST}/{DB_NAME}?driver={DB_DRIVER}"
    )
    db_manager = DatabaseManager(DATABASE_URL)

    # Example Usage
    print("Tables in the database:", db_manager.get_tables())

    # Adding a log entry
    db_manager.write_log("INFO", "This is a test log entry.")

    # Reading all log entries
    logs = db_manager.read_logs()
    for log in logs:
        print(
            f"ID: {log.id}, Level: {log.log_level}, Message: {log.message}, Timestamp: {log.timestamp}"
        )
