from tornado.websocket import WebSocketHandler
import os
import subprocess
from jwt_util import jwt_required,verify_jwt
import tornado.ioloop

class AudioWebSocketHandler(WebSocketHandler):
    connections = set()
    def check_origin(self, origin):
        # Contoh sederhana: hanya menerima permintaan dari origin tertentu
        allowed_origins = ["http://localhost:8888", "https://example.com"]
        return origin in allowed_origins
    # @jwt_required
    async def open(self,token):
        user_info = verify_jwt(token)
        if not user_info[0]:
            self.close()  # Tutup koneksi jika token tidak valid
        else:
            self.user_info = user_info  # Simpan informasi pengguna dari token JWT
            self.connections.add(self)
        
    
    def on_message(self, message):
        # Tindakan yang akan diambil saat pesan diterima
        for conn in self.connections:
            conn.write_message(message)
 

    # def on_close(self):
    #     print("WebSocket ditutup")
    #     try:
    #         subprocess.run(["python", "Handlers/encodeAudio.py"])
    #         self.connections.remove(self)
    #     except Exception as e:
    #         print("Error saat menjalankan encodeAudio.py:", str(e))

    def on_close(self):
        print("WebSocket ditutup")
        try:
            self.connections.remove(self)
        except Exception as e:
            print("Error saat menjalankan encodeAudio.py:", str(e))

        self.run_encode_audio_callback()

    async def run_encode_audio(self):
        loop = tornado.ioloop.IOLoop.current()
        await loop.run_in_executor(None, subprocess.run, ["python", "Handlers/encodeAudio.py"])


    def run_encode_audio_callback(self):
        loop = tornado.ioloop.IOLoop.current()
        loop.add_callback(self.run_encode_audio)

    
