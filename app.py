from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key="YOUR_API_KEY")  # ← 여기에 키 넣기

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>맞춤법 검사기</title>
</head>
<body>
    <h1>맞춤법 검사기</h1>

    <textarea id="text" rows="6" cols="50"></textarea>
    <br><br>

    <button onclick="check()">검사</button>

    <h3>결과</h3>
    <div id="result"></div>

    <script>
        async function check() {
            const text = document.getElementById("text").value;

            const res = await fetch("/check", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({text})
            });

            const data = await res.json();
            document.getElementById("result").innerText = data.result;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    text = data.get("text", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "너는 한국어 맞춤법 교정기야. 문장을 자연스럽게 교정해서 결과만 출력해."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        corrected = response.choices[0].message.content

    except Exception as e:
        corrected = f"에러: {str(e)}"

    return jsonify({"result": corrected})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
