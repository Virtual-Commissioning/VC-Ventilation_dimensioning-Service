from app import app
from flask import request
from app.services import to_varmenet_service

@app.route('/')
@app.route('/to_varmenet_converter', methods=['POST'])
def to_varmenet_converter():
    data = request.get_data()
    converted_xml_varmenet_format = to_varmenet_service.to_varmenet_xml_converter(data)
    return converted_xml_varmenet_format