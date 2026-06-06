import sys
from flask import Blueprint, jsonify, request
from pathlib import Path
import json

settings_bp = Blueprint('settings', __name__, url_prefix='/api')

def get_data_file():
    base = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent
    return base / 'data' / 'data.json'

def read_data():
    with open(get_data_file(), 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(get_data_file(), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@settings_bp.route('/settings', methods=['GET'])
def get_settings():
    data = read_data()
    return jsonify(data['settings'])

@settings_bp.route('/settings', methods=['PUT'])
def update_settings():
    data = read_data()
    body = request.get_json()
    allowed = {'theme', 'language', 'week_start'}
    for key, value in body.items():
        if key in allowed:
            data['settings'][key] = value
    write_data(data)
    return jsonify(data['settings'])