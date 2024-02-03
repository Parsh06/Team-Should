from flask import Flask, render_template, redirect, url_for, request, send_file

app = Flask(__name__)

@app.route('/')
def home1():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/submit_contact_form', methods=['GET', 'POST'])
def submit_contact_form():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        
        # Save user_input to a file on the server
        with open('Team-Should/Data set/user_input.csv', 'w') as file:
            file.write(user_input)
        
        # Redirect to home route
        return redirect(url_for('index.html'))
    else:
        # Handle GET request, if needed
        return render_template('submit_contact_form.html')  # Add a template for this if necessary

@app.route('/download_user_input')
def download_user_input():
    # Send the user_input.csv file to the user for download
    return send_file('Team-Should/Data set/user_input.csv', as_attachment=True)

# Add routes for additional pages
@app.route('/result.html')
def result():
    # Add logic or rendering for result.html
    return render_template('result.html')

@app.route('/contact.html')
def contact():
    # Add logic or rendering for contact.html
    return render_template('contact.html')

@app.route('/heading.html')
def heading():
    # Add logic or rendering for heading.html
    return render_template('heading.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
