import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# docker-compose.ymlで定義した環境変数からDB接続情報を取得
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'app_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'app_password')
DB_NAME = os.environ.get('DB_NAME', 'app_db')

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# 起動時にテーブルを作成する処理（初期化用）
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # contactsテーブルが存在しなければ作成する
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# フロントエンドからリクエストを受け取るエンドポイント
@app.route('/api/submit', methods=['POST'])
def submit_form():
    # JavaScriptから送信されたJSONデータを取得
    data = request.get_json()

    if not data or 'name' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    name = data['name']
    message = data['message']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 【重要】プレースホルダー（%s）を使用してSQLインジェクションを防止する
        sql = "INSERT INTO contacts (name, message) VALUES (%s, %s)"
        val = (name, message)
        
        cursor.execute(sql, val)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Data saved successfully!'}), 201

    except Exception as e:
        # エラーが発生した場合は500エラーを返す
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # アプリケーション起動前にDBの初期化を実行
    init_db()
    # Dockerコンテナの外部（プロキシ等）からアクセスできるよう host='0.0.0.0' に設定
    app.run(host='0.0.0.0', port=5000)