from flask import Flask, render_template_string, request
import smtplib
from email.mime.text import MIMEText
import os
import threading

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MailForge Pro</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .tab { display: none; border: 1px solid #ccc; padding: 15px; margin-top: 10px; }
        .active { display: block; }
        button { margin: 5px; padding: 10px; }
        input, textarea { width: 300px; margin: 5px 0; }
    </style>
</head>
<body>

<h2>📧 MailForge Pro</h2>

<div>
    <button onclick="showTab('send')">Send Email</button>
</div>

<div id="send" class="tab active">
    <h3>Send Email</h3>
    <form method="POST">
        <input name="recipient" placeholder="Recipient Email" required><br>
        <input name="subject" placeholder="Subject" required><br>
        <textarea name="message" placeholder="Message" required></textarea><br>
        <button type="submit">Send</button>
    </form>
</div>

<script>
function showTab(id) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}
</script>

</body>
</html>
"""


# 🔥 EMAIL SENDER (RUNS IN BACKGROUND)
def send_email_async(recipient, subject, message):
    try:
        sender = os.environ.get("EMAIL_USER")
        password = os.environ.get("EMAIL_PASS")

        if not sender or not password:
            print("ENV VARIABLES MISSING")
            return

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        print("EMAIL SENT SUCCESSFULLY ✔")

    except Exception as e:
        print("EMAIL ERROR:", e)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        recipient = request.form["recipient"]
        subject = request.form["subject"]
        message = request.form["message"]

        # 🚀 RUN IN BACKGROUND (NO TIMEOUT)
        threading.Thread(
            target=send_email_async,
            args=(recipient, subject, message)
        ).start()

        return render_template_string(HTML)

    return render_template_string(HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)