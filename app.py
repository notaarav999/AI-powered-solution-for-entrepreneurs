from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

# Google Gemini API Key
GEMINI_API_KEY = "AIzaSyB4MQ_qUVx0_em6HJtabbm6rA4WiejjM3w"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data['message']

    # Send request to Google Gemini AI
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(GEMINI_URL, json=payload, headers=headers)
    if response.status_code == 200:
        ai_reply = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't understand.")
    else:
        ai_reply = "Error: Unable to reach AI service."

    return jsonify(reply=ai_reply)

if __name__ == '__main__':
    app.run(debug=True)
