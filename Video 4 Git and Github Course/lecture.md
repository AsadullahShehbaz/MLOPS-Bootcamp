# Deploy Your First ML Model — Flask API + Bootstrap + Railway (Free)

End-to-end guide: convert your Streamlit sentiment app into a Flask API with a Bootstrap frontend, then deploy it live on Railway for free.

---

## 1. Final Project Structure

```
sentiment-flask-app/
├── app.py
├── requirements.txt
├── Procfile
├── models/
│   ├── nb_pipeline.pkl
│   ├── lstm_model.h5
│   └── lstm_tokenizer.pkl
├── templates/
│   └── index.html
└── static/
    └── style.css
```

---

## 2. `app.py` — Flask Backend

This replaces your Streamlit UI with two routes: one that renders the page, one that serves predictions as JSON.

```python
# app.py
import re
import numpy as np
import joblib
import nltk
from flask import Flask, render_template, request, jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

app = Flask(__name__)

# ------------------------------
# Load models once at startup
# ------------------------------
nb_pipeline = joblib.load("models/nb_pipeline.pkl")
lstm_model = load_model("models/lstm_model.h5")
lstm_tokenizer = joblib.load("models/lstm_tokenizer.pkl")

stop_words = set(stopwords.words("english"))
label_map = {0: "Negative 😡", 1: "Neutral 😐", 2: "Positive 😊"}


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = word_tokenize(text)
    filtered = [w for w in tokens if w not in stop_words]
    return " ".join(filtered)


def predict_nb(text):
    return nb_pipeline.predict([text])[0]


def predict_lstm(text, max_len=100):
    seq = lstm_tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_len)
    pred = lstm_model.predict(padded)
    return int(np.argmax(pred, axis=1)[0])


# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "").strip()
    model_choice = data.get("model", "nb")

    if not text:
        return jsonify({"error": "Please enter some text"}), 400

    cleaned = preprocess(text)

    if model_choice == "lstm":
        label = predict_lstm(cleaned)
    else:
        label = predict_nb(cleaned)

    return jsonify({"sentiment": label_map[int(label)]})


if __name__ == "__main__":
    app.run(debug=True)
```

**Teaching point for the video:** show viewers the request in DevTools → Network tab so they see the raw JSON going to `/predict` and coming back. This is the "aha" moment that Streamlit hides.

---

## 3. `templates/index.html` — Bootstrap Frontend

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sentiment Analysis App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body class="bg-light">

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-7">
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <h3 class="mb-3 text-center">💬 Sentiment Analysis</h3>
                    <p class="text-muted text-center">Choose a model, type a review, get the sentiment.</p>

                    <div class="mb-3">
                        <label class="form-label">Model</label>
                        <select id="modelChoice" class="form-select">
                            <option value="nb">Naive Bayes</option>
                            <option value="lstm">LSTM</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Enter your review</label>
                        <textarea id="userText" class="form-control" rows="4" placeholder="Type here..."></textarea>
                    </div>

                    <button class="btn btn-primary w-100" onclick="predictSentiment()">🔎 Predict Sentiment</button>

                    <div id="result" class="alert alert-success mt-3 text-center fw-bold" style="display:none;"></div>
                    <div id="errorMsg" class="alert alert-warning mt-3 text-center" style="display:none;"></div>
                </div>
                <div class="card-footer text-center text-muted small">
                    Built with Flask + Bootstrap | Deployed on Railway
                </div>
            </div>
        </div>
    </div>
</div>

<script>
async function predictSentiment() {
    const text = document.getElementById("userText").value;
    const model = document.getElementById("modelChoice").value;
    const resultBox = document.getElementById("result");
    const errorBox = document.getElementById("errorMsg");

    resultBox.style.display = "none";
    errorBox.style.display = "none";

    if (!text.trim()) {
        errorBox.innerText = "⚠️ Please enter some text.";
        errorBox.style.display = "block";
        return;
    }

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, model })
        });
        const data = await res.json();

        if (data.error) {
            errorBox.innerText = data.error;
            errorBox.style.display = "block";
        } else {
            resultBox.innerText = "Predicted Sentiment: " + data.sentiment;
            resultBox.style.display = "block";
        }
    } catch (err) {
        errorBox.innerText = "Something went wrong. Try again.";
        errorBox.style.display = "block";
    }
}
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## 4. `static/style.css` — Small Polish Layer

```css
body {
    font-family: 'Segoe UI', sans-serif;
}
.card {
    border: none;
    border-radius: 16px;
}
```

---

## 5. `requirements.txt`

Pin versions so Railway's build is reproducible — this is a common failure point for beginners.

```
Flask==3.0.3
gunicorn==22.0.0
scikit-learn==1.5.0
joblib==1.4.2
nltk==3.8.1
tensorflow==2.16.1
numpy==1.26.4
```

> **Video callout:** `tensorflow` is heavy (~500MB+). If your LSTM model isn't essential to the demo, consider dropping it and shipping Naive Bayes only — it cuts build time dramatically and avoids Railway free-tier memory limits. This is a great "production tradeoff" teaching moment.

---

## 6. `Procfile` — Tells Railway How to Run the App

```
web: gunicorn app:app
```

No file extension. This one line replaces `streamlit run app.py`.

---

## 7. Local Testing Before Deployment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000` and confirm predictions work before touching Railway.

---

## 8. Push to GitHub

```bash
git init
git add .
git commit -m "Flask sentiment API with Bootstrap frontend"
git branch -M main
git remote add origin https://github.com/AsadullahShehbaz/sentiment-flask-app.git
git push -u origin main
```

> Tip for the video: show a `.gitignore` excluding `venv/` and `__pycache__/` so the repo stays clean.

---

## 9. Deploy on Railway (Free)

1. Go to **railway.com** → sign in with GitHub.
2. Click **New Project → Deploy from GitHub repo** → select `sentiment-flask-app`.
3. Railway auto-detects Python and reads `requirements.txt` + `Procfile`.
4. Under **Settings → Networking**, click **Generate Domain** to get a public URL.
5. Watch the **Deploy Logs** tab — this is great screen-recording material for the video since viewers see the exact build steps (pip install, gunicorn boot).
6. Once it says "Deployment live," open the generated URL.

**Common gotchas to cover on camera:**
- Model files (`.pkl`, `.h5`) must be committed to the repo (or pulled from cloud storage) — Railway can't see local-only files.
- Free tier has a memory ceiling; a large TensorFlow build can fail silently — check logs for `OOM` or `Killed`.
- If `nltk.download()` runs at import time, it can slow cold starts — consider pre-downloading and packaging the `nltk_data` folder instead.

---

## 10. Test the Live App

Open the Railway URL, type a review, hit predict, and show the Network tab again — same `/predict` call, now running on a public server instead of localhost. This full-circle moment (localhost → GitHub → Railway → public URL) is the strongest close for the video.

---

## Suggested Video Outline

1. **Hook** – "Streamlit is great for prototypes, but here's how real APIs work" (30s)
2. **Show the Flask code** – routes, JSON in/out (3–4 min)
3. **Build the Bootstrap UI** – CDN link, fetch() call (3–4 min)
4. **Local test** – prove it works before deploying (1–2 min)
5. **Push to GitHub** (1 min)
6. **Deploy on Railway** – live, screen-recorded (3–4 min)
7. **Live demo + Network tab walkthrough** (2 min)
8. **Wrap-up** – mention swapping the frontend later (React/Streamlit) without touching the API — reinforces *why* decoupling matters

Given your Kaggle Grandmaster + internship background, you could also add a short "what I'd do differently in production" segment (e.g., model versioning, Dockerizing instead of Procfile, adding a `/health` endpoint) — that kind of practitioner insight is what separates your bootcamp content from generic tutorials.