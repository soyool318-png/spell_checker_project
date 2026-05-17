import os
import difflib
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

# Groq API 연결
client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# 수정된 부분 빨간색 표시
def highlight_changes(original, corrected):
    result = ""

    diff = difflib.ndiff(original, corrected)

    for d in diff:
        code = d[0]
        char = d[-1]

        # 같은 글자
        if code == " ":
            result += char

        # 추가된(수정된) 글자
        elif code == "+":
            result += f'<span style="color:red; font-weight:bold;">{char}</span>'

    return result


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
            line-height: 1.8;
            font-size: 18px;
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

            document.getElementById("result").innerHTML = "검사 중...";

            const response = await fetch("/check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            document.getElementById("result").innerHTML = data.result;
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
를 수정해라.

가능한 한 원문의 글자와 형태를 유지한 채 수정해라.
표현을 완전히 다른 표현으로 바꾸지 마라.
예를 들면, 다나까체를 요체로 바꾸지 마라.

문체, 말투, 의미, 어조는 유지해라.
존댓말/반말을 임의로 바꾸지 마라.

인터넷 말투와 구어체 표현도 올바르게 교정해라.

영어 문장이 들어오면:
- 번역하지 마라.
- 문장을 전체적으로 정확하게 분석해라.
- 영어 어법, 문법, 철자를 정확하게 수정해라.

설명하지 마라.
추가 문장을 쓰지 마라.

수정할 부분이 없으면 원문 그대로 출력해라.
"""
                },

                {
                    "role": "user",
                    "content": text
                }
            ],

            temperature=0,
            max_tokens=200
        )

        result = response.choices[0].message.content.strip()

        # 화살표 제거 방지
        if "->" in result:
            result = result.split("->")[-1].strip()

        # 원문과 수정문 비교해서 빨간색 처리
        highlighted = highlight_changes(text, result)

        result = highlighted

    except Exception as e:

        result = text

    return jsonify({"result": result})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
