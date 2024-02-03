from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Use triple slashes for relative paths in SQLite URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# Suppress a warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Don't create tables here, create them in the main block

@app.route('/')
def home1():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/submit_analysis', methods=['POST'])
def submit_analysis():
    user_input = request.form['user_input']

    # Save user input to a file
    with open('user_input.txt', 'w') as file:
        file.write(user_input)

    return redirect(url_for('result', user_input=user_input))
@app.route('/save_user_input', methods=['POST'])
def save_user_input():
    try:
        data = request.json
        user_input = data.get('user_input', '')
        
        # Save user input to a file
        with open('user_input.txt', 'w') as file:
            file.write(user_input)

        return '', 200  # Return success status
    except Exception as e:
        print('Error saving user input:', str(e))
        return '', 500  # Return internal server error status
@app.route('/result.html')
def result():
    user_input = request.args.get('user_input', '')
    # Perform additional logic if needed

    return render_template('result.html', user_input=user_input)

@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        new_contact = ContactForm(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        # Redirect to home route after form submission
        return redirect(url_for('home1'))  # Corrected the route

    return render_template('contact.html')

@app.route('/heading.html')
def heading():
    # Add logic or rendering for heading.html
    return render_template('heading.html')

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)
