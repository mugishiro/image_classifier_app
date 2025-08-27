from flask import Flask, request, jsonify, render_template
import os
import sys
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB制限

# 画像分類器を初期化（エラーハンドリング付き）
try:
    from image_classifier_simple import ImageClassifierSimple
    classifier = ImageClassifierSimple()
    print("画像分類器の初期化が完了しました")
except Exception as e:
    print(f"画像分類器の初期化エラー: {e}")
    classifier = None

# アップロードフォルダの作成
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """ヘルスチェック用エンドポイント"""
    try:
        if classifier is None:
            return jsonify({
                'status': 'unhealthy',
                'message': 'Image classifier not initialized'
            }), 500
        
        return jsonify({
            'status': 'healthy',
            'message': 'Image Classifier App is running'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Health check failed: {str(e)}'
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if classifier is None:
            return jsonify({
                'success': False,
                'error': '画像分類器が初期化されていません'
            }), 500

        # ファイルが存在するかチェック
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': '画像ファイルが選択されていません'})

        file = request.files['image']

        # ファイル名が空でないかチェック
        if file.filename == '':
            return jsonify({'success': False, 'error': 'ファイルが選択されていません'})

        # ファイル形式をチェック
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'success': False, 'error': '対応していないファイル形式です'})

        # ファイルを保存
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 画像分類を実行
        predictions = classifier.predict(filepath)

        # 一時ファイルを削除
        os.remove(filepath)

        if predictions:
            return jsonify({
                'success': True,
                'predictions': predictions
            })
        else:
            return jsonify({
                'success': False,
                'error': '予測に失敗しました'
            })

    except Exception as e:
        print(f"エラー: {e}")
        return jsonify({
            'success': False,
            'error': f'予測に失敗しました: {str(e)}'
        })

if __name__ == '__main__':
    print("画像分類アプリを起動中...")
    print("ブラウザで http://localhost:5000 にアクセスしてください")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
