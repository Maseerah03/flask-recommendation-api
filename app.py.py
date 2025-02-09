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
    try:
        aspects = request.args.get("aspects", "")
        aspect_list = [a.strip() for a in aspects.split(",")]
        recommendations = recommend_products(aspect_list)
        return jsonify({"recommended_aspects": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)})

# Fix: Use Render-compatible host and port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)  # Debug mode for error logs
