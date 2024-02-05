import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle
import pandas as pd

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

# Load your scikit-learn model
model_path = os.path.join('website', 'Model', 'model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Define left_words and right_words
left_words = [
    'left', 'liberal', 'progressive', 'socialist', 'egalitarian', 'inclusive', 'environmentalist',
    'activist', 'feminist', 'peaceful', 'tolerant', 'diverse', 'reformist', 'humanitarian',
    'pro-choice', 'equality', 'worker', 'communal', 'cooperative', 'solidarity', 'liberation',
    'pacifist', 'progress', 'community', 'social justice', 'open-minded', 'civil rights',
    'anti-war', 'sustainability', 'green', 'renewable', 'fair trade', 'inclusive', 'empowerment',
    'multicultural', 'ally', 'progressive tax', 'welfare', 'universal healthcare', 'gun control',
    'climate change', 'activism', 'grassroots', 'egalitarianism'
]

right_words = [
    'right', 'conservative', 'traditional', 'nationalist', 'patriotic', 'capitalist', 'free-market',
    'individualist', 'limited government', 'self-reliance', 'pro-life', 'law and order', 'authoritarian',
    'strong defense', 'border security', 'national sovereignty', 'family values', 'religious freedom',
    'military strength', 'liberty', 'small government', 'free enterprise', 'individual freedom',
    'entrepreneurship', 'traditional values', 'hard work', 'free speech', 'traditional marriage',
    'personal responsibility', 'gun rights', 'limited regulation', 'low taxes', 'conservation',
    'nationalism', 'traditionalism', 'family', 'heritage', 'values', 'private property', 'economic freedom',
    'individual rights', 'constitutionalism', 'protectionism', 'secure borders', 'patriotism',
    'protection of life', 'defense spending', 'religious values'
]

# Add any additional words that you think might be relevant to each category.


def check_political_inclination(text, left_words, right_words):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)

    if sentiment_scores['compound'] >= 0.05:
        result = "Neutral or no clear political inclination"
    elif sentiment_scores['compound'] <= -0.05:
        if any(word in text.lower() for word in left_words):
            result = "Left-leaning"
        elif any(word in text.lower() for word in right_words):
            result = "Right-leaning"
        else:
            result = "Neutral or no clear political inclination"
    else:
        result = "Neutral or no clear political inclination"

    print(f"Text: {text}")
    print(f"Result: {result}")
    print(f"Sentiment Scores: {sentiment_scores}")

    return result, sentiment_scores

def analyze_articles(article_df, left_words, right_words):
    results = []
    for index, row in article_df.iterrows():
        article_text = row['Content'].lower()
        result, sentiment_scores = check_political_inclination(article_text, left_words, right_words)
        results.append({
            'Article': index + 1,
            'Result': result,
            'Positive': sentiment_scores['pos'],
            'Negative': sentiment_scores['neg'],
            'Neutral': sentiment_scores['neu'],
            'Compound': sentiment_scores['compound']
        })
        print(f"Article {index + 1}: {result}")
    return results

@app.route('/')
def home1():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/submit_analysis', methods=['POST'])
def submit_analysis():
    # Read the contents of 'user_input.txt'
    with open('user_input.txt', 'r') as file:
        user_input = file.read()

    # Save user input to a file
    with open('user_input.txt', 'w') as file:
        file.write(user_input)

    # Initialize article_df here
    article_df = pd.DataFrame({'Content': [user_input]})

    # Assuming you have an analyze_articles function, adjust this line accordingly
    analysis_results = analyze_articles(article_df, left_words, right_words)

    # Get the model prediction for user_input
    model_output = model.predict([user_input])[0]  # Assuming model is a text classification model

    return render_template('result.html', user_input=user_input, content_classification=model_output, done_button=True)


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
    analysis_results = request.args.get('analysis_results', None)
    model_output = request.args.get('model_output', None)

    return render_template('result.html', user_input=user_input, analysis_results=analysis_results, model_output=model_output)

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
        return redirect(url_for('home1'))

    return render_template('contact.html')

@app.route('/heading.html')
def heading():
    # Add logic or rendering for heading.html
    return render_template('heading.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5500)
