import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

def load_corpus(file_path):
    corpus_df = pd.read_csv(file_path)
    left_words = corpus_df['Left'].dropna().str.lower().tolist()
    right_words = corpus_df['Right'].dropna().str.lower().tolist()
    return left_words, right_words

def check_political_inclination(text, left_words, right_words):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)

    if sentiment_scores['compound'] >= 0.05:
        return "Neutral or no clear political inclination"
    elif sentiment_scores['compound'] <= -0.05:
        if any(word in text.lower() for word in left_words):
            return "Left-leaning"
        elif any(word in text.lower() for word in right_words):
            return "Right-leaning"
        else:
            return "Neutral or no clear political inclination"
    else:
        return "Neutral or no clear political inclination"

def analyze_articles(article_df, left_words, right_words):
    for index, row in article_df.iterrows():
        article_text = row['News Content'].lower()
        result = check_political_inclination(article_text, left_words, right_words)
        print(f"Article {index + 1}: {result}")

if __name__ == "__main__":
    corpus_file_path = 'Team-Should/Data set/Political Corpus - Sheet1.csv'
    article_file_path = 'Team-Should/Data set/indian_express_political_article_one_year_scraped.csv'

    left_words, right_words = load_corpus(corpus_file_path)
    article_df = pd.read_csv(article_file_path)

    analyze_articles(article_df, left_words, right_words)
