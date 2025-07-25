# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import StudyLog
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic'  # ← 日本語フォント指定（Windows）

import io
import base64
from collections import defaultdict

# Blueprint定義
main = Blueprint('main', __name__)

# トップページ（記録入力・一覧表示）
@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form["subject"]
        study_time = float(request.form["study_time"])
        date = request.form["date"]
        note = request.form["note"]

        new_log = StudyLog(
            subject=subject,
            study_time=study_time,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            note=note
        )
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for("main.index"))

    logs = StudyLog.query.order_by(StudyLog.date.desc()).all()
    return render_template("index.html", logs=logs)

# グラフ表示ページ
@main.route("/graph")
def show_graph():
    logs = StudyLog.query.all()

    # 日付ごとの学習時間を集計
    daily_totals = defaultdict(float)
    for log in logs:
        daily_totals[log.date] += log.study_time

    dates = sorted(daily_totals.keys())
    hours = [daily_totals[d] for d in dates]

    # グラフ生成
    plt.figure(figsize=(8, 4))
    plt.plot(dates, hours, marker='o')
    plt.title("日別学習時間")
    plt.xlabel("日付")
    plt.ylabel("学習時間 (h)")
    plt.tight_layout()

    # 画像をBase64に変換してHTMLに埋め込む
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    return render_template("graph.html", plot_url=plot_data)
