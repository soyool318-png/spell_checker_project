from flask import Flask, request, jsonify

app = Flask(__name__)

# 간단 맞춤법 교정 규칙
rules = {
    "안녕하세용": "안녕하세요",
    "임니다": "입니다",
    "하세용": "하세요",
    "학생임니다": "학생입니다",
    "맞춤법틀렷어요": "맞춤법 틀렸어요"
}

@app.route('/')
def home():
    return """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>맞춤법 드래그 교정</title>
</head>

<body>

<h3>텍스트 드래그하면 교정됨</h3>

<textarea id="text" style="width:500px;height:200px;" placeholder="문장을 입력하세요"></textarea>

<p id="result" style="margin-top:20px;font-weight:bold;color:blue;"></p>

<script>
let timer = null;

// 드래그 후 마우스 떼면 실행
document.addEventListener("mouseup", function(){

    clearTimeout(timer);

    timer = setTimeout(() => {

        let selected = window.getSelection().toString();

        // 선택 없으면 아무것도 안함
        if(!selected || selected.trim().length === 0){
            return;
        }

        fetch('/check', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: selected})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerText =
                "교정 결과: " + data.result;
        });

    }, 200);

});
</script>

</body>
</html>
"""

@app.route('/check', methods=['POST'])
def check():
    text = request.json['text']

    # 맞춤법 교정
    for wrong, right in rules.items():
        text = text.replace(wrong, right)

    return jsonify({'result': text})

if __name__ == '__main__':
    app.run(debug=True)