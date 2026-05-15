from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>맞춤법 검사기</title>
</head>
<body>
    <h1>맞춤법 검사기</h1>
    <textarea id="text" rows="6" cols="50"></textarea><br>
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

    # 👉 여기서 맞춤법 라이브러리 연결 (임시 로직)
    # 지금은 간단 테스트용
    corrected = text.replace("않되", "안 돼").replace("되요", "돼요")

    return jsonify({"result": corrected})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
