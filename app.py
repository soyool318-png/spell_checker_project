import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

# Groq API 연결
client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# 웹페이지 HTML
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>한글/영어 맞춤법 검사기</title>
    <style>
        body {
            font-family: Arial;
            max-width: 700px;
            margin: 50px auto;
            padding: 20px;
        }

        textarea {
            width: 100%;
            height: 150px;
            font-size: 16px;
            padding: 10px;
        }

        button {
            margin-top: 15px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }

        #result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f3f3f3;
            border-radius: 10px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>

    <h1>한글/영어 맞춤법 검사기</h1>

    <textarea id="text" placeholder="문장을 입력하세요"></textarea>
    <br>

    <button onclick="check()">맞춤법 검사</button>

    <div id="result"></div>

    <script>
        async function check() {
            const text = document.getElementById("text").value;

            document.getElementById("result").innerText = "검사 중...";

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
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
    "content": """
너는 맞춤법 검사기다.

사용자의 문장에서:
- 맞춤법
- 띄어쓰기
- 오타
만 수정해라.

문체, 말투, 의미, 어조는 절대 바꾸지 마라.
원문 느낌을 최대한 유지해라.

영어 문장이 들어오면:
- 번역하지 마라.
- 영어 철자와 문법만 수정해라.

수정된 문장만 출력해라.
설명하지 마라.
화살표(->)를 사용하지 마라.
원문과 비교하지 마라.
추가 문장을 쓰지 마라.
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.2
        )

        try:
    response = client.chat.completions.create(
        ...
    )

    result = response.choices[0].message.content.strip()

    if "->" in result:
        result = result.split("->")[-1].strip()

    result = result.split("\n")[-1].strip()

except Exception as e:
    result = f"에러 발생: {str(e)}"

    except Exception as e:
        result = f"에러 발생: {str(e)}"

    return jsonify({"result": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
