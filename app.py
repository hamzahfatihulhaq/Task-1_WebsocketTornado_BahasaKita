import tornado.web
import tornado.ioloop
from Handlers.getAudio import GetAudios
from Handlers.todoAudio import TodoAudios
from Handlers.auth import RegisterHandler, LoginHandler
from Handlers.audioSocket import AudioWebSocketHandler
from Handlers.htmlHandler import HTMLHandler
from Handlers.encodeAudio import EncodeAudios
from tornado.web import HTTPError
from jwt_util import SECRET_KEY
secret_key = SECRET_KEY

items = []
users = []

def make_app():
    return tornado.web.Application([
        (r"/", HTMLHandler),
        (r"/get_audio/([a-zA-Z0-9-]+)", GetAudios, dict(audioId=None)),
        (r"/encodeAudio/", EncodeAudios),
        (r"/audio/", TodoAudios),
        (r"/register", RegisterHandler,  {"users": users}),
        (r"/login", LoginHandler,  {"users": users, "secret_key": secret_key}),
        (r"/websocket/([^/]+)", AudioWebSocketHandler),
    ],
    debug=True,
    autoreload=True,
    )

if __name__ == '__main__':
    app = make_app()
    port = 8888
    app.listen(port)
    print(f'Server is listening on localhost on port {port}')
    
    try:
        tornado.ioloop.IOLoop.current().start()
    except HTTPError as e:
        print(f"HTTP Error: {e.status_code} - {e.reason}")