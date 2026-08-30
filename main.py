import asyncio
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Web server giả lập giữ port cho Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot status: OK")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# Lấy các biến môi trường
api_id_raw = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
session_str = os.environ.get("SESSION_STRING")

if not api_id_raw or not api_hash or not session_str:
    print("LỖI: Bạn chưa thêm đầy đủ API_ID, API_HASH hoặc SESSION_STRING trong tab Environment của Render!")
else:
    api_id = int(api_id_raw)
    client = TelegramClient(StringSession(session_str), api_id, api_hash)

    async def main():
        await client.connect()
        if not await client.is_user_authorized():
            print("LỖI: SESSION_STRING bị sai hoặc đã bị Telegram hủy do đăng xuất!")
            return
            
        print("Bot đã kết nối thành công!")
        while True:
            now_vn = datetime.utcnow() + timedelta(hours=7)
            time_str = now_vn.strftime("%H : %M")
            new_name = f"사랑해요 {time_str}"
            
            try:
                await client(UpdateProfileRequest(first_name=new_name))
                print(f"Đã cập nhật tên: {new_name}")
            except Exception as e:
                print(f"Lỗi khi đổi tên: {e}")
            
            await asyncio.sleep(60)

    asyncio.run(main())
