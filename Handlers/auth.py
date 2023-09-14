import tornado.web
import jwt
import json
import datetime

class RegisterHandler(tornado.web.RequestHandler):
    def initialize(self, users):
        self.users = users
    def post(self):
        try:
            user_data = json.loads(self.request.body.decode("utf-8"))
            username = user_data.get("username")
            password = user_data.get("password")

            if not username or not password:
                self.set_status(400)
                self.write({"error": "Username and password are required"})
                return
            
            self.users.append({"username": username, "password": password})
            self.write({"massage": "User registered successfully"})
 
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': 'Invalid JSON Format'})

class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, users, secret_key):
        self.users = users
        self.secret_key = secret_key
    def get(self):
        # Baca file HTML dan kirimkan sebagai respons
        with open("login.html", "r") as file:
            html_content = file.read()
            self.write(html_content)

    def post(self):
        try:
            user_data = json.loads(self.request.body.decode("utf-8"))
            username = user_data.get("username")
            password = user_data.get("password")

            if not username or not password:
                self.set_status(400)
                self.write({"error": "Username and password are required"})
                return

            for user in self.users:
                if user["username"] == username and user["password"] == password:
                    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
 
                    payload = {
                        "username": username,
                        "exp": expiration_time
                    }

                    token = jwt.encode(payload, self.secret_key, algorithm="HS256")
                    # print(token)
                    
                    # Set token dalam cookie
                    self.set_cookie("jwtToken", token)
                    
                    # Mengirim token sebagai respons JSON (opsional)
                    self.write({"token": token})
                    return

            self.set_status(401)
            self.write({"error": "Invalid username or password"})
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': 'Invalid JSON Format'})