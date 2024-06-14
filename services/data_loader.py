import os
import logging
import psycopg2
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from database.queries import INSERT_RECORDS_QUERY, INSERT_STATION_QUERY, STATION_ID_QUERY, STATS_QUERY

MISSING_VALUES = '-9999'

class DataLoader:
    def __init__(self):
        load_dotenv()
        self.db_params = {
            'dbname': os.getenv("DB_NAME"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT")
        }
        self.generate_log_file_for_ingestion()

    def generate_log_file_for_ingestion(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='generate_ingestion_logs.log'
        )

    def connect_to_db(self):
        return psycopg2.connect(**self.db_params)

    def load_data_from_files(self, folder_path: str = 'data/wx_data'):
        start_time = datetime.now()
        file_list = os.listdir(folder_path)
        with self.connect_to_db() as connection:
            cursor = connection.cursor()
            for file_name in file_list:
                if file_name.endswith('.txt'):
                    self.process_file(cursor, folder_path, file_name)
            connection.commit()

        end_time = datetime.now()
        logging.info(f'Data loading process start time :: {start_time} and end time :: {end_time}')

    def process_file(self, cursor, folder_path, file_name):
        file_path = Path(folder_path) / file_name
        station_name = file_path.stem

        station_id = self.insert_station(cursor, station_name)
        records = self.read_file(file_path, station_id)
        self.insert_records(cursor, records)
    
    def insert_station(self, cursor, station_name: str) -> int:
        cursor.execute(INSERT_STATION_QUERY, (station_name,))
        station_id = cursor.fetchone()
        
        if not station_id:
            cursor.execute(STATION_ID_QUERY, (station_name,))
            station_id = cursor.fetchone()
        
        return station_id[0]

    def read_file(self, file_path: Path, station_id: int) -> list:
        records = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split('\t')
                if MISSING_VALUES not in data:
                    date = datetime.strptime(data[0], '%Y%m%d').date()
                    record = [date] + [int(cell) for cell in data[1:]] + [station_id]
                    records.append(record)
        return records

    def insert_records(self, cursor, records: list):
        for record in records:
            cursor.execute(INSERT_RECORDS_QUERY, record)

    def calculate_statistics(self):
        try:
            with self.connect_to_db() as connection:
                cursor = connection.cursor()
                stats_query = STATS_QUERY
                cursor.execute(stats_query)
                connection.commit()
        except Exception as e:
            logging.error(f"Error occured while calculating statistics: {e}")
