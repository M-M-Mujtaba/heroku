from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database connection settings
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'

@app.route('/health', methods=['GET'])
def health_check():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "healthy", "time": current_time})


@app.route('/select_query', methods=['POST'])
def select_query():
    query = request.json.get('query')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall() if cur.description else []
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/test_update_delete', methods=['POST'])
def test_update_delete():
    update_delete_query = request.json.get('update_delete_query')
    validation_query = request.json.get('validation_query')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(update_delete_query)
        cur.execute(validation_query)
        result = cur.fetchall() if cur.description else []
        cur.close()
        conn.rollback()  # Rollback the transaction
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/execute_update_delete', methods=['POST'])
def execute_update_delete():
    query = request.json.get('query')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()  # Commit the transaction
        cur.close()
        conn.close()
        return jsonify({"message": "Query executed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
