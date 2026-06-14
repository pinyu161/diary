from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'diary.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS daily_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date DATE UNIQUE NOT NULL,
            weight REAL,
            breakfast TEXT,
            lunch TEXT,
            dinner TEXT,
            water_ml INTEGER DEFAULT 0,
            exercise TEXT,
            had_bowel_movement INTEGER DEFAULT 0,
            mood_emoji TEXT,
            diary TEXT,
            gratitude_1 TEXT,
            gratitude_2 TEXT,
            gratitude_3 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ── Pages ──────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record')
def record_page():
    return render_template('record.html')

@app.route('/calendar')
def calendar_page():
    return render_template('calendar.html')

@app.route('/stats')
def stats_page():
    return render_template('stats.html')

# ── API ────────────────────────────────────────────────
@app.route('/api/record', methods=['POST'])
def save_record():
    data = request.get_json()
    if not data or not data.get('record_date'):
        return jsonify({'error': '缺少日期'}), 400

    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO daily_records
                (record_date, weight, breakfast, lunch, dinner, water_ml,
                 exercise, had_bowel_movement, mood_emoji, diary,
                 gratitude_1, gratitude_2, gratitude_3)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(record_date) DO UPDATE SET
                weight=excluded.weight,
                breakfast=excluded.breakfast,
                lunch=excluded.lunch,
                dinner=excluded.dinner,
                water_ml=excluded.water_ml,
                exercise=excluded.exercise,
                had_bowel_movement=excluded.had_bowel_movement,
                mood_emoji=excluded.mood_emoji,
                diary=excluded.diary,
                gratitude_1=excluded.gratitude_1,
                gratitude_2=excluded.gratitude_2,
                gratitude_3=excluded.gratitude_3
        ''', (
            data.get('record_date'),
            data.get('weight'),
            data.get('breakfast'),
            data.get('lunch'),
            data.get('dinner'),
            data.get('water_ml', 0),
            data.get('exercise'),
            1 if data.get('had_bowel_movement') else 0,
            data.get('mood_emoji'),
            data.get('diary'),
            data.get('gratitude_1'),
            data.get('gratitude_2'),
            data.get('gratitude_3'),
        ))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/record/<date>', methods=['GET'])
def get_record(date):
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM daily_records WHERE record_date = ?', (date,)
    ).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify(None)

@app.route('/api/records/<int:year>/<int:month>', methods=['GET'])
def get_month_records(year, month):
    prefix = f'{year:04d}-{month:02d}'
    conn = get_db()
    rows = conn.execute(
        'SELECT record_date, mood_emoji, weight FROM daily_records WHERE record_date LIKE ?',
        (prefix + '%',)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/weight-history', methods=['GET'])
def weight_history():
    conn = get_db()
    rows = conn.execute(
        'SELECT record_date, weight FROM daily_records WHERE weight IS NOT NULL ORDER BY record_date ASC LIMIT 60'
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/mood-stats/<int:year>/<int:month>', methods=['GET'])
def mood_stats(year, month):
    prefix = f'{year:04d}-{month:02d}'
    conn = get_db()
    rows = conn.execute(
        'SELECT mood_emoji, COUNT(*) as cnt FROM daily_records WHERE record_date LIKE ? AND mood_emoji IS NOT NULL GROUP BY mood_emoji',
        (prefix + '%',)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/water-week', methods=['GET'])
def water_week():
    conn = get_db()
    rows = conn.execute(
        'SELECT record_date, water_ml FROM daily_records ORDER BY record_date DESC LIMIT 7'
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows][::-1])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
