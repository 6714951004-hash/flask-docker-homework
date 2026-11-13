from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "log.txt"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Flask Docker Homework</title>
    <style>
        body { font-family: sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
        input[type="text"] { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background-color: #e9f7ef; border-left: 5px solid #28a745; }
    </style>
</head>
<body>
    <h2>ระบบบันทึกข้อความ (Flask + Docker)</h2>
    <form method="POST">
        <label for="message">กรอกข้อความที่ต้องการบันทึก:</label>
        <input type="text" id="message" name="message" placeholder="พิมพ์ข้อความที่นี่..." required>
        <button type="submit">ส่งข้อมูล</button>
    </form>

    {% if submitted_message %}
    <div class="result">
        <strong>ได้รับข้อความเรียบร้อยแล้ว:</strong><br>
        {{ submitted_message }}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    submitted_message = None
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
            submitted_message = message
    return render_template_string(HTML_TEMPLATE, submitted_message=submitted_message)

if __name__ == "__main__":
    # สร้างไฟล์ log.txt เปล่าไว้ตั้งแต่เริ่มหากยังไม่มี
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w", encoding="utf-8").close()
    app.run(host="0.0.0.0", port=5000)