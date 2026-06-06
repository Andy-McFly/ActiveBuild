import sys
from flask import Blueprint, jsonify, request
from pathlib import Path
import json
import uuid
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix='/api')

def get_data_file():
    base = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent
    return base / 'data' / 'data.json'

def read_data():
    with open(get_data_file(), 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(get_data_file(), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@games_bp.route('/games', methods=['GET'])
def get_games():
    data = read_data()
    return jsonify(data['games'])

@games_bp.route('/games', methods=['POST'])
def add_game():
    data = read_data()
    body = request.get_json()
    game = {
        'id': str(uuid.uuid4()),
        'name': body.get('name', ''),
        'cover_url': body.get('cover_url', ''),
        'genres': body.get('genres', []),
        'hltb_id': body.get('hltb_id', None),
        'platform': body.get('platform', ''),
        'role': body.get('role', None),
        'status': body.get('status', 'backlog'),
        'added_date': str(date.today())
    }
    data['games'].append(game)
    write_data(data)
    return jsonify(game), 201

@games_bp.route('/games/<game_id>', methods=['PUT'])
def update_game(game_id):
    data = read_data()
    game = next((g for g in data['games'] if g['id'] == game_id), None)
    if not game:
        return jsonify({'error': 'Juego no encontrado'}), 404
    allowed = {'name', 'cover_url', 'genres', 'hltb_id', 'platform', 'role', 'status'}
    body = request.get_json()
    for key, value in body.items():
        if key in allowed:
            game[key] = value
    write_data(data)
    return jsonify(game)

@games_bp.route('/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    data = read_data()
    game = next((g for g in data['games'] if g['id'] == game_id), None)
    if not game:
        return jsonify({'error': 'Juego no encontrado'}), 404
    data['games'] = [g for g in data['games'] if g['id'] != game_id]
    data['sessions'] = [s for s in data['sessions'] if s['game_id'] != game_id]
    write_data(data)
    return jsonify({'ok': True})

@games_bp.route('/games/<game_id>/play', methods=['POST'])
def play_game(game_id):
    data = read_data()
    game = next((g for g in data['games'] if g['id'] == game_id), None)
    if not game:
        return jsonify({'error': 'Juego no encontrado'}), 404
    today = str(date.today())
    already_played = any(
        s['game_id'] == game_id and s['date'] == today
        for s in data['sessions']
    )
    if already_played:
        return jsonify({'ok': True, 'message': 'Ya registrado hoy'})
    session = {
        'id': str(uuid.uuid4()),
        'game_id': game_id,
        'role': game['role'],
        'date': today
    }
    data['sessions'].append(session)
    write_data(data)
    return jsonify(session), 201

@games_bp.route('/hltb', methods=['POST'])
def lookup_hltb():
    body = request.get_json()
    url = body.get('url', '')
    if not url:
        return jsonify({'error': 'URL requerida'}), 400
    from services.hltb import get_hltb_data
    result = get_hltb_data(url)
    if not result:
        return jsonify({'error': 'No se encontró el juego'}), 404
    return jsonify(result)