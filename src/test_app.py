import unittest
from app import create_app
from models import WeatherRecord, WeatherStats, db
from flask import json

class WeatherAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Add sample data
            record1 = WeatherRecord(date='20230101', max_temp=250, min_temp=150, precipitation=0, weather_station_id='STATION1')
            record2 = WeatherRecord(date='20230102', max_temp=260, min_temp=160, precipitation=5, weather_station_id='STATION1')
            stat1 = WeatherStats(year=2023, weather_station_id='STATION1', avg_max_temp=25.0, avg_min_temp=15.0, total_precipitation=0.5)
            db.session.add(record1)
            db.session.add(record2)
            db.session.add(stat1)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_invalid_date_format(self):
        response = self.client.get('/api/weather?date=2023-02-31')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_invalid_year_format(self):
        response = self.client.get('/api/weather/stats?year=20A3')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_empty_response(self):
        response = self.client.get('/api/weather?date=2024-01-01')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

        response = self.client.get('/api/weather/stats?year=2024')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_valid_response(self):
        response = self.client.get('/api/weather?date=2023-01-01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['items']), 1)

        response = self.client.get('/api/weather/stats?year=2023')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['items']), 1)

    def test_pagination(self):
        response = self.client.get('/api/weather?page=1&per_page=1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 2)

        response = self.client.get('/api/weather/stats?page=1&per_page=1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)

if __name__ == '__main__':
    unittest.main()
