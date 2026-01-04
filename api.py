from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/depot', methods=['GET'])
def get_depot():
    DATA_DIR = os.getenv('DATA_PATH', 'data')
    try:
        dir = f'{DATA_DIR}/current_depot.csv'
        print(dir)
        df = pd.read_csv(dir).dropna()
        
        data = df.to_dict(orient='records')
        
        return data
        
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "Depot file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)