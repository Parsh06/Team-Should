import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Load the political corpus data
political_corpus_data = pd.read_csv('Data set/Political Corpus - Sheet1.csv')

def classify_content(text_data):
    text_data_lower = text_data.lower()

    left_keywords = political_corpus_data['Left'].dropna().tolist()
    right_keywords = political_corpus_data['Right'].dropna().tolist()

    if any(keyword in text_data_lower for keyword in left_keywords):
        return 'Left'
    elif any(keyword in text_data_lower for keyword in right_keywords):
        return 'Right'
    else:
        return 'Neutral'

def check_political_inclination(text):
    content_classification = classify_content(text)
    return content_classification

@app.route('/')
def home1():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/submit_analysis', methods=['POST'])
def submit_analysis():
    user_input = request.form['user_input']
    with open('user_input.txt', 'w') as file:
        file.write(user_input)

    # Perform content classification
    content_classification = check_political_inclination(user_input)

    return redirect(url_for('result', user_input=user_input, content_classification=content_classification))


@app.route('/result.html')
def result():
    user_input = request.args.get('user_input', '')
    content_classification = request.args.get('content_classification', '')

    return render_template('result.html', user_input=user_input, content_classification=content_classification)

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

        return redirect(url_for('home'))

    return render_template('contact.html')

@app.route('/heading.html')
def heading():
    # Add logic or rendering for heading.html
    return render_template('heading.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5500)
