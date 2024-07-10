import os
import logging
from datetime import datetime
from app import create_app
from models import WeatherRecord, db
from sqlalchemy import func

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data_from_files(directory):
    start_time = datetime.now()
    logger.info(f"Data loading started at {start_time}")
    
    record_count = 0

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            weather_station_id = os.path.splitext(filename)[0]  # Extract the weather station ID from the filename
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                for line in file:
                    columns = line.strip().split('\t')
                    date = columns[0]
                    max_temp = int(columns[1]) if columns[1] != '-9999' else None
                    min_temp = int(columns[2]) if columns[2] != '-9999' else None
                    precipitation = int(columns[3]) if columns[3] != '-9999' else None

                    # Check for duplicates based on all columns
                    # existing_record = WeatherRecord.query.filter_by(
                    #     date=date,
                    #     max_temp=max_temp,
                    #     min_temp=min_temp,
                    #     precipitation=precipitation,
                    #     weather_station_id=weather_station_id
                    # ).first()
                    # if existing_record:
                    #     logger.info(f"Duplicate found: {existing_record}")
                    #     continue

                    weather_record = WeatherRecord(
                        date=date,
                        max_temp=max_temp,
                        min_temp=min_temp,
                        precipitation=precipitation,
                        weather_station_id=weather_station_id,
                        ingestion_timestamp=datetime.utcnow()
                    )
                    db.session.add(weather_record)
                    record_count += 1
            db.session.commit()

    end_time = datetime.now()
    logger.info(f"Data loading finished at {end_time}")
    logger.info(f"Number of records ingested: {record_count}")
    logger.info(f"Total time taken: {end_time - start_time}")

def remove_duplicates():
    start_time = datetime.now()
    logger.info(f"Duplicate removal started at {start_time}")
    
    subquery = db.session.query(
        WeatherRecord.date,
        WeatherRecord.max_temp,
        WeatherRecord.min_temp,
        WeatherRecord.precipitation,
        WeatherRecord.weather_station_id,
        func.max(WeatherRecord.ingestion_timestamp).label('max_ingestion_timestamp')
    ).group_by(
        WeatherRecord.date,
        WeatherRecord.max_temp,
        WeatherRecord.min_temp,
        WeatherRecord.precipitation,
        WeatherRecord.weather_station_id
    ).subquery()

    duplicates = db.session.query(WeatherRecord).join(
        subquery,
        (WeatherRecord.date == subquery.c.date) &
        (WeatherRecord.max_temp == subquery.c.max_temp) &
        (WeatherRecord.min_temp == subquery.c.min_temp) &
        (WeatherRecord.precipitation == subquery.c.precipitation) &
        (WeatherRecord.weather_station_id == subquery.c.weather_station_id) &
        (WeatherRecord.ingestion_timestamp != subquery.c.max_ingestion_timestamp)
    ).all()

    duplicate_count = len(duplicates)
    for record in duplicates:
        db.session.delete(record)

    db.session.commit()

    end_time = datetime.now()
    logger.info(f"Duplicate removal finished at {end_time}")
    logger.info(f"Number of duplicate records deleted: {duplicate_count}")
    logger.info(f"Total time taken: {end_time - start_time}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        load_data_from_files('wx_data')
        remove_duplicates()
