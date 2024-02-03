# Your Flask app code

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result.html', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Your result handling logic for POST requests goes here
        return render_template('result.html')
    else:
        # Your logic for handling GET requests goes here (if needed)
        return render_template('result.html')  # You may want to render a different template for GET requests

@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/heading.html', methods=['GET', 'POST'])
def heading():
    return render_template('heading.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
