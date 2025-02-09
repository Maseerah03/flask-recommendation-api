# -*- coding: utf-8 -*-
"""Untitled55.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12drN-2xp8OFXgx59ghsWYYBNavT08Yhb
"""

!pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_amazon_reviews(url, num_pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36"
    }

    reviews = []

    for page in range(1, num_pages + 1):
        full_url = f"{url}&pageNumber={page}"
        response = requests.get(full_url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}, status code:", response.status_code)
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        review_elements = soup.find_all("span", {"data-hook": "review-body"})

        for review in review_elements:
            reviews.append(review.text.strip())

        time.sleep(2)  # Delay to prevent getting blocked

    return reviews

PRODUCT_URL = "https://www.amazon.in/gp/aw/d/B0CHX3TW6X/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=69c382013700199a3fc322dc4f40afc7&hsa_cr_id=0&qid=1739093065&sr=1-1-e0fa1fdd-d857-4087-adda-5bd576b25987&ref_=sbx_be_s_sparkle_lsi4d_asin_0_title&pd_rd_w=V11nX&content-id=amzn1.sym.df9fe057-524b-4172-ac34-9a1b3c4e647d%3Aamzn1.sym.df9fe057-524b-4172-ac34-9a1b3c4e647d&pf_rd_p=df9fe057-524b-4172-ac34-9a1b3c4e647d&pf_rd_r=YF2CXYFCPPX3VH3YRSVV&pd_rd_wg=rJbZu&pd_rd_r=5b883a80-bb45-46cd-917f-9a4fda346a97&th=1"

reviews = scrape_amazon_reviews(PRODUCT_URL, num_pages=3)

# Save to CSV
df = pd.DataFrame(reviews, columns=["Review"])
df.to_csv("amazon_reviews.csv", index=False)

print("Scraping Complete! Reviews saved to amazon_reviews.csv")

!pip install nltk pandas

import pandas as pd

# Load the scraped reviews
df = pd.read_csv("amazon_reviews.csv")

# Display first few reviews
df.head()

import nltk

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")  # WordNet dependency
nltk.download('punkt_tab')

import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load dataset
df = pd.read_csv("amazon_reviews.csv")

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    words = word_tokenize(text)  # Tokenize text
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Lemmatization & remove stopwords
    return " ".join(words)

# Apply cleaning function to all reviews
df["Cleaned_Review"] = df["Review"].apply(clean_text)

# Save cleaned reviews
df.to_csv("cleaned_reviews.csv", index=False)

print("Preprocessing Complete! Cleaned reviews saved to cleaned_reviews.csv")

!pip install nltk pandas vaderSentiment

import pandas as pd

# Load preprocessed reviews
df = pd.read_csv("cleaned_reviews.csv")

# Display the first few reviews
df.head()

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
nltk.download("vader_lexicon")

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Function to classify sentiment
def get_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
df["Sentiment"] = df["Cleaned_Review"].apply(get_sentiment)

# Save sentiment analysis results
df.to_csv("sentiment_analysis_results.csv", index=False)

print("Sentiment Analysis Complete! Results saved to sentiment_analysis_results.csv")
df.head()

!pip install spacy pandas nltk
!python -m spacy download en_core_web_sm

import pandas as pd

# Load preprocessed reviews with sentiment
df = pd.read_csv("sentiment_analysis_results.csv")

# Display first few rows
df.head()

import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to extract aspects (nouns)
def extract_aspects(text):
    doc = nlp(text)
    aspects = [token.text for token in doc if token.pos_ in ["NOUN"]]
    return ", ".join(aspects)

# Apply function to extract aspects from each review
df["Aspects"] = df["Cleaned_Review"].apply(extract_aspects)

# Save extracted aspects
df.to_csv("aspect_extraction_results.csv", index=False)

print("Aspect Extraction Complete! Results saved to aspect_extraction_results.csv")
df.head()

from collections import defaultdict

# Create a dictionary to store aspect-based sentiments
aspect_sentiments = defaultdict(lambda: {"Positive": 0, "Negative": 0, "Neutral": 0})

# Loop through reviews and count sentiment per aspect
for _, row in df.iterrows():
    aspects = row["Aspects"].split(", ")
    sentiment = row["Sentiment"]

    for aspect in aspects:
        if aspect:
            aspect_sentiments[aspect][sentiment] += 1

# Convert aspect sentiment counts into a DataFrame
aspect_df = pd.DataFrame.from_dict(aspect_sentiments, orient="index").reset_index()
aspect_df.columns = ["Aspect", "Positive", "Negative", "Neutral"]

# Save aspect-based sentiment analysis
aspect_df.to_csv("aspect_based_sentiment_analysis.csv", index=False)

print("Aspect-Based Sentiment Analysis Complete! Results saved to aspect_based_sentiment_analysis.csv")
aspect_df.head()

!pip install matplotlib seaborn pandas

import pandas as pd

# Load aspect-based sentiment analysis results
aspect_df = pd.read_csv("aspect_based_sentiment_analysis.csv")

# Display first few rows
aspect_df.head()

import matplotlib.pyplot as plt
import seaborn as sns

# Sort aspects by most positive mentions
aspect_df = aspect_df.sort_values(by="Positive", ascending=False).head(10)

# Plot sentiment distribution
plt.figure(figsize=(12, 6))
sns.barplot(x="Aspect", y="Positive", data=aspect_df, color="green", label="Positive")
sns.barplot(x="Aspect", y="Negative", data=aspect_df, color="red", label="Negative", alpha=0.7)
sns.barplot(x="Aspect", y="Neutral", data=aspect_df, color="gray", label="Neutral", alpha=0.5)

plt.xlabel("Product Aspects")
plt.ylabel("Number of Mentions")
plt.title("Aspect-Based Sentiment Analysis")
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Get top 5 liked and disliked aspects
top_positive_aspects = aspect_df.nlargest(5, "Positive")[["Aspect", "Positive"]]
top_negative_aspects = aspect_df.nlargest(5, "Negative")[["Aspect", "Negative"]]

print("Top 5 Most Liked Aspects:\n", top_positive_aspects)
print("\nTop 5 Most Disliked Aspects:\n", top_negative_aspects)

!pip install pandas numpy

import pandas as pd

# Load aspect sentiment analysis results
aspect_df = pd.read_csv("aspect_based_sentiment_analysis.csv")

# Display first few rows
aspect_df.head()

# Avoid division by zero by adding a small value (0.001)
aspect_df["Sentiment_Score"] = (aspect_df["Positive"] - aspect_df["Negative"]) / (aspect_df["Positive"] + aspect_df["Negative"] + aspect_df["Neutral"] + 0.001)

# Sort by highest sentiment score
recommended_aspects = aspect_df.sort_values(by="Sentiment_Score", ascending=False)

# Display top aspects
print("Top Recommended Aspects:")
print(recommended_aspects[["Aspect", "Sentiment_Score"]].head(10))

def recommend_products(aspect_list, threshold=0.2):
    """
    Recommends products based on sentiment score of aspects.

    :param aspect_list: List of aspects important to the user
    :param threshold: Minimum sentiment score for recommendation
    :return: List of recommended aspects
    """
    filtered_aspects = recommended_aspects[recommended_aspects["Aspect"].isin(aspect_list)]
    recommended = filtered_aspects[filtered_aspects["Sentiment_Score"] > threshold]

    return recommended[["Aspect", "Sentiment_Score"]]

# Example: Recommend products for aspects related to "battery" and "design"
user_aspects = ["battery", "design"]
recommendations = recommend_products(user_aspects)

print("Recommended Aspects for You:")
print(recommendations)

"""###REFUND OPTIMIZATION"""

import pandas as pd

# Load sentiment analysis results
df = pd.read_csv("sentiment_analysis_results.csv")

# Display first few rows
df.head()

# Keywords related to refunds & returns
refund_keywords = ["refund", "return", "replace", "replacement", "money back", "defective", "damaged"]

# Function to check if a review mentions refund-related terms
def is_refund_related(review):
    return any(keyword in review.lower() for keyword in refund_keywords)

# Apply function to find refund-related reviews
df["Refund_Related"] = df["Cleaned_Review"].apply(is_refund_related)

# Filter refund-related reviews
refund_reviews = df[df["Refund_Related"] == True]

# Save refund-related reviews
refund_reviews.to_csv("refund_related_reviews.csv", index=False)

print("Refund Analysis Complete! Refund-related reviews saved to refund_related_reviews.csv")
refund_reviews.head()

from collections import Counter
import nltk
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.download("punkt")

# Tokenize refund reviews
refund_words = []
for review in refund_reviews["Cleaned_Review"]:
    refund_words.extend(word_tokenize(review.lower()))

# Count most common words
common_words = Counter(refund_words).most_common(20)

# Display top refund reasons
print("Top 20 Most Common Words in Refund Reviews:")
for word, count in common_words:
    print(f"{word}: {count}")

# Function to predict refund likelihood
def refund_likelihood(sentiment):
    if sentiment == "Negative":
        return "High"
    elif sentiment == "Neutral":
        return "Medium"
    else:
        return "Low"

# Apply function
refund_reviews["Refund_Likelihood"] = refund_reviews["Sentiment"].apply(refund_likelihood)

# Save refund predictions
refund_reviews.to_csv("refund_likelihood_predictions.csv", index=False)

print("Refund Prediction Complete! Results saved to refund_likelihood_predictions.csv")
refund_reviews[["Cleaned_Review", "Sentiment", "Refund_Likelihood"]].head()

"""###Deploying the Recommendation System as a Flask API

"""

!pip install flask pandas

import pandas as pd
from flask import Flask, request, jsonify

# Load aspect-based sentiment data
aspect_df = pd.read_csv("aspect_based_sentiment_analysis.csv")

# Calculate Sentiment Score
aspect_df["Sentiment_Score"] = (aspect_df["Positive"] - aspect_df["Negative"]) / (aspect_df["Positive"] + aspect_df["Negative"] + aspect_df["Neutral"] + 0.001)

# Sort by sentiment score
recommended_aspects = aspect_df.sort_values(by="Sentiment_Score", ascending=False)

# Flask app setup
app = Flask(__name__)

# Define recommendation function
def recommend_products(aspect_list, threshold=0.2):
    filtered_aspects = recommended_aspects[recommended_aspects["Aspect"].isin(aspect_list)]
    recommended = filtered_aspects[filtered_aspects["Sentiment_Score"] > threshold]
    return recommended[["Aspect", "Sentiment_Score"]].to_dict(orient="records")

# Flask API endpoint
@app.route("/recommend", methods=["GET"])
def recommend():
    # Get user input (comma-separated aspects)
    aspects = request.args.get("aspects", "")
    aspect_list = [a.strip() for a in aspects.split(",")]

    # Get recommendations
    recommendations = recommend_products(aspect_list)

    return jsonify({"recommended_aspects": recommendations})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

