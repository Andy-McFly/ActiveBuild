from flask import Blueprint, jsonify, request
from pathlib import Path
from datetime import date, timedelta
import json

stats_bp = Blueprint('stats', __name__, url_prefix='/api')

DATA_FILE = Path(__file__).parent.parent / 'data' / 'data.json'

def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_week_start(settings):
    today = date.today()
    if settings.get('week_start', 'monday') == 'monday':
        return today - timedelta(days=today.weekday())
    else:
        return today - timedelta(days=(today.weekday() + 1) % 7)

@stats_bp.route('/stats/summary', methods=['GET'])
def get_summary():
    data = read_data()
    sessions = data['sessions']
    settings = data['settings']
    today = date.today()
    week_start = get_week_start(settings)
    month_start = today.replace(day=1)

    sessions_week = [
        s for s in sessions
        if date.fromisoformat(s['date']) >= week_start
    ]
    sessions_month = [
        s for s in sessions
        if date.fromisoformat(s['date']) >= month_start
    ]

    role_counts = {'principal': 0, 'secundario': 0, 'comodin': 0}
    for s in sessions_month:
        role = s.get('role')
        if role in role_counts:
            role_counts[role] += 1
    top_role = max(role_counts, key=role_counts.get) if any(role_counts.values()) else None

    return jsonify({
        'sessions_this_week': len(sessions_week),
        'sessions_this_month': len(sessions_month),
        'top_role': top_role
    })

@stats_bp.route('/stats/weekly', methods=['GET'])
def get_weekly():
    data = read_data()
    sessions = data['sessions']
    settings = data['settings']
    weeks = int(request.args.get('weeks', 8))
    today = date.today()
    week_start = get_week_start(settings)
    result = []
    for i in range(weeks - 1, -1, -1):
        w_start = week_start - timedelta(weeks=i)
        w_end = w_start + timedelta(days=6)
        days_played = len(set(
            s['date'] for s in sessions
            if w_start <= date.fromisoformat(s['date']) <= w_end
        ))
        result.append({
            'week': str(w_start),
            'days_played': days_played
        })
    return jsonify(result)

@stats_bp.route('/stats/most-played', methods=['GET'])
def get_most_played():
    data = read_data()
    sessions = data['sessions']
    games = {g['id']: g['name'] for g in data['games']}
    settings = data['settings']
    today = date.today()
    week_start = get_week_start(settings)
    month_start = today.replace(day=1)

    def top_game(session_list):
        counts = {}
        for s in session_list:
            counts[s['game_id']] = counts.get(s['game_id'], 0) + 1
        if not counts:
            return None
        top_id = max(counts, key=counts.get)
        return {'id': top_id, 'name': games.get(top_id, 'Desconocido'), 'sessions': counts[top_id]}

    return jsonify({
        'this_week': top_game([s for s in sessions if date.fromisoformat(s['date']) >= week_start]),
        'this_month': top_game([s for s in sessions if date.fromisoformat(s['date']) >= month_start])
    })

@stats_bp.route('/stats/completed', methods=['GET'])
def get_completed():
    data = read_data()
    completed = [g for g in data['games'] if g['status'] == 'completed']
    result = []
    for game in completed:
        total_sessions = len([s for s in data['sessions'] if s['game_id'] == game['id']])
        result.append({
            'id': game['id'],
            'name': game['name'],
            'platform': game['platform'],
            'cover_url': game['cover_url'],
            'total_sessions': total_sessions
        })
    return jsonify(result)