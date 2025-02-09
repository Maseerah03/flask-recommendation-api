import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS  # Allow frontend to call API

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Fix CORS issue

# Ensure CSV is available
csv_url = "https://raw.githubusercontent.com/Maseerah03/flask-recommendation-api/main/aspect_based_sentiment_analysis.csv"
csv_path = "aspect_based_sentiment_analysis.csv"

if not os.path.exists(csv_path):
    print("Downloading missing CSV file...")
    df = pd.read_csv(csv_url)
    df.to_csv(csv_path, index=False)

# Load aspect-based sentiment data
aspect_df = pd.read_csv(csv_path)

# Calculate Sentiment Score
aspect_df["Sentiment_Score"] = (aspect_df["Positive"] - aspect_df["Negative"]) / (
    aspect_df["Positive"] + aspect_df["Negative"] + aspect_df["Neutral"] + 0.001
)

# Sort by sentiment score
recommended_aspects = aspect_df.sort_values(by="Sentiment_Score", ascending=False)

# Define recommendation function
def recommend_products(aspect_list, threshold=0.2):
    filtered_aspects = recommended_aspects[recommended_aspects["Aspect"].isin(aspect_list)]
    recommended = filtered_aspects[filtered_aspects["Sentiment_Score"] > threshold]
    return recommended[["Aspect", "Sentiment_Score"]].to_dict(orient="records")

# Flask API endpoint
@app.route("/recommend", methods=["GET"])
def recommend():
    try:
        # Get user input (comma-separated aspects)
        aspects = request.args.get("aspects", "")
        aspect_list = [a.strip() for a in aspects.split(",")]

        # Get recommendations
        recommendations = recommend_products(aspect_list)

        return jsonify({"recommended_aspects": recommendations})
    
    except Exception as e:
        return jsonify({"error": str(e)})

# Run Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use environment variable for Render
    app.run(host="0.0.0.0", port=port, debug=True)
