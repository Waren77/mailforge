from flask import Flask, render_template_string, request
import smtplib
import os
import csv
import io

app = Flask(__name__)
app.secret_key = "mailforge-pro-key"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MailForge Pro</title>
</head>
<body>
    <h2>📧 MailForge Pro Email Sender</h2>

    <h3>Single Email</h3>
    <form method="POST">
        <input name="email" placeholder="Recipient Email"><br><br>
        <input name="subject" placeholder="Subject"><br><br>
        <textarea name="message" placeholder="Message"></textarea><br><br>
        <button name="action" value="single">Send Email</button>
    </form>

    <hr>

    <h3>CSV Bulk Send</h3>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv"><br><br>
        <input name="subject_bulk" placeholder="Subject"><br><br>
        <textarea name="message_bulk" placeholder="Message"></textarea><br><br>
        <button name="action" value="bulk">Send Bulk Emails</button>
    </form>

    <p>{{ msg }}</p>
</body>
</html>
"""


def get_server():
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        raise Exception("Missing EMAIL_ADDRESS or EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
    server.starttls()
    server.login(sender, password)
    return server, sender


def send_single(to_email, subject, message):
    try:
        server, sender = get_server()

        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender, to_email, msg)
        server.quit()

        return "✅ Single email sent"

    except Exception as e:
        return f"❌ Error: {str(e)}"


def send_bulk(file, subject, message):
    try:
        server, sender = get_server()

        stream = io.StringIO(file.stream.read().decode("utf-8"))
        reader = csv.reader(stream)

        count = 0

        for row in reader:
            if len(row) == 0:
                continue

            email = row[0].strip()
            if email:
                msg = f"Subject: {subject}\n\n{message}"
                server.sendmail(sender, email, msg)
                count += 1

        server.quit()

        return f"✅ Bulk emails sent: {count}"

    except Exception as e:
        return f"❌ Bulk error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "single":
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")

            msg = send_single(email, subject, message)

        elif action == "bulk":
            file = request.files.get("file")
            subject = request.form.get("subject_bulk")
            message = request.form.get("message_bulk")

            if file:
                msg = send_bulk(file, subject, message)
            else:
                msg = "❌ No CSV file uploaded"

    return render_template_string(HTML, msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)