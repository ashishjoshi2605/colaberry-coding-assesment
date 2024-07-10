from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class WeatherRecord(db.Model):
    """
    Model representing a weather record.
    """
    # Define columns for the weather_record table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    date = db.Column(db.String(8), nullable=False, index=True)  # Date in YYYYMMDD format
    max_temp = db.Column(db.Integer, nullable=True)  # Maximum temperature in tenths of degrees Celsius
    min_temp = db.Column(db.Integer, nullable=True)  # Minimum temperature in tenths of degrees Celsius
    precipitation = db.Column(db.Integer, nullable=True)  # Precipitation in tenths of millimeters
    weather_station_id = db.Column(db.String, nullable=False, index=True)  # Weather station ID
    ingestion_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of data ingestion

    # Define a composite index on date and weather_station_id for fast lookup
    __table_args__ = (
        db.Index('idx_date_station', 'date', 'weather_station_id'),
    )

    def to_dict(self):
        """
        Convert the WeatherRecord instance to a dictionary.
        """
        return {
            'id': self.id,
            'date': self.date,
            'max_temp': self.max_temp,
            'min_temp': self.min_temp,
            'precipitation': self.precipitation,
            'weather_station_id': self.weather_station_id,
            'ingestion_timestamp': self.ingestion_timestamp.isoformat()
        }

    def __repr__(self):
        """
        String representation of the WeatherRecord instance.
        """
        return f'<WeatherRecord {self.date} {self.weather_station_id}>'

class WeatherStats(db.Model):
    """
    Model representing weather statistics for a specific year and weather station.
    """
    # Define columns for the weather_stats table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    year = db.Column(db.Integer, nullable=False, index=True)  # Year
    weather_station_id = db.Column(db.String, nullable=False, index=True)  # Weather station ID
    avg_max_temp = db.Column(db.Float, nullable=True)  # Average maximum temperature in degrees Celsius
    avg_min_temp = db.Column(db.Float, nullable=True)  # Average minimum temperature in degrees Celsius
    total_precipitation = db.Column(db.Float, nullable=True)  # Total precipitation in centimeters

    # Define a composite index on year and weather_station_id for fast lookup
    __table_args__ = (
        db.Index('idx_year_station', 'year', 'weather_station_id'),
    )

    def to_dict(self):
        """
        Convert the WeatherStats instance to a dictionary.
        """
        return {
            'id': self.id,
            'year': self.year,
            'weather_station_id': self.weather_station_id,
            'avg_max_temp': self.avg_max_temp,
            'avg_min_temp': self.avg_min_temp,
            'total_precipitation': self.total_precipitation
        }

    def __repr__(self):
        """
        String representation of the WeatherStats instance.
        """
        return f'<WeatherStats {self.year} {self.weather_station_id}>'
