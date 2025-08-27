# マルチステージビルドでサイズを削減
FROM python:3.10-slim as builder

# ビルド依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txtをコピー
COPY requirements.txt .

# PyTorch CPU版をインストール（軽量版）
RUN pip install --no-cache-dir torch==2.8.0+cpu torchvision==0.23.0+cpu torchaudio==2.8.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# その他の依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# 本番用イメージ
FROM python:3.10-slim

# 必要なシステムライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ビルドしたPythonパッケージをコピー
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# アプリケーションファイルをコピー
COPY . .

# ポートを公開
EXPOSE 5000

# 環境変数を設定
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# アプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
