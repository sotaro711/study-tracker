from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app import db
from app.models import StudyLog
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import csv
from collections import defaultdict

main = Blueprint('main', __name__)

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

@main.route("/graph")
def show_graph():
    logs = StudyLog.query.all()

    # 日別に学習時間を集計
    daily_totals = defaultdict(float)
    for log in logs:
        daily_totals[log.date] += log.study_time

    dates = sorted(daily_totals.keys())
    hours = [daily_totals[d] for d in dates]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, hours, marker='o')
    plt.title("日別学習時間")
    plt.xlabel("日付")
    plt.ylabel("学習時間 (h)")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    return render_template("graph.html", plot_url=plot_data)

@main.route("/download_csv")
def download_csv():
    logs = StudyLog.query.order_by(StudyLog.date.desc()).all()

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(["教科", "学習時間(h)", "日付", "メモ"])
    for log in logs:
        writer.writerow([log.subject, log.study_time, log.date.strftime("%Y-%m-%d"), log.note])

    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)

    return send_file(output,
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='study_logs.csv')

@main.route("/delete/<int:log_id>", methods=["POST"])
def delete_log(log_id):
    log = StudyLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return redirect(url_for("main.index"))
