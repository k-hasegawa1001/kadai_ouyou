# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 必要なパッケージリスト（requirements.txt）をコピーしてインストール
# ※ 同じディレクトリに requirements.txt (Flask, mysql-connector-python等を記載) を作成してください
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコンテナ内にコピー
COPY . .

# コンテナ起動時に実行するコマンド（例としてFlaskの起動）
# 本番環境に近い形にするなら gunicorn などの使用も検討します
CMD ["python", "app.py"]