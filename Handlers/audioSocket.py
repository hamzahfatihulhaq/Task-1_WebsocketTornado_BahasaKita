from tornado.websocket import WebSocketHandler
import os
import subprocess
from jwt_util import jwt_required

class AudioWebSocketHandler(WebSocketHandler):
    connections = set()
    def open(self):
        self.connections.add(self)
    
    def on_message(self, message):
        # Tindakan yang akan diambil saat pesan diterima
        for conn in self.connections:
            conn.write_message(message)
 

    def on_close(self):
        print("WebSocket ditutup")
        try:
            subprocess.run(["python", "Handlers/encodeAudio.py"])
            self.connections.remove(self)
        except Exception as e:
            print("Error saat menjalankan encodeAudio.py:", str(e))
    
