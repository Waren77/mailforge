import os
import csv
import smtplib
from flask import Flask, request, render_template_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


# ---------------- AI EMAIL GENERATOR (SIMPLE SMART TEMPLATE ENGINE) ----------------
def generate_email(prompt, recipient):
    """
    Lightweight AI generator (no API needed)
    """
    prompt = prompt.lower()

    if "sale" in prompt:
        return f"""
Hello {recipient},

We are excited to announce our latest SALE! 🎉
Don't miss out on exclusive discounts available for a limited time.

Regards,
{EMAIL_ADDRESS}
"""

    elif "meeting" in prompt:
        return f"""
Hello {recipient},

This is a reminder about our upcoming meeting.
Please confirm your availability.

Regards,
{EMAIL_ADDRESS}
"""

    elif "job" in prompt:
        return f"""
Hello {recipient},

We would like to inform you about a new job opportunity that may interest you.
Kindly respond if interested.

Regards,
{EMAIL_ADDRESS}
"""

    else:
        return f"""
Hello {recipient},

{prompt}

Regards,
{EMAIL_ADDRESS}
"""


# ---------------- SEND EMAIL FUNCTION ----------------
def send_email(to_email, subject, message, attachment=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    # attachment support
    if attachment:
        filename = attachment.filename
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MailForge Pro</title>
</head>
<body>

<h2>MailForge Pro 🚀</h2>

<form method="POST" enctype="multipart/form-data">

    <h3>Sender Info</h3>
    <p>Using ENV variables (EMAIL_ADDRESS + APP PASSWORD)</p>

    <h3>Recipient Mode</h3>
    <label>Single Email:</label><br>
    <input name="single_email"><br><br>

    <label>OR Upload CSV (column: email)</label><br>
    <input type="file" name="csv_file"><br><br>

    <h3>Email Content</h3>

    <label>Subject:</label><br>
    <input name="subject"><br><br>

    <label>Message / AI Prompt:</label><br>
    <textarea name="message" rows="5"></textarea><br><br>

    <label>Attachment:</label><br>
    <input type="file" name="attachment"><br><br>

    <button type="submit">Send Emails</button>

</form>

<p style="color:green">{{msg}}</p>

</body>
</html>
"""


# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""

    if request.method == "POST":
        try:
            subject = request.form.get("subject", "")
            message_input = request.form.get("message", "")
            single_email = request.form.get("single_email")

            attachment = request.files.get("attachment")

            recipients = []

            # SINGLE EMAIL MODE
            if single_email:
                recipients.append(single_email)

            # CSV MODE
            csv_file = request.files.get("csv_file")
            if csv_file and csv_file.filename != "":
                stream = csv_file.stream.read().decode("utf-8").splitlines()
                reader = csv.DictReader(stream)
                for row in reader:
                    if row.get("email"):
                        recipients.append(row["email"])

            # SEND LOOP
            count = 0

            for email in recipients:
                try:
                    final_message = generate_email(message_input, email)

                    send_email(
                        to_email=email,
                        subject=subject,
                        message=final_message,
                        attachment=attachment if attachment else None
                    )

                    count += 1

                except Exception as e:
                    print("Failed:", email, e)

            msg = f"✅ Sent {count} emails successfully"

        except Exception as e:
            msg = f"❌ Error: {str(e)}"

    return render_template_string(HTML, msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)