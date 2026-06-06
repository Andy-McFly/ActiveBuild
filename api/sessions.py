from flask import Blueprint, jsonify
from pathlib import Path
import json

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api')

DATA_FILE = Path(__file__).parent.parent / 'data' / 'data.json'

def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@sessions_bp.route('/sessions', methods=['GET'])
def get_sessions():
    data = read_data()
    return jsonify(data['sessions'])

@sessions_bp.route('/sessions/<game_id>', methods=['GET'])
def get_sessions_by_game(game_id):
    data = read_data()
    sessions = [s for s in data['sessions'] if s['game_id'] == game_id]
    return jsonify(sessions)

@sessions_bp.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    data = read_data()
    session = next((s for s in data['sessions'] if s['id'] == session_id), None)
    if not session:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    data['sessions'] = [s for s in data['sessions'] if s['id'] != session_id]
    write_data(data)
    return jsonify({'ok': True})