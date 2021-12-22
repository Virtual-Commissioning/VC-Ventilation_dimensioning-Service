from app import app
from flask import request
from app.services import rule_checker

@app.route('/')
@app.route('/hvac-rule-checker', methods=['POST'])
def check_system_integrity():
    data = request.get_data()
    status_json = rule_checker.rule_checker(data)
    return status_json