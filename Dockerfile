# 軽量版Dockerfile for Railway (ONNX Runtime版)
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを最小限に更新
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# アップロードフォルダを作成
RUN mkdir -p uploads

# ポートを公開
EXPOSE 5000

# 環境変数を設定
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# アプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
