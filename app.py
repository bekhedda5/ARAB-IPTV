from flask import Flask, render_template_string, request, Response
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
    <title>IRON PRO PLAYER 2026</title>
    <script src="cdn.jsdelivr.net"></script>
    <style>
        body { background: #050505; color: white; font-family: sans-serif; margin: 0; display: flex; height: 100vh; overflow: hidden; }
        .side-cats { width: 20%; background: #111; border-left: 1px solid #222; overflow-y: auto; }
        .side-chans { width: 25%; background: #181818; border-left: 1px solid #222; overflow-y: auto; display: none; }
        .player-view { flex: 1; background: black; display: flex; align-items: center; position: relative; }
        .item { padding: 12px; border-bottom: 1px solid #222; cursor: pointer; transition: 0.2s; font-size: 13px; }
        .item:hover { background: #00d4ff; color: black; }
        video { width: 100%; height: auto; background: #000; }
        .login { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #0a0a0a; display: flex; justify-content: center; align-items: center; z-index: 100; }
        .box { background: #1e1e1e; padding: 30px; border-radius: 12px; width: 320px; border: 1px solid #00d4ff; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #00d4ff; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

{% if not categories %}
    <div class="login">
        <div class="box">
            <h2 style="text-align:center; color:#00d4ff;">IRON PRO LOGIN</h2>
            <form method="POST">
                <input name="host" placeholder="http://host:port" required>
                <input name="user" placeholder="Username" required>
                <input name="pass" type="password" placeholder="Password" required>
                <button type="submit">دخول مباشر</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="side-cats">
        <h4 style="text-align:center; color:#00d4ff;">الأقسام</h4>
        {% for cat in categories %}
        <div class="item" onclick="loadCh('{{ cat.category_id }}')">{{ cat.category_name }}</div>
        {% endfor %}
    </div>
    <div class="side-chans" id="ch-list">
        <h4 style="text-align:center; color:#00d4ff;">القنوات</h4>
        <div id="ch-container"></div>
    </div>
    <div class="player-view">
        <video id="video" controls autoplay></video>
    </div>

    <script>
        let channels = {{ channels | tojson }};
        function loadCh(id) {
            document.getElementById('ch-list').style.display = 'block';
            let container = document.getElementById('ch-container');
            container.innerHTML = "";
            channels.filter(c => c.category_id == id).forEach(c => {
                let div = document.createElement('div');
                div.className = 'item';
                div.innerText = c.name;
                // استخدام البروكسي الداخلي لتشغيل القناة
                div.onclick = () => {
                    let streamUrl = `/proxy?url=${encodeURIComponent('{{host}}/live/{{user}}/{{password}}/' + c.stream_id + '.ts')}`;
                    play(streamUrl);
                };
                container.appendChild(div);
            });
        }
        function play(url) {
            let v = document.getElementById('video');
            if(Hls.isSupported()) {
                let h = new Hls(); h.loadSource(url); h.attachMedia(v);
                h.on(Hls.Events.MANIFEST_PARSED, () => v.play());
            } else { v.src = url; v.play(); }
        }
    </script>
{% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    categories, channels, host, user, password = [], [], "", "", ""
    if request.method == 'POST':
        host = request.form.get('host').strip('/')
        user = request.form.get('user')
        password = request.form.get('pass')
        try:
            categories = requests.get(f"{host}/player_api.php?username={user}&password={password}&action=get_live_categories").json()
            channels = requests.get(f"{host}/player_api.php?username={user}&password={password}&action=get_live_streams").json()
        except: pass
    return render_template_string(HTML_TEMPLATE, categories=categories, channels=channels, host=host, user=user, password=password)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    r = requests.get(url, stream=True, timeout=10)
    return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get('Content-Type'))

if __name__ == "__main__":
    app.run()
    
