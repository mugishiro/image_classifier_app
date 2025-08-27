import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json

class ImageClassifier:
    def __init__(self):
        # ResNet18モデルを読み込み
        self.model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.model.eval()

        # 画像の前処理
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        # ImageNetクラス名を読み込み
        self.classes = self.load_imagenet_classes()

    def load_imagenet_classes(self):
        # torchvisionの標準的なImageNetクラス名を使用
        from torchvision.models.resnet import ResNet18_Weights
        weights = ResNet18_Weights.IMAGENET1K_V1
        return weights.meta["categories"]

    def predict(self, image_path):
        """画像を分類する"""
        try:
            # 画像を読み込み
            image = Image.open(image_path).convert('RGB')

            # 前処理
            image_tensor = self.transform(image).unsqueeze(0)

            # 予測
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                top3_prob, top3_indices = torch.topk(probabilities, 3)

            # 結果を取得
            results = []
            for i in range(3):
                results.append({
                    'class': self.classes[top3_indices[0][i].item()],
                    'probability': top3_prob[0][i].item()
                })

            return results

        except Exception as e:
            print(f"エラー: {e}")
            return None

# テスト用
if __name__ == "__main__":
    classifier = ImageClassifier()
    print("画像分類器が初期化されました")
    print(f"利用可能なクラス数: {len(classifier.classes)}")
