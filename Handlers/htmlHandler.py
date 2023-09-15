import tornado.web
from jwt_util import jwt_required,verify_jwt

class HTMLHandler(tornado.web.RequestHandler):
    def initialize(self) :
        # Ambil token dari cookie
        self._jwt_token = self.get_cookie("jwtToken")

    async def get(self):
        user_info = verify_jwt(self._jwt_token)
        # print(user_info[0])
        if not user_info[0]:
            self.write({"error": user_info[1]})
        else:
            self.user_info = user_info  
            with open("index.html", "r") as file:
                html_content = file.read()
                self.write(html_content)
