from flask import request, jsonify
from flask_restful import Resource
from flasgger import swag_from
from models import WeatherRecord, WeatherStats
from app import db
from datetime import datetime

# Pagination function to paginate query results
def paginate(query, page, per_page):
    total = query.count()
    items = query.paginate(page, per_page, False).items
    return {
        'total': total,
        'page': page,
        'per_page': per_page,
        'items': [item.to_dict() for item in items]
    }

class WeatherResource(Resource):
    """
    Resource for fetching weather records.
    """
    @swag_from({
        'tags': ['weather'],
        'description': 'Get weather records',
        'parameters': [
            {
                'name': 'page',
                'description': 'Page number',
                'in': 'query',
                'type': 'integer',
                'required': False
            },
            {
                'name': 'per_page',
                'description': 'Number of records per page',
                'in': 'query',
                'type': 'integer',
                'required': False
            },
            {
                'name': 'date',
                'description': 'Filter by date (format: YYYY-MM-DD)',
                'in': 'query',
                'type': 'string',
                'required': False,
                'format': 'date'
            },
            {
                'name': 'station_id',
                'description': 'Filter by station ID',
                'in': 'query',
                'type': 'string',
                'required': False
            }
        ],
        'responses': {
            '200': {
                'description': 'Weather records',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'date': {'type': 'string'},
                            'max_temp': {'type': 'integer'},
                            'min_temp': {'type': 'integer'},
                            'precipitation': {'type': 'integer'},
                            'weather_station_id': {'type': 'string'},
                            'ingestion_timestamp': {'type': 'string'}
                        }
                    }
                }
            },
            '400': {
                'description': 'Invalid date format or illogical date'
            },
            '404': {
                'description': 'No records matching this criteria found'
            }
        }
    })
    def get(self):
        """
        GET method to fetch weather records with optional filters for date and station ID.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        date = request.args.get('date', type=str)
        station_id = request.args.get('station_id', type=str)

        query = WeatherRecord.query
        if date:
            try:
                # Validate and convert the date from YYYY-MM-DD to YYYYMMDD format
                datetime.strptime(date, '%Y-%m-%d')
                date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
            except ValueError:
                return {"error": "Invalid date format or illogical date. Use YYYY-MM-DD format."}, 400
            
            query = query.filter(WeatherRecord.date == date)
        if station_id:
            query = query.filter(WeatherRecord.weather_station_id == station_id)

        result = paginate(query, page, per_page)
        if not result['items']:
            return {"error": "No records matching this criteria found"}, 404
        return result

class WeatherStatsResource(Resource):
    """
    Resource for fetching weather statistics.
    """
    @swag_from({
        'tags': ['weather_stats'],
        'description': 'Get weather statistics',
        'parameters': [
            {
                'name': 'page',
                'description': 'Page number',
                'in': 'query',
                'type': 'integer',
                'required': False
            },
            {
                'name': 'per_page',
                'description': 'Number of records per page',
                'in': 'query',
                'type': 'integer',
                'required': False
            },
            {
                'name': 'year',
                'description': 'Filter by year (format: YYYY)',
                'in': 'query',
                'type': 'integer',
                'required': False
            },
            {
                'name': 'station_id',
                'description': 'Filter by station ID',
                'in': 'query',
                'type': 'string',
                'required': False
            }
        ],
        'responses': {
            '200': {
                'description': 'Weather statistics',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'year': {'type': 'integer'},
                            'weather_station_id': {'type': 'string'},
                            'avg_max_temp': {'type': 'number'},
                            'avg_min_temp': {'type': 'number'},
                            'total_precipitation': {'type': 'number'}
                        }
                    }
                }
            },
            '400': {
                'description': 'Invalid year format'
            },
            '404': {
                'description': 'No records matching this criteria found'
            }
        }
    })
    def get(self):
        """
        GET method to fetch weather statistics with optional filters for year and station ID.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        year = request.args.get('year', type=str)
        station_id = request.args.get('station_id', type=str)

        query = WeatherStats.query
        if year:
            try:
                # Validate the year format
                if len(year) != 4 or not year.isdigit():
                    raise ValueError("Invalid year format")
            except ValueError:
                return {"error": "Invalid year format. Use YYYY format."}, 400
            
            query = query.filter(WeatherStats.year == int(year))
        if station_id:
            query = query.filter(WeatherStats.weather_station_id == station_id)

        result = paginate(query, page, per_page)
        if not result['items']:
            return {"error": "No records matching this criteria found"}, 404
        return result
