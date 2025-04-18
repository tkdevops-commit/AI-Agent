# backend/main.py
from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_email():
    data = request.json
    prompt = data.get("prompt", "")
    tone = data.get("tone", "professional")
    
    messages = [
        {"role": "system", "content": f"You are an assistant writing {tone} emails."},
        {"role": "user", "content": prompt}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return jsonify({"email": response['choices'][0]['message']['content']})

@app.route("/analyze", methods=["POST"])
def analyze_email():
    data = request.json
    email_text = data.get("email", "")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that analyzes emails and extracts summary and action items."},
            {"role": "user", "content": email_text}
        ]
    )
    return jsonify({"analysis": response['choices'][0]['message']['content']})

if __name__ == "__main__":
    app.run(debug=True)
