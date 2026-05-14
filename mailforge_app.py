from flask import Flask, render_template_string, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MailForge Pro</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .tab { display: none; padding: 10px; border: 1px solid #ccc; margin-top: 10px; }
        .active { display: block; }
        button { margin: 5px; padding: 10px; }
    </style>
</head>

<body>

<h2>📧 MailForge Pro</h2>

<button onclick="showTab('send')">Send Email</button>
<button onclick="showTab('gen')">Generate Email</button>
<button onclick="showTab('bulk')">Bulk Email</button>

<!-- SEND EMAIL -->
<div id="send" class="tab active">
    <h3>Send Email</h3>
    <form method="POST">
        <input name="sender" placeholder="Sender Email"><br><br>
        <input name="recipient" placeholder="Recipient Email"><br><br>
        <input name="subject" placeholder="Subject"><br><br>
        <textarea name="message" placeholder="Message"></textarea><br><br>
        <button type="submit">Send</button>
    </form>
</div>

<!-- GENERATOR -->
<div id="gen" class="tab">
    <h3>Email Generator</h3>
    <p>Type a prompt:</p>
    <textarea placeholder="e.g. Write a professional apology email"></textarea><br><br>
    <button>Generate</button>
</div>

<!-- BULK -->
<div id="bulk" class="tab">
    <h3>Bulk Email</h3>
    <p>Upload CSV (coming next step)</p>
    <input type="file"><br><br>
    <button>Send Bulk</button>
</div>

<script>
function showTab(tabId) {
    let tabs = document.querySelectorAll('.tab');
    tabs.forEach(t => t.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        sender = request.form["sender"]
        recipient = request.form["recipient"]
        subject = request.form["subject"]
        message = request.form["message"]

        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = recipient

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            # 🔴 PUT YOUR APP PASSWORD HERE
            server.login(sender, "ufduwsascxlbajoc")

            server.send_message(msg)
            server.quit()

            print("EMAIL SENT SUCCESSFULLY")

            return render_template_string(HTML, sent=True)

        except Exception as e:
            print("ERROR:", e)
            return render_template_string(HTML, sent=False)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)