# 📘 Study Tracker（学習習慣記録アプリ）

Flaskで作成した、学習習慣を記録・可視化できるWebアプリケーションです。

## 🚀 主な機能

- 📝 学習記録の登録（教科・時間・日付・メモ）
- 📊 学習時間のグラフ可視化（日別）
- ⬇️ 学習記録のCSVダウンロード
- 🗑 学習記録の削除機能
- 💄 Bootstrapによるレスポンシブ対応UI

## 🛠 使用技術

- Python 3 / Flask
- SQLite / SQLAlchemy
- matplotlib
- Bootstrap 5
- Git / GitHub

## 💻 起動方法（ローカル）

```bash
git clone https://github.com/sotaro711/study-tracker.git
cd study-tracker
python -m venv venv
venv\Scripts\activate  # ※Windowsの場合
pip install -r requirements.txt
python run.py
