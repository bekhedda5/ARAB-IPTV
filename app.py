from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# تصميم الواجهة الاحترافية (CSS + HTML)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XTREAM PLAYER 2026</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }
        .login-container { max-width: 400px; margin: 50px auto; background: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #333; }
        h2 { text-align: center; color: #00d4ff; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #444; background: #2a2a2a; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #00d4ff; border: none; border-radius: 8px; color: black; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #008fb3; }
        .channels-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; padding: 20px; }
        .channel-card { background: #1e1e1e; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; transition: 0.3s; }
        .channel-card:hover { transform: scale(1.05); border-color: #00d4ff; }
        img { width: 60px; height: 60px; border-radius: 50%; margin-bottom: 10px; background: #333; }
        a { text-decoration: none; color: white; font-size: 14px; }
    </style>
</head>
<body>

{% if not channels %}
    <div class="login-container">
        <h2>XTREAM LOGIN 2026</h2>
        <form method="POST">
            <input type="text" name="host" placeholder="السيرفر (Host URL)" required>
            <input type="text" name="user" placeholder="اسم المستخدم (Username)" required>
            <input type="password" name="pass" placeholder="كلمة المرور (Password)" required>
            <button type="submit">دخول مباشر</button>
        </form>
    </div>
{% else %}
    <h2 style="text-align:center;">قائمة القنوات المباشرة</h2>
    <div class="channels-grid">
        {% for ch in channels %}
        <div class="channel-card">
            <img src="{{ ch.stream_icon }}" onerror="this.src='via.placeholder.com'">
            <br>
            <a href="{{ host }}/live/{{ user }}/{{ password }}/{{ ch.stream_id }}.ts" target="_blank">
                {{ ch.name }}
            </a>
        </div>
        {% endfor %}
    </div>
{% endif %}

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    channels = []
    host = ""
    user = ""
    password = ""
    
    if request.method == 'POST':
        host = request.form.get('host').strip('/')
        user = request.form.get('user')
        password = request.form.get('pass')
        
        # الاتصال بسيرفر Xtream
        api_url = f"{host}/player_api.php?username={user}&password={password}&action=get_live_streams"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                channels = response.json()
        except:
            return "خطأ في الاتصال بالسيرفر. تأكد من البيانات."

    return render_template_string(HTML_TEMPLATE, channels=channels, host=host, user=user, password=password)

if __name__ == "__main__":
    app.run()
    
