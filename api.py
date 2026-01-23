from price import update_depot_with_currencies

from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import pytz

import os

app = Flask(__name__)
CORS(app)

def is__allowed_time():
    cet = pytz.timezone('CET')
    now = datetime.now(cet)
    current_hour = now.hour

    print(current_hour)

    if 6 <= current_hour < 22:
        return True
    return False

@app.route('/api/depot', methods=['GET'])
def get_depot():
    DATA_DIR = os.getenv('DATA_PATH', 'data')
    try:
        if is__allowed_time():
            update_depot_with_currencies()
        else:
            print("outside of timeframe. skipping :(")
    except Exception as e:
        print(e)
    finally:
        try:
            dir = f'{DATA_DIR}/current_depot.csv'
            df = pd.read_csv(dir).dropna()
            
            data = df.to_dict(orient='records')
            
            return data
            
        except FileNotFoundError:
            return jsonify({"status": "error", "message": "Depot file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)