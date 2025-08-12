from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Gmail SMTP Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'akila271819@gmail.com'  # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'nmuw lfns gyml xoxu'  # Use App Password here

mail = Mail(app)

# Admin Email
ADMIN_EMAIL = 'kesavanakila08@gmail.com'  # Replace with actual admin email

# Sample contacts data
contacts = [
    {'name': 'Alice Johnson', 'phone': '555-123-4567', 'email': 'alice@example.com'},
    {'name': 'Bob Smith', 'phone': '555-987-6543', 'email': 'bob@example.com'},
]

@app.route('/')
def index():
    return render_template('index.html', contacts=contacts)

@app.route('/add-contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        phone = request.form.get('phone').strip()
        email = request.form.get('email').strip()

        if not name or not phone or not email:
            flash('Please fill out all fields.', 'danger')
            return redirect(url_for('add_contact'))

        new_contact = {'name': name, 'phone': phone, 'email': email}
        contacts.append(new_contact)

        # Send admin notification email
        try:
            msg = Message('New Contact Added',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[ADMIN_EMAIL])
            msg.body = f"A new contact was added:\n\nName: {name}\nPhone: {phone}\nEmail: {email}"
            mail.send(msg)
            flash('Contact added and admin notified!', 'success')
        except Exception as e:
            flash(f'Contact added but failed to send email notification. Error: {e}', 'warning')

        return redirect(url_for('index'))

    return render_template('add_contact.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        sender_name = request.form.get('name').strip()
        sender_email = request.form.get('email').strip()
        message = request.form.get('message').strip()

        if not sender_name or not sender_email or not message:
            flash('Please fill out all fields.', 'danger')
            return redirect(url_for('feedback'))

        try:
            msg = Message('Feedback from Contact Book',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[ADMIN_EMAIL])
            msg.body = f"Feedback received:\n\nFrom: {sender_name} <{sender_email}>\n\nMessage:\n{message}"
            mail.send(msg)
            flash('Feedback sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send feedback email. Error: {e}', 'danger')

        return redirect(url_for('index'))

    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
