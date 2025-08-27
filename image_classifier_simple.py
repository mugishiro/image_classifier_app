import numpy as np
from PIL import Image
import os

class ImageClassifierSimple:
    def __init__(self):
        self.classes = self.load_imagenet_classes()
        self.transform = self.get_transform()

    def get_transform(self):
        """画像前処理の設定"""
        def transform(image):
            # 画像をリサイズ
            image = image.resize((224, 224))
            # PIL画像をnumpy配列に変換
            image_array = np.array(image)
            # 正規化
            image_array = image_array.astype(np.float32) / 255.0
            return image_array
        return transform

    def load_imagenet_classes(self):
        """ImageNetクラス名の読み込み"""
        # 簡易版のクラス名（実際のImageNet 1000クラスの一部）
        classes = [
            "golden retriever", "Labrador retriever", "German shepherd",
            "cat", "dog", "bird", "car", "truck", "bicycle",
            "person", "building", "tree", "flower", "food",
            "computer", "phone", "book", "chair", "table"
        ]
        return classes

    def predict(self, image_path):
        """画像を分類"""
        try:
            # 画像を読み込み
            image = Image.open(image_path).convert('RGB')

            # 画像を前処理
            input_array = self.transform(image)

            # 簡易版の予測
            predictions = self.simple_predict(input_array)

            return predictions

        except Exception as e:
            print(f"予測エラー: {e}")
            return []

    def simple_predict(self, input_array):
        """簡易版の予測（画像の特徴に基づく分類）"""
        try:
            # 画像の特徴を計算
            mean_value = np.mean(input_array)
            std_value = np.std(input_array)

            # RGB各チャンネルの平均値
            if len(input_array.shape) == 3:
                r_mean = np.mean(input_array[:, :, 0])
                g_mean = np.mean(input_array[:, :, 1])
                b_mean = np.mean(input_array[:, :, 2])
            else:
                r_mean = g_mean = b_mean = mean_value

            # 簡易的な分類ロジック
            if mean_value > 0.6 and r_mean > 0.5:
                predictions = [
                    {"class": "golden retriever", "probability": 0.85},
                    {"class": "Labrador retriever", "probability": 0.12},
                    {"class": "German shepherd", "probability": 0.03}
                ]
            elif mean_value > 0.4 and g_mean > 0.4:
                predictions = [
                    {"class": "cat", "probability": 0.78},
                    {"class": "dog", "probability": 0.15},
                    {"class": "bird", "probability": 0.07}
                ]
            elif std_value > 0.2:
                predictions = [
                    {"class": "building", "probability": 0.65},
                    {"class": "tree", "probability": 0.25},
                    {"class": "person", "probability": 0.10}
                ]
            else:
                predictions = [
                    {"class": "computer", "probability": 0.70},
                    {"class": "phone", "probability": 0.20},
                    {"class": "book", "probability": 0.10}
                ]

            return predictions

        except Exception as e:
            print(f"予測処理エラー: {e}")
            # デフォルトの予測結果
            return [
                {"class": "unknown", "probability": 1.0}
            ]
