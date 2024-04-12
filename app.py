from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import csv
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

class CSVData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    new_sensor_data = SensorData(equipment_id=data['equipmentId'], timestamp=data['timestamp'], value=data['value'])
    db.session.add(new_sensor_data)
    db.session.commit()
    return jsonify({'message': 'Data received and stored successfully'}), 200

@app.route('/csv-data', methods=['POST'])
def receive_csv_data():
    file = request.files['file']
    content = file.stream.read().decode('utf-8')
    csv_data = csv.reader(StringIO(content))
    for row in csv_data:
        equipment_id, timestamp_str, value_str = row
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        value = float(value_str)
        new_csv_data = CSVData(equipment_id=equipment_id, timestamp=timestamp, value=value)
        db.session.add(new_csv_data)
    db.session.commit()
    return jsonify({'message': 'CSV data received and stored successfully'}), 200

@app.route('/')
def index():
    last_24_hours_data = get_average_sensor_data(datetime.utcnow() - timedelta(days=1))
    last_48_hours_data = get_average_sensor_data(datetime.utcnow() - timedelta(days=2))
    last_week_data = get_average_sensor_data(datetime.utcnow() - timedelta(weeks=1))
    last_month_data = get_average_sensor_data(datetime.utcnow() - timedelta(weeks=4))
    return render_template('index.html', 
                           last_24_hours_data=last_24_hours_data, 
                           last_48_hours_data=last_48_hours_data, 
                           last_week_data=last_week_data, 
                           last_month_data=last_month_data)

def get_average_sensor_data(start_date):
    end_date = datetime.utcnow()
    query = db.session.query(SensorData.equipment_id, func.avg(SensorData.value).label('average_value')) \
                      .filter(SensorData.timestamp >= start_date, SensorData.timestamp <= end_date) \
                      .group_by(SensorData.equipment_id) \
                      .order_by(desc('average_value'))
    return query.all()

if __name__ == '__main__':
    app.run(debug=True)
