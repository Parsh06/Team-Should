import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the dataset
df = pd.read_csv('Team-Should/Data set/indian_express_political_article_one_year_scraped.csv')

# Predefined words for left-leaning, right-leaning, and neutral
left_words = ['progressive', 'equality', 'social justice', 'welfare', 'public service']
right_words = ['conservative', 'individual liberty', 'free market', 'national security', 'traditional values']

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Function to check political inclination based on predefined words
def check_political_inclination(text):
    # Analyze sentiment of the text
    sentiment_scores = sia.polarity_scores(text)
    
    # Check for positive or negative sentiment
    if sentiment_scores['compound'] >= 0.05:
        return "Neutral or no clear political inclination"
    elif sentiment_scores['compound'] <= -0.05:
        # Check for predefined left-leaning words
        if any(word in text.lower() for word in left_words):
            return "Left-leaning"
        # Check for predefined right-leaning words
        elif any(word in text.lower() for word in right_words):
            return "Right-leaning"
        else:
            return "Neutral or no clear political inclination"
    else:
        return "Neutral or no clear political inclination"

# Iterate through rows in the dataset and print political inclination
for index, row in df.iterrows():
    article_text = row['News Content']  # Replace 'your_actual_column_name' with the correct column name
    result = check_political_inclination(article_text)
    print(f"Article {index + 1}: {result}")
