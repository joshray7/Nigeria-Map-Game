import os
from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# --- Robust CSV loading (same directory as this file) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = "Nigerian_states.csv"   # <-- make sure this file exists
CSV_PATH = os.path.join(BASE_DIR, CSV_NAME)

if not os.path.isfile(CSV_PATH):
    raise FileNotFoundError(f"{CSV_NAME} not found in {BASE_DIR}. Put your CSV there.")

# load csv into DataFrame
df = pd.read_csv(CSV_PATH)

# Expect columns: state,x,y (x,y are turtle coordinates: center origin)
# Normalize names to lowercase for matching
df['state_key'] = df['state'].str.strip().str.lower()

# Build dict: key -> (x,y)
states = {row.state_key: (int(row.x), int(row.y)) for row in df.itertuples()}

# Map image dimensions (adjust if your image size differs)
MAP_WIDTH = 779
MAP_HEIGHT = 599

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/states")
def get_states():
    # return states list (converted to web coords) if you want to load all at once
    records = []
    for r in df.to_dict(orient="records"):
        x = int(r['x'])
        y = int(r['y'])
        web_x = (MAP_WIDTH / 2) + x
        web_y = (MAP_HEIGHT / 2) - y
        records.append({
            "state": r['state'],
            "x": web_x,
            "y": web_y
        })
    return jsonify(records)

@app.route("/check_answer", methods=['POST'])
def check_answer():
    data = request.get_json(force=True)
    if not data or 'state' not in data:
        return jsonify({'correct': False, 'error': 'No state provided'}), 400

    user_state = str(data['state']).strip().lower()
    if user_state in states:
        x, y = states[user_state]
        web_x = (MAP_WIDTH / 2) + x
        web_y = (MAP_HEIGHT / 2) - y
        return jsonify({
            'correct': True,
            'state': df[df['state_key'] == user_state]['state'].values[0],
            'x': web_x,
            'y': web_y
        })
    else:
        return jsonify({'correct': False})

if __name__ == "__main__":
    # debug True for development; turn off in production
    app.run(debug=True)

