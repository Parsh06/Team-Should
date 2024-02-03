import pandas as pd
import matplotlib.pyplot as plt
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
        return "Neutral or no clear political inclination", sentiment_scores
    elif sentiment_scores['compound'] <= -0.05:
        if any(word in text.lower() for word in left_words):
            return "Left-leaning", sentiment_scores
        elif any(word in text.lower() for word in right_words):
            return "Right-leaning", sentiment_scores
        else:
            return "Neutral or no clear political inclination", sentiment_scores
    else:
        return "Neutral or no clear political inclination", sentiment_scores

def analyze_articles(article_df, left_words, right_words):
    results = []
    for index, row in article_df.iterrows():
        article_text = row['News Content'].lower()
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

def add_analysis_to_dataframe(article_df, analysis_results):
    analysis_df = pd.DataFrame(analysis_results)
    merged_df = pd.merge(article_df, analysis_df, left_index=True, right_on='Article')
    return merged_df

def export_to_csv(df, output_file):
    df.to_csv(output_file, index=False)
    print(f"\nResults exported to {output_file}")

def visualize_results(results):
    result_df = pd.DataFrame(results)
    result_counts = result_df['Result'].value_counts()
    
    plt.bar(result_counts.index, result_counts.values, color=['blue', 'red', 'green'])
    plt.title('Distribution of Political Inclination')
    plt.xlabel('Political Inclination')
    plt.ylabel('Number of Articles')
    plt.show()

if __name__ == "__main__":
    corpus_file_path = 'Team-Should/Data set/Political Corpus - Sheet1.csv'
    article_file_path = 'Team-Should/Data set/indian_express_political_article_one_year_scraped.csv'
    output_csv_path = 'Team-Should/Data set/analysis_results.csv'

    left_words, right_words = load_corpus(corpus_file_path)
    article_df = pd.read_csv(article_file_path)

    analysis_results = analyze_articles(article_df, left_words, right_words)
    article_df_with_analysis = add_analysis_to_dataframe(article_df, analysis_results)
    export_to_csv(article_df_with_analysis, output_csv_path)
    visualize_results(analysis_results)
