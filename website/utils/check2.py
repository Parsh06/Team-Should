import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the dataset with left and right columns
df = pd.read_csv('Team-Should/Data set/Political Corpus - Sheet1.csv')

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Function to check political inclination based on words in the corpus file
def check_political_inclination(text, left_words, right_words):
    # Analyze sentiment of the text
    sentiment_scores = sia.polarity_scores(text)
    
    # Check for positive or negative sentiment
    if sentiment_scores['compound'] >= 0.05:
        return "Neutral or no clear political inclination"
    elif sentiment_scores['compound'] <= -0.05:
        # Check for words in the 'left' column
        if any(word in text.lower() for word in left_words):
            return "Left-leaning"
        # Check for words in the 'right' column
        elif any(word in text.lower() for word in right_words):
            return "Right-leaning"
        else:
            return "Neutral or no clear political inclination"
    else:
        return "Neutral or no clear political inclination"

# Get the list of words from the 'left' and 'right' columns in the corpus file
left_words = df['left'].dropna().tolist()
right_words = df['right'].dropna().tolist()

# Iterate through rows in the dataset and print political inclination
for index, row in df.iterrows():
    article_text = row['left'] if row['left'] else row['right']  # Choose the column with the text in your corpus
    result = check_political_inclination(article_text, left_words, right_words)
    print(f"Article {index + 1}: {result}")
