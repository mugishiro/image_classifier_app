# 軽量版Dockerfile for Railway
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを最小限に更新
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピー
COPY requirements.txt .

# PyTorch CPU版をインストール（軽量版）
RUN pip install --no-cache-dir torch==2.8.0+cpu torchvision==0.23.0+cpu torchaudio==2.8.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# その他の依存関係をインストール
RUN pip install --no-cache-dir flask==3.1.1 pillow==9.0.1 numpy==2.2.6 gunicorn==21.2.0

# アプリケーションファイルをコピー
COPY . .

# ポートを公開
EXPOSE 5000

# 環境変数を設定
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# アプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
