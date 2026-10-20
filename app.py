from flask import Flask, render_template_string, request, redirect, url_for
from database import init_db, add_session, get_all_sessions, update_session, delete_session
from streak import calculate_streaks, get_current_week_totals
from datetime import datetime

app = Flask(__name__)
init_db()

# Embedded HTML template so you don't need a separate file or folder!
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study & Streak Tracker</title>
    <style>
        :root { background-color: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
        body { max-width: 900px; margin: 40px auto; padding: 0 20px; }
        h1, h2 { color: #38bdf8; }
        .card-container { display: flex; gap: 20px; margin-bottom: 30px; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; flex: 1; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border: 1px solid #334155; text-align: center; }
        .card h3 { margin: 0 0 10px 0; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; }
        .card .val { font-size: 2rem; font-weight: bold; color: #f43f5e; }
        form { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 30px; display: grid; grid-template-columns: 2fr 1fr 1.5fr 1fr; gap: 15px; align-items: end; }
        .form-group { display: flex; flex-direction: column; }
        label { font-size: 0.85rem; margin-bottom: 5px; color: #94a3b8; }
        input, button { padding: 10px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 1rem; }
        button { background: #0284c7; border: none; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #0369a1; }
        table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; border: 1px solid #334155; }
        th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #334155; }
        th { background: #334155; color: #e2e8f0; font-size: 0.9rem; }
        tr:last-child td { border-bottom: none; }
        .btn-delete { color: #f43f5e; text-decoration: none; font-weight: bold; }
        .btn-delete:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Study & Streak Tracker</h1>

    <div class="card-container">
        <div class="card">
            <h3>Current Streak</h3>
            <div class="val">{{ current_streak }} Days 🔥</div>
        </div>
        <div class="card">
            <h3>Longest Streak</h3>
            <div class="val" style="color: #38bdf8;">{{ longest_streak }} Days ⚡</div>
        </div>
    </div>

    <h2>Log Study Session</h2>
    <form action="/add" method="POST">
        <div class="form-group">
            <label for="subject">Subject</label>
            <input type="text" id="subject" name="subject" required placeholder="e.g. Mathematics">
        </div>
        <div class="form-group">
            <label for="duration">Duration (mins)</label>
            <input type="number" id="duration" name="duration" required placeholder="60">
        </div>
        <div class="form-group">
            <label for="date">Date</label>
            <input type="date" id="date" name="date">
        </div>
        <button type="submit">Log Session</button>
    </form>

    <h2>Current Week Totals per Subject</h2>
    <div style="background: #1e293b; padding: 15px 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 30px;">
        {% if weekly_totals %}
            <ul>
            {% for subject, mins in weekly_totals.items() %}
                <li><strong>{{ subject }}</strong>: {{ mins }} minutes</li>
            {% endfor %}
            </ul>
        {% else %}
            <p style="color: #94a3b8; margin: 0;">No study sessions logged for this week yet.</p>
        {% endif %}
    </div>

    <h2>Past Sessions</h2>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Subject</th>
                <th>Duration (Minutes)</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for sess in sessions %}
            <tr>
                <td>{{ sess[3] }}</td>
                <td>{{ sess[1] }}</td>
                <td>{{ sess[2] }} mins</td>
                <td><a href="/delete/{{ sess[0] }}" class="btn-delete">Delete</a></td>
            </tr>
            {% else %}
            <tr>
                <td colspan="4" style="text-align: center; color: #94a3b8;">No sessions recorded yet. Start studying!</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    sessions = get_all_sessions()
    session_dates = [row[3] for row in sessions]
    current_streak, longest_streak = calculate_streaks(session_dates)
    weekly_totals = get_current_week_totals(sessions)
    
    return render_template_string(HTML_TEMPLATE, 
                                  sessions=sessions, 
                                  current_streak=current_streak, 
                                  longest_streak=longest_streak,
                                  weekly_totals=weekly_totals)

@app.route('/add', methods=['POST'])
def add():
    subject = request.form.get('subject')
    duration = int(request.form.get('duration'))
    date_str = request.form.get('date') or datetime.now().strftime("%Y-%m-%d")
    
    add_session(subject, duration, date_str)
    return redirect(url_for('index'))

@app.route('/delete/<int:session_id>')
def delete(session_id):
    delete_session(session_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)