from flask import Flask
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    # Increment counter in Redis
    count = r.incr("counter")

    return f"Welcome to Ultimate Docker Course for ML and GenAI ! Counter: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)