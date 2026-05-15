import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI 맞춤법 검사기</title>
</head>
<body>
    <h1>무료 AI 맞춤법 검사기</h1>

    <textarea id="text" rows="6" cols="50"></textarea>
    <br><br>

    <button onclick="check()">검사</button>

    <h3>결과:</h3>
    <div id="result"></div>

    <script>
        async function check() {
            const text = document.getElementById("text").value;

            const response = await fetch("/check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

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
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "너는 한국어 맞춤법 검사기다. 문장을 자연스럽고 올바르게 수정해서 결과만 출력해라."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        result = response.choices[0].message.content

    except Exception as e:
        result = f"에러 발생: {str(e)}"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
