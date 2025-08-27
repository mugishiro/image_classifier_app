# PyTorch画像分類アプリ

PyTorchとFlaskを使用した画像分類Webアプリケーションです。ResNet-18モデルを使用してImageNetの1000クラスを分類できます。

## 機能

- 🖼️ 画像のドラッグ&ドロップアップロード
- 🎯 リアルタイム画像分類
- 📊 上位3位までの予測結果表示
- 📱 レスポンシブデザイン
- ⚡ 高速処理（1-3秒）

## 技術スタック

- **バックエンド**: Python 3.8+, Flask, PyTorch
- **フロントエンド**: HTML5, CSS3, JavaScript
- **AIモデル**: ResNet-18 (ImageNet事前学習済み)
- **画像処理**: PIL (Pillow)

## インストール

1. リポジトリをクローン
```bash
git clone <repository-url>
cd image_classifier_app
```

2. 必要なライブラリをインストール
```bash
pip3 install torch torchvision torchaudio flask pillow numpy
```

## 使用方法

1. アプリケーションを起動
```bash
python3 app.py
```

2. ブラウザでアクセス
```
http://localhost:5000
```

3. 画像をアップロードして分類結果を確認

## プロジェクト構造

```
image_classifier_app/
├── app.py                 # Flask Webアプリケーション
├── image_classifier.py    # 画像分類クラス
├── templates/
│   └── index.html        # メインHTMLテンプレート
├── uploads/              # アップロード画像保存用
└── README.md            # このファイル
```

## API仕様

### POST /predict

画像を分類するAPIエンドポイント

**リクエスト**:
- Content-Type: multipart/form-data
- Body: image (画像ファイル)

**レスポンス**:
```json
{
  "success": true,
  "predictions": [
    {
      "class": "golden retriever",
      "probability": 0.852
    },
    {
      "class": "Labrador retriever",
      "probability": 0.121
    },
    {
      "class": "tennis ball",
      "probability": 0.027
    }
  ]
}
```

## 対応画像形式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## 制限事項

- 最大ファイルサイズ: 10MB
- 対応クラス数: 1000 (ImageNet)
- 処理時間: 1-3秒

## トラブルシューティング

### よくある問題

1. **PyTorchのインストールエラー**
   ```bash
   # CPU版をインストール
   pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

2. **ポート5000が使用中**
   ```bash
   # 別のポートで起動
   python3 app.py --port 5001
   ```

3. **メモリ不足エラー**
   - 画像サイズを小さくする
   - 他のアプリケーションを終了する

## 今後の改善予定

- [ ] カスタムモデルのサポート
- [ ] バッチ処理機能
- [ ] リアルタイムカメラ機能
- [ ] 多言語対応
- [ ] 結果の保存機能

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します！
