import sys
import os
import threading
import time
import webview
from flask import Flask, render_template, send_from_directory
from pathlib import Path
import json

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative
    return Path(__file__).parent / relative

def data_path(relative):
    base = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
    return base / relative

app = Flask(
    __name__,
    template_folder=str(resource_path('templates')),
    static_folder=str(resource_path('static'))
)

DATA_DIR = data_path('data')
DATA_FILE = DATA_DIR / 'data.json'

DEFAULT_DATA = {
    "settings": {
        "theme": "standard",
        "language": "es",
        "week_start": "monday"
    },
    "games": [],
    "sessions": []
}

def init_data():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DATA, f, indent=2, ensure_ascii=False)

from api.games import games_bp
from api.sessions import sessions_bp
from api.stats import stats_bp
from api.settings import settings_bp

app.register_blueprint(games_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(settings_bp)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    return render_template('index.html', active='home')

@app.route('/games')
def games_page():
    return render_template('games.html', active='games')

@app.route('/stats')
def stats_page():
    return render_template('stats.html', active='stats')

@app.route('/settings')
def settings_page():
    return render_template('settings.html', active='settings')

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    init_data()
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(0.5)
    icon_path = str(resource_path('logo.ico'))
    webview.create_window(
        'ActiveBuild',
        'http://127.0.0.1:5000',
        width=1100,
        height=720,
        min_size=(800, 600)
    )
    webview.start(icon=icon_path)