# # import pickle
# # import numpy as np

# # # Load the pickled model
# # with open("Team-Should/website/Model/model.pkl", 'rb') as file:
# #     loaded_object = pickle.load(file)

# # # Check the type of the loaded object
# # if isinstance(loaded_object, np.ndarray):
# #     print("Loaded object is a NumPy array. It does not have a predict method.")
# # else:
# #     # Assuming it's a scikit-learn model, use the predict method
# #     new_input_data = np.array(['Hello world'])
# #     Y_predict = loaded_object.predict(new_input_data)
# #     print("Prediction:", Y_predict)



# import joblib

# # Load the pre-trained model and vectorizer from .pkl files
# model = joblib.load('Team-Should/website/Model/model.pkl')
# vectorizer = joblib.load('Team-Should/website/Model/first_vectorizer.pkl')

# # Read the contents of the .txt file
# with open('user_input.txt', 'r') as file:
#     text_data = file.read()

# # Use the loaded vectorizer to transform the input text
# vectorized_text = vectorizer.transform([text_data])

# # Make predictions using the loaded model
# predictions = model.predict(vectorized_text)

# # Print or use the predictions as needed
# print(predictions)

import joblib
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

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

# Load the pre-trained model and vectorizer from .pkl files
model = joblib.load('Team-Should/website/Model/model.pkl')
vectorizer = joblib.load('Team-Should/website/Model/first_vectorizer.pkl')

# Load the political corpus data
political_corpus_data = pd.read_csv('Team-Should/Data set/Political Corpus - Sheet1.csv')

def classify_content(text_data):
    left_keywords = political_corpus_data['Left'].tolist()
    right_keywords = political_corpus_data['Right'].tolist()
    text_data_lower = text_data.lower()

    if any(keyword in text_data_lower for keyword in left_keywords):
        return 'Left'
    elif any(keyword in text_data_lower for keyword in right_keywords):
        return 'Right'
    else:
        return 'Neutral'

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

    # Use the loaded vectorizer to transform the input text
    vectorized_text = vectorizer.transform([user_input])

    # Make predictions using the loaded model
    prediction = model.predict(vectorized_text)[0]

    # Check whether the content is left, right, or neutral based on the political corpus data
    content_classification = classify_content(user_input)

    return redirect(url_for('result', user_input=user_input, prediction=prediction, content_classification=content_classification))

@app.route('/result.html')
def result():
    user_input = request.args.get('user_input', '')
    prediction = request.args.get('prediction', '')
    content_classification = request.args.get('content_classification', '')

    return render_template('result.html', user_input=user_input, prediction=prediction, content_classification=content_classification)

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
