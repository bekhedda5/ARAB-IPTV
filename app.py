from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XTREAM VIP PLAYER 2026</title>
    <script src="cdn.jsdelivr.net"></script>
    <style>
        body { background: #050505; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #111; padding: 15px; text-align: center; border-bottom: 2px solid #00d4ff; }
        .main-container { display: flex; flex: 1; overflow: hidden; }
        
        /* مشغل الفيديو */
        .player-section { flex: 2; background: black; display: flex; flex-direction: column; justify-content: center; }
        video { width: 100%; max-height: 80vh; background: black; box-shadow: 0 0 20px rgba(0,212,255,0.2); }
        
        /* قائمة القنوات */
        .channels-list { flex: 1; background: #111; overflow-y: auto; border-right: 1px solid #333; padding: 10px; }
        .channel-item { display: flex; align-items: center; padding: 10px; margin-bottom: 8px; background: #1e1e1e; border-radius: 8px; cursor: pointer; transition: 0.3s; border: 1px solid transparent; }
        .channel-item:hover { background: #2a2a2a; border-color: #00d4ff; }
        .channel-item img { width: 40px; height: 40px; border-radius: 5px; margin-left: 10px; }
        
        /* نموذج الدخول */
        .login-box { max-width: 400px; margin: 100px auto; background: #1e1e1e; padding: 30px; border-radius: 15px; border: 1px solid #333; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #444; background: #2a2a2a; color: white; }
        button { width: 100%; padding: 12px; background: #00d4ff; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

{% if not channels %}
    <div class="login-box">
        <h2 style="text-align:center; color:#00d4ff;">XTREAM LOGIN</h2>
        <form method="POST">
            <input type="text" name="host" placeholder="http://host-url:port" required>
            <input type="text" name="user" placeholder="Username" required>
            <input type="password" name="pass" placeholder="Password" required>
            <button type="submit">دخول للمشغل</button>
        </form>
    </div>
{% else %}
    <div class="header">
        <h3 id="current-channel">اختر قناة للبدء...</h3>
    </div>
    <div class="main-container">
        <!-- قائمة القنوات -->
        <div class="channels-list">
            {% for ch in channels %}
            <div class="channel-item" onclick="playChannel('{{ host }}/live/{{ user }}/{{ password }}/{{ ch.stream_id }}.ts', '{{ ch.name }}')">
                <img src="{{ ch.stream_icon }}" onerror="this.src='via.placeholder.com'">
                <span>{{ ch.name }}</span>
            </div>
            {% endfor %}
        </div>
        
        <!-- قسم الفيديو -->
        <div class="player-section">
            <video id="video" controls autoplay></video>
        </div>
    </div>

    <script>
        function playChannel(url, name) {
            document.getElementById('current-channel').innerText = "تشغيل الآن: " + name;
            var video = document.getElementById('video');
            if (Hls.isSupported()) {
                var hls = new Hls();
                hls.loadSource(url);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    video.play();
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = url;
                video.addEventListener('loadedmetadata', function() {
                    video.play();
                });
            }
        }
    </script>
{% endif %}

</body>
</html>
