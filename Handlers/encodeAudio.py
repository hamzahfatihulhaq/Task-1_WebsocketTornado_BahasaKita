import base64
import tornado.web
import os

def encode_audio():
    try:
        upload_folder = "Uploads"
        audio_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]

        for audio_file in audio_files:
            # Baca file audio
            file_path = os.path.join(upload_folder, audio_file)
            with open(file_path, "rb") as f:
                audio_data = f.read()

            # Konversi ke base64
            encoded_audio = base64.b64encode(audio_data).decode("utf-8")

            # Simpan file dalam folder "Audiodb" dengan ekstensi yang sesuai
            audio_id = os.path.splitext(audio_file)[0].split("_")[0]
            audio_db_path = os.path.join("Audiodb", f"{audio_id}.base64")
            chunk_size = 3200
            
            with open(audio_db_path, "w") as file:
                for i in range(0, len(encoded_audio), chunk_size):
                    audio_chunk = encoded_audio[i:i+chunk_size]
                    file.write(audio_chunk + "\n")

            # Hapus file audio dari folder "Uploads"
            os.remove(file_path)

        return {"message": f"All Audio success save in Audiodb"}
    except Exception as e:
        return {"error": str(e)}
                
class EncodeAudios(tornado.web.RequestHandler):
    async def post(self):
        response_data = encode_audio()
        if "error" in response_data:
            self.set_status(500)
        self.write(response_data)

encode_audio()