import logging
from datetime import datetime
from sqlalchemy.sql import func
from app import create_app
from models import WeatherRecord, WeatherStats, db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_statistics():
    start_time = datetime.now()
    logger.info(f"Statistics calculation started at {start_time}")
    
    records = db.session.query(
        func.substr(WeatherRecord.date, 1, 4).label('year'),
        WeatherRecord.weather_station_id,
        func.round(func.avg(WeatherRecord.max_temp / 10.0), 2).label('avg_max_temp'),
        func.round(func.avg(WeatherRecord.min_temp / 10.0), 2).label('avg_min_temp'),
        func.round(func.sum(WeatherRecord.precipitation / 100.0), 2).label('total_precipitation')
    ).group_by(
        func.substr(WeatherRecord.date, 1, 4),
        WeatherRecord.weather_station_id
    ).all()

    batch_size = 1000
    batch = []
    for record in records:
        year = int(record.year)
        station = record.weather_station_id
        avg_max_temp = record.avg_max_temp
        avg_min_temp = record.avg_min_temp
        total_precipitation = record.total_precipitation


        weather_stat = WeatherStats(
            year=year,
            weather_station_id=station,
            avg_max_temp=avg_max_temp,
            avg_min_temp=avg_min_temp,
            total_precipitation=total_precipitation
        )
        batch.append(weather_stat)
        
        if len(batch) >= batch_size:
            db.session.bulk_save_objects(batch)
            db.session.commit()
            batch = []

    if batch:
        db.session.bulk_save_objects(batch)
        db.session.commit()

    end_time = datetime.now()
    logger.info(f"Statistics calculation finished at {end_time}")
    logger.info(f"Total time taken: {end_time - start_time}")

def remove_duplicates():
    start_time = datetime.now()
    logger.info(f"Duplicate removal started at {start_time}")
    
    subquery = db.session.query(
        WeatherStats.year,
        WeatherStats.weather_station_id,
        WeatherStats.avg_max_temp,
        WeatherStats.avg_min_temp,
        WeatherStats.total_precipitation,
        func.max(WeatherStats.id).label('max_id')
    ).group_by(
        WeatherStats.year,
        WeatherStats.weather_station_id,
        WeatherStats.avg_max_temp,
        WeatherStats.avg_min_temp,
        WeatherStats.total_precipitation
    ).subquery()

    duplicates = db.session.query(WeatherStats).join(
        subquery,
        (WeatherStats.year == subquery.c.year) &
        (WeatherStats.weather_station_id == subquery.c.weather_station_id) &
        (WeatherStats.avg_max_temp == subquery.c.avg_max_temp) &
        (WeatherStats.avg_min_temp == subquery.c.avg_min_temp) &
        (WeatherStats.total_precipitation == subquery.c.total_precipitation) &
        (WeatherStats.id != subquery.c.max_id)
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
        calculate_statistics()
        remove_duplicates()
