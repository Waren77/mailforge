from flask import Flask, render_template_string, request, flash, redirect
import smtplib
import os

app = Flask(__name__)
app.secret_key = "secret-key"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MailForge</title>
</head>
<body>
    <h2>MailForge Email Sender</h2>

    <form method="POST">
        <input name="email" placeholder="Recipient Email" required><br><br>
        <input name="subject" placeholder="Subject" required><br><br>
        <textarea name="message" placeholder="Message" required></textarea><br><br>
        <button type="submit">Send Email</button>
    </form>

    <p>{{ msg }}</p>
</body>
</html>
"""


def send_email(to_email, subject, message):
    sender_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not app_password:
        return "Missing environment variables"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(sender_email, app_password)

        full_msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, full_msg)
        server.quit()

        return "Email sent successfully"

    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""

    if request.method == "POST":
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        # IMPORTANT: no blocking outside function
        msg = send_email(email, subject, message)

    return render_template_string(HTML, msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)