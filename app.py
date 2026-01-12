from flask import Flask, render_template_string, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # هذا السطر ضروري جداً لتشغيل الفيديو

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XTREAM PLAYER 2026</title>
    <script src="cdn.jsdelivr.net"></script>
    <style>
        body { background: #050505; color: white; font-family: sans-serif; margin: 0; }
        .login-box { max-width: 400px; margin: 100px auto; background: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center; }
        input { width: 90%; padding: 10px; margin: 10px 0; background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 5px; }
        button { width: 95%; padding: 10px; background: #00d4ff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .main { display: flex; height: 100vh; }
        .list { width: 30%; background: #111; overflow-y: auto; padding: 10px; }
        .player { width: 70%; background: black; display: flex; align-items: center; }
        .ch-item { padding: 10px; border-bottom: 1px solid #222; cursor: pointer; }
        video { width: 100%; }
    </style>
</head>
<body>
{% if not channels %}
    <div class="login-box">
        <h2>LOGIN XTREAM</h2>
        <form method="POST">
            <input name="host" placeholder="Server URL" required>
            <input name="user" placeholder="Username" required>
            <input name="pass" type="password" placeholder="Password" required>
            <button type="submit">LOGIN</button>
        </form>
    </div>
{% else %}
    <div class="main">
        <div class="list">
            {% for ch in channels %}
            <div class="ch-item" onclick="play('{{host}}/live/{{user}}/{{password}}/{{ch.stream_id}}.ts')">{{ ch.name }}</div>
            {% endfor %}
        </div>
        <div class="player"><video id="video" controls autoplay></video></div>
    </div>
    <script>
        function play(url) {
            var v = document.getElementById('video');
            if(Hls.isSupported()) { var h = new Hls(); h.loadSource(url); h.attachMedia(v); h.on(Hls.Events.MANIFEST_PARSED,function() {v.play();}); }
            else { v.src = url; v.play(); }
        }
    </script>
{% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    channels, host, user, password = [], "", "", ""
    if request.method == 'POST':
        host = request.form.get('host').strip('/')
        user = request.form.get('user')
        password = request.form.get('pass')
        try:
            r = requests.get(f"{host}/player_api.php?username={user}&password={password}&action=get_live_streams", timeout=10)
            channels = r.json()
        except: return "خطأ في الاتصال بالسيرفر"
    return render_template_string(HTML_TEMPLATE, channels=channels, host=host, user=user, password=password)

if __name__ == "__main__":
    app.run()
