import tornado.web
import tornado.ioloop
from tornado.web import HTTPError
from decouple import config
import jwt
import json
from datetime import datetime

SECRET_KEY = config('SECRET_KEY')

def check_jwt_expired(jwt_token):
    try:
        # Parse JWT token
        decoded = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        # Ambil waktu kedaluwarsa dari payload JWT
        jwt_exp = decoded.get('exp', None)

        if jwt_exp:
            current_time = datetime.utcnow().timestamp()
            # Periksa apakah waktu kedaluwarsa JWT kurang dari waktu saat ini
            return jwt_exp < current_time

        return False  # Kembalikan False jika tidak ada waktu kedaluwarsa dalam JWT
    except jwt.ExpiredSignatureError:
        return True  # JWT telah kedaluwarsa

def jwt_required(handler_method):
    async def check_jwt(self, *args, **kwargs):
        token = self.request.headers.get('Authorization', None)

        if not token:
            error_response = {
                'error': 'Authorization header is missing'
            }
            self.set_header('Content-Type', 'application/json')
            self.set_status(401)
            self.write(json.dumps(error_response))
            self.finish()
            raise HTTPError(401, "Authorization header is missing")
        
        # Split token berdasarkan spasi
        token_parts = token.split(' ')

        # Pastikan token terdiri dari dua bagian (Bearer dan token itu sendiri)
        if len(token_parts) != 2:
            error_response = {
                'error': 'Invalid token format'
            }
            self.set_header('Content-Type', 'application/json')
            self.set_status(401)
            self.write(json.dumps(error_response))
            self.finish()
            raise HTTPError(401, "Invalid token format")

        # Ambil bagian token saja
        token_value = token_parts[1]

        # Periksa apakah JWT kedaluwarsa
        if check_jwt_expired(token_value):
            error_response = {
                'error': 'Token has expired'
            }
            self.set_header('Content-Type', 'application/json')
            self.set_status(401)
            self.write(json.dumps(error_response))
            self.finish()
            raise HTTPError(401, 'Token has expired')

        try:
            decoded = jwt.decode(token_value, SECRET_KEY, algorithms=['HS256'])
            self.current_user = decoded
            result = await handler_method(self, *args, **kwargs)
            return result
        except jwt.InvalidTokenError:
            error_response = {
                'error': 'Invalid token'
            }
            self.set_header('Content-Type', 'application/json')
            self.set_status(401)
            self.write(json.dumps(error_response))
            self.finish()
            raise HTTPError(401, 'Token is invalid')
    
    return check_jwt
