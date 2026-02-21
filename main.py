import telebot
import requests
import socket
from flask import Flask
from threading import Thread
import os

TOKEN = '8222981632:AAHdlIgt95sXQz97BYiMSNIbfYwXNYwFra4'
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# --- 1. QUÉT THÔNG TIN IP THẬT (REAL SCAN) ---
@bot.message_handler(commands=['ip'])
def ip_info(message):
    ip = message.text.replace('/ip', '').strip()
    if not ip:
        bot.reply_to(message, "⚠️ Sếp nhập IP cần check đi. VD: `/ip 8.8.8.8`", parse_mode='Markdown')
        return
    
    res = requests.get(f"http://ip-api.com/json/{ip}").json()
    if res['status'] == 'success':
        info = (
            f"🌐 **THÔNG TIN IP THẬT**\n"
            f"📍 Quốc gia: {res['country']}\n"
            f"🏙 Thành phố: {res['city']}\n"
            f"📡 Nhà mạng: {res['isp']}\n"
            f"🎯 Tọa độ: {res['lat']}, {res['lon']}\n"
            f"🏷 IP: `{res['query']}`"
        )
        bot.reply_to(message, info, parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ Không lấy được thông tin IP này.")

# --- 2. QUÉT CỔNG SERVER (REAL PORT SCAN) ---
@bot.message_handler(commands=['scanport'])
def scan_port(message):
    target = message.text.replace('/scanport', '').strip()
    if not target:
        bot.reply_to(message, "⚠️ Nhập domain/IP. VD: `/scanport google.com`", parse_mode='Markdown')
        return

    ports = [21, 22, 80, 443, 3306, 8080]
    open_ports = []
    bot.send_message(message.chat.id, f"⚡ Đang quét các cổng phổ biến trên {target}...")

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(str(port))
        sock.close()

    if open_ports:
        bot.send_message(message.chat.id, f"✅ Mục tiêu: {target}\n🔓 Cổng đang mở: `{', '.join(open_ports)}`", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f"🛡 Mục tiêu {target} có vẻ rất kín kẽ, không thấy cổng nào mở.")

# --- 3. KIỂM TRA WEB DÙNG CÔNG NGHỆ GÌ (CMS DETECT) ---
@bot.message_handler(commands=['checkweb'])
def check_web(message):
    url = message.text.replace('/checkweb', '').strip()
    if not url:
        bot.reply_to(message, "⚠️ Nhập URL. VD: `/checkweb https://vnexpress.net`", parse_mode='Markdown')
        return
    
    try:
        r = requests.get(url, timeout=5)
        headers = str(r.headers).lower()
        cms = "Không xác định"
        if "wp-content" in r.text: cms = "WordPress"
        elif "joomla" in r.text: cms = "Joomla"
        
        server = r.headers.get('Server', 'Bảo mật/Ẩn')
        bot.reply_to(message, f"🔍 **KẾT QUẢ WEB**\n🌐 CMS: `{cms}`\n🖥 Server: `{server}`", parse_mode='Markdown')
    except:
        bot.reply_to(message, "❌ Không thể kết nối tới trang web này.")

# --- GIỮ BOT SỐNG ---
@app.route('/')
def home(): return "HACKER SYSTEM ONLINE 💀"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
