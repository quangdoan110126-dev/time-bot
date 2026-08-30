  import asyncio
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Tạo web server giả lập port để Render không báo lỗi
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Chạy Web Server ở luồng riêng
threading.Thread(target=run_web_server, daemon=True).start()

# Lấy biến môi trường
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_str = os.environ.get("SESSION_STRING")

client = TelegramClient(StringSession(session_str), api_id, api_hash)

async def main():
    await client.start()
    print("Bot đã kết nối thành công!")
    while True:
        # Lấy giờ phút theo múi giờ Việt Nam (UTC+7)
        now_vn = datetime.utcnow() + timedelta(hours=7)
        time_str = now_vn.strftime("%H : %M")
        
        # Tên cũ kết hợp với thời gian
        new_name = f"off {time_str}"
        
        try:
            await client(UpdateProfileRequest(first_name=new_name))
            print(f"Đã cập nhật tên: {new_name}")
        except Exception as e:
            print(f"Lỗi: {e}")
        
        # Chờ 60 giây để nhảy sang phút tiếp theo
        await asyncio.sleep(60)

with client:
    client.loop.run_until_complete(main())
