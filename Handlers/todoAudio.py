import os
import tornado.web
import uuid
import json
from  Schemas.audioSchemas import get_audio_metadata
from jwt_util import jwt_required

class TodoAudios(tornado.web.RequestHandler):
    @jwt_required
    async def post(self):
        try:
            audio_data = self.request.files.get("audio_data")[0]

            # Membuat ID unik
            unique_id = self.create_unique_id()
            # Simpan file sementara
            file_path = os.path.join("Uploads", unique_id + "_" + audio_data.filename)
            with open(file_path, "wb") as f:
                f.write(audio_data.body)

            # Simpan metadata audio ke folder "Metadatadb"
            metadata =  get_audio_metadata(file_path)
            metadata_file_path = os.path.join("Metadatadb", unique_id + ".json")
            with open(metadata_file_path, "w") as metadata_file:
                json.dump(metadata, metadata_file)

            self.write({"message": f"Audio uploaded successfully with ID: {unique_id}"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

    def create_unique_id(self):
        # Kode untuk membuat ID unik di sini, misalnya dengan modul uuid
        unique_id = str(uuid.uuid4())  # Membuat UUID versi 4 (random)
        return unique_id