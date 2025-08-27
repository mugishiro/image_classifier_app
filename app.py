from flask import Flask, render_template, request, jsonify
from image_classifier import ImageClassifier
import base64
import io
from PIL import Image
import os

app = Flask(__name__)
classifier = ImageClassifier()

# アップロードされた画像を保存するフォルダ
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """画像を分類するAPIエンドポイント"""
    try:
        # 画像データを取得
        if 'image' in request.files:
            # ファイルアップロード
            file = request.files['image']
            image = Image.open(file.stream).convert('RGB')
        else:
            # Base64エンコードされた画像
            image_data = request.json['image']
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        # 一時ファイルとして保存
        temp_path = os.path.join(UPLOAD_FOLDER, 'temp.jpg')
        image.save(temp_path)

        # 予測実行
        results = classifier.predict(temp_path)

        # 一時ファイルを削除
        os.remove(temp_path)

        if results:
            return jsonify({
                'success': True,
                'predictions': results
            })
        else:
            return jsonify({
                'success': False,
                'error': '予測に失敗しました'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("画像分類アプリを起動中...")
    print("ブラウザで http://localhost:5000 にアクセスしてください")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
