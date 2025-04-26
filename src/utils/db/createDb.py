from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import os

load_dotenv()
dbUrl = os.getenv('DB_CREATE_URL')
dbName=os.getenv('DB_NAME')

engine = create_engine(dbUrl)
 
def createDB():
    try:
        with engine.connect() as conn:
            conn = conn.execution_options(isolation_level="AUTOCOMMIT")
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": dbName}
            ).fetchone()
            if result:
                print(f"Database '{dbName}' already exists. Skipping creation.")
            else:
                conn.execute(text(f"CREATE DATABASE {dbName}"))
                print(f"Database '{dbName}' created successfully.")
    except ProgrammingError as e:
        print(f"Error while creating db: {e}")
    except Exception as e:
        print(f"Error while creating db: {e}")
   
if __name__=='__main__':
    createDB()
 