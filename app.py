from flask import Flask, render_template, request, url_for
from transformers import pipeline
import os

app = Flask(__name__)

# Create static folder if not exists
os.makedirs("static", exist_ok=True)

# Load model
print("Loading model...")
classifier = pipeline("image-classification")
print("Model loaded!")

def predict_food_quality(image_path):
    results = classifier(image_path)
    label = results[0]["label"].lower()

    if "rotten" in label or "mold" in label or "spoiled" in label:
        return "❌ Avoid"
    elif "fresh" in label or "healthy" in label:
        return "✅ Fresh"
    else:
        return "⚠️ Okay"

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        file = request.files["image"]
        path = os.path.join("static", "uploaded.jpg")
        file.save(path)

        prediction = predict_food_quality(path)

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run()
