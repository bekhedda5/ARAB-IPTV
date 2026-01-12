from flask import Flask, render_template_string, request, jsonify
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
    <title>IRON PRO STYLE - 2026</title>
    <script src="cdn.jsdelivr.net"></script>
    <style>
        body { background: #0a0a0a; color: white; font-family: sans-serif; margin: 0; display: flex; height: 100vh; overflow: hidden; }
        
        /* الأقسام - مثل Iron Pro */
        .categories { width: 20%; background: #111; border-left: 1px solid #222; overflow-y: auto; }
        .cat-item { padding: 15px; border-bottom: 1px solid #1a1a1a; cursor: pointer; font-size: 14px; transition: 0.3s; color: #bbb; }
        .cat-item:hover, .cat-active { background: #00d4ff; color: black; font-weight: bold; }

        /* قائمة القنوات */
        .channels { width: 25%; background: #181818; border-left: 1px solid #222; overflow-y: auto; display: none; }
        .ch-item { padding: 12px; border-bottom: 1px solid #222; cursor: pointer; display: flex; align-items: center; }
        .ch-item img { width: 30px; height: 30px; margin-left: 10px; border-radius: 4px; }
        .ch-item:hover { background: #333; }

        /* المشغل */
        .player-container { flex: 1; background: black; display: flex; flex-direction: column; justify-content: center; position: relative; }
        video { width: 100%; height: auto; max-height: 80vh; }
        
        .login-box { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #1e1e1e; padding: 30px; border-radius: 10px; width: 350px; text-align: center; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #00d4ff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

{% if not categories %}
    <div class="login-box">
        <h2 style="color:#00d4ff">IRON PRO CLONE</h2>
        <form method="POST">
            <input name="host" placeholder="http://server.com:8080" required>
            <input name="user" placeholder="Username" required>
            <input name="pass" type="password" placeholder="Password" required>
            <button type="submit">تسجيل الدخول</button>
        </form>
    </div>
{% else %}
    <!-- قائمة الأقسام -->
    <div class="categories">
        <h3 style="text-align:center; color:#00d4ff; padding:10px;">الأقسام</h3>
        {% for cat in categories %}
        <div class="cat-item" onclick="loadChannels('{{ cat.category_id }}')">{{ cat.category_name }}</div>
        {% endfor %}
    </div>

    <!-- قائمة القنوات (ستظهر عند الضغط على قسم) -->
    <div class="channels" id="channels-list">
        <h3 style="text-align:center; color:#00d4ff; padding:10px;">القنوات</h3>
        <div id="channels-container"></div>
    </div>

    <!-- مشغل الفيديو -->
    <div class="player-container">
        <video id="video" controls autoplay></video>
        <h3 id="current-ch" style="text-align:center; color:#00d4ff"></h3>
    </div>

    <script>
        let allChannels = {{ channels | tojson }};
        let host = "{{ host }}";
        let user = "{{ user }}";
        let pass = "{{ password }}";

        function loadChannels(catId) {
            document.getElementById('channels-list').style.display = 'block';
            let container = document.getElementById('channels-container');
            container.innerHTML = "";
            
            let filtered = allChannels.filter(ch => ch.category_id == catId);
            filtered.forEach(ch => {
                let div = document.createElement('div');
                div.className = 'ch-item';
                div.innerHTML = `<img src="${ch.stream_icon}" onerror="this.src='via.placeholder.com'">${ch.name}`;
                div.onclick = () => play(`${host}/live/${user}/${pass}/${ch.stream_id}.ts`, ch.name);
                container.appendChild(div);
            });
        }

        function play(url, name) {
            document.getElementById('current-ch').innerText = name;
            var v = document.getElementById('video');
            if(Hls.isSupported()) {
                var h = new Hls();
                h.loadSource(url);
                h.attachMedia(v);
                h.on(Hls.Events.MANIFEST_PARSED, () => v.play());
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
    categories, channels, host, user, password = [], [], "", "", ""
    if request.method == 'POST':
        host = request.form.get('host').strip('/')
        user = request.form.get('user')
        password = request.form.get('pass')
        try:
            # جلب الأقسام والقنوات
            cat_r = requests.get(f"{host}/player_api.php?username={user}&password={password}&action=get_live_categories", timeout=10)
            ch_r = requests.get(f"{host}/player_api.php?username={user}&password={password}&action=get_live_streams", timeout=10)
            categories = cat_r.json()
            channels = ch_r.json()
        except: return "خطأ في بيانات السيرفر"
        
    return render_template_string(HTML_TEMPLATE, categories=categories, channels=channels, host=host, user=user, password=password)

if __name__ == "__main__":
    app.run()
