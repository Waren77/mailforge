from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MailForge</title>
</head>
<body>
    <h2>MailForge Email Sender</h2>

    <form method="POST">
        <label>Sender Email:</label><br>
        <input name="sender" required><br><br>

        <label>Recipient Email:</label><br>
        <input name="recipient" required><br><br>

        <label>Subject:</label><br>
        <input name="subject" required><br><br>

        <label>Message:</label><br>
        <textarea name="message" required></textarea><br><br>

        <button type="submit">Send Email</button>
    </form>

    {% if sent %}
        <p style="color:green;">Email prepared successfully (demo mode)</p>
    {% endif %}
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

        print("SENDING EMAIL:")
        print(sender, recipient, subject, message)

        return render_template_string(HTML, sent=True)

    return render_template_string(HTML, sent=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)