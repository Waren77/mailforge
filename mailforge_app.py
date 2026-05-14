from flask import Flask, request, render_template_string
import smtplib
import os

app = Flask(__name__)

HTML = """
<h2>🚀 MailForge</h2>

<form method="POST">
    <input name="to" placeholder="Recipient Email"><br><br>
    <input name="subject" placeholder="Subject"><br><br>
    <textarea name="message" placeholder="Message"></textarea><br><br>
    <button type="submit">Send Email</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        to = request.form["to"]
        subject = request.form["subject"]
        message = request.form["message"]
        
        sender_email = "YOUR_EMAIL@gmail.com"
        password = "YOUR_APP_PASSWORD"

        text = f"Subject: {subject}\n\n{message}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to, text)
            server.quit()
            return "<h3>Email sent successfully 🚀</h3>"
        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"

    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True)