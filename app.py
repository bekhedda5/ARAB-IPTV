from flask import Flask, render_template_string, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XTREAM PLAYER 2026</title>
    <script src="cdn.jsdelivr.net"></script>
    <style>
        body { background: #050505; color: white; font-family: sans-serif; margin: 0; display: flex; height: 100vh; overflow: hidden; }
        .list { width: 30%; background: #111; overflow-y: auto; border-left: 1px solid #333; }
        .player-container { width: 70%; background: black; display: flex; flex-direction: column; justify-content: center; }
        .ch-item { padding: 15px; border-bottom: 1px solid #222; cursor: pointer; transition: 0.3s; }
        .ch-item:hover { background: #00d4ff; color: black; }
        video { width: 100%; max-height: 100%; }
        .login-box { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #1e1e1e; padding: 30px; border-radius: 10px; text-align: center; width: 350px; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #00d4ff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
{% if not channels %}
    <div class="login-box">
        <h2 style="color:#00d4ff">XTREAM LOGIN</h2>
        <form method="POST">
            <input name="host" placeholder="http://server.com:8080" required>
            <input name="user" placeholder="Username" required>
            <input name="pass" type="password" placeholder="Password" required>
            <button type="submit">دخول</button>
        </form>
    </div>
{% else %}
    <div class="list">
        <h3 style="text-align:center; color:#00d4ff">قائمة القنوات</h3>
        {% for ch in channels %}
        <div class="ch-item" onclick="play('{{host}}/live/{{user}}/{{password}}/{{ch.stream_id}}.ts')">{{ ch.name }}</div>
        {% endfor %}
    </div>
    <div class="player-container">
        <video id="video" controls autoplay></video>
    </div>
    <script>
        function play(url) {
            var v = document.getElementById('video');
            // استبدال البروتوكول ليتوافق مع الموقع إذا لزم الأمر
            if (window.location.protocol === 'https:' && url.startsWith('http:')) {
                console.warn("قد لا يعمل الفيديو بسبب سياسة HTTPS/HTTP");
            }
            if(Hls.isSupported()) {
                var h = new Hls();
                h.loadSource(url);
                h.attachMedia(v);
                h.on(Hls.Events.MANIFEST_PARSED,function() { v.play(); });
            } else {
                v.src = url;
                v.play();
            }
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
        except: return "خطأ في الاتصال بالسيرفر - تأكد من الرابط"
    return render_template_string(HTML_TEMPLATE, channels=channels, host=host, user=user, password=password)

if __name__ == "__main__":
    app.run()
    
