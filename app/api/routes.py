from app import app
from flask import request
from app.services import airflow_determinator

@app.route('/')
@app.route('/calculate_ventilation_demand', methods=['POST'])
def calculate_ventilation_demand():
    data = request.get_data()
    ventilation_demand_as_json = airflow_determinator.airflow_determinator(data)
    return ventilation_demand_as_json