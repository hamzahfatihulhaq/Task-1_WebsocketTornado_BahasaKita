import tornado.web
import os
import json
from jwt_util import jwt_required

class GetAudios (tornado.web.RequestHandler):
    def initialize(self, audioId):
        self.audioId = audioId
    
    @jwt_required
    async def get(self,audioId):
        # print(self.audioId)
        # audio_id = self.get_query_argument("audioId")
        metadata_folder = "Metadatadb"
        audio_metadata = None

        # Cari file metadata berdasarkan audioId
        for audio_file in os.listdir(metadata_folder):
            if audio_file.startswith(audioId):
                file_path = os.path.join(metadata_folder, audio_file)
                with open(file_path, "r") as f:
                    audio_metadata = json.load(f)
                break  # Keluar dari loop setelah menemukan file metadata yang sesuai

        if audio_metadata:
            self.write({"metadata": audio_metadata})
        else:
            self.set_status(404)  # Set status 404 jika metadata tidak ditemukan
            self.write({"error": "Audio not found"})