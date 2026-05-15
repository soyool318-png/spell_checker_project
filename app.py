from flask import Flask, request, jsonify, render_template_string

# hanspell (맞춤법 검사)
from hanspell import spell_checker

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>맞춤법 검사기</title>
</head>
<body>
    <h1>맞춤법 검사기</h1>

    <textarea id="text" rows="6" cols="50" placeholder="문장을 입력하세요"></textarea>
    <br><br>

    <button onclick="check()">검사</button>

    <h3>결과</h3>
    <div id="result" style="white-space: pre-wrap;"></div>

    <script>
        async function check() {
            const text = document.getElementById("text").value;

            const res = await fetch("/check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
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

    # 🔥 안전 처리 (hanspell 오류 방지)
    if not text.strip():
        return jsonify({"result": "입력된 문장이 없습니다."})

    try:
        result = spell_checker.check(text)

        # hanspell 결과 안전 추출
        corrected = getattr(result, "checked", text)

    except Exception as e:
        # 실패해도 서버 안 죽게
        corrected = text  # 원문 반환 (안정성 우선)

    return jsonify({"result": corrected})


# Render 호환 실행
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
