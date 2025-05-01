from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv('API_KEY')

@app.route('/')
def home():
    return """
    <h1>Weather Service</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/weather">/weather</a> - Get current weather</li>
    </ul>
    """


@app.route('/weather')
def get_weather():
    try:
        city = os.getenv('CITY', 'London')
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric",
            timeout=5
        )

        # 检查响应状态
        response.raise_for_status()
        data = response.json()

        # 验证数据结构
        if 'main' not in data:
            return jsonify({
                "error": "Invalid API response",
                "raw_response": data  # 返回原始数据用于调试
            }), 502

        return jsonify({
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)