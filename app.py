import os
from flask import Flask, request, jsonify

# Define Flask app
app = Flask(__name__)

# Sample product recommendations based on aspects
product_recommendations = {
    "battery": ["Samsung Galaxy M51", "iPhone 13 Pro Max", "OnePlus 9"],
    "design": ["MacBook Air M2", "Dell XPS 13", "HP Spectre x360"],
    "camera": ["Canon EOS R6", "Nikon Z50", "Sony A7 III"],
    "performance": ["ASUS ROG Strix", "MacBook Pro M2", "Lenovo Legion 5"],
    "display": ["Samsung QLED Monitor", "LG OLED TV", "BenQ 4K Monitor"],
    "gaming": ["Sony PlayStation 5", "Xbox Series X", "Nintendo Switch"],
    "sound": ["Bose QuietComfort 45", "Sony WH-1000XM4", "JBL Flip 6"],
    "processor": ["Intel i9 13th Gen", "AMD Ryzen 9 5900X", "Apple M2 Chip"],
    "storage": ["Samsung 980 Pro SSD", "WD Black NVMe", "Seagate Barracuda HDD"],
}

# Function to get product recommendations
def get_product_recommendations(aspect_list):
    recommended_products = []
    for aspect in aspect_list:
        if aspect in product_recommendations:
            recommended_products.extend(product_recommendations[aspect])
    return list(set(recommended_products))  # Remove duplicates

# Flask API route
@app.route("/recommend", methods=["GET"])
def recommend():
    try:
        aspects = request.args.get("aspects", "").lower().strip()
        aspect_list = [a.strip() for a in aspects.split(",")]

        recommended_products = get_product_recommendations(aspect_list)

        if not recommended_products:
            return jsonify({"message": "No matching products found for the given aspect."})

        return jsonify({"recommended_products": recommended_products})
    
    except Exception as e:
        return jsonify({"error": str(e)})

# Run Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
