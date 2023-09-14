import tornado.web
from jwt_util import jwt_required

class HTMLHandler(tornado.web.RequestHandler):
    # @jwt_required
    async def get(self):
        # Ambil token dari cookie
        jwt_token = self.get_cookie("jwtToken")
        
        # Jika ada token JWT, tambahkan header Authorization
        if jwt_token:
            self.set_header("Authorization", f"Bearer {jwt_token}")
            
        # Baca file HTML dan kirimkan sebagai respons
        with open("index.html", "r") as file:
            html_content = file.read()
            self.write(html_content)
