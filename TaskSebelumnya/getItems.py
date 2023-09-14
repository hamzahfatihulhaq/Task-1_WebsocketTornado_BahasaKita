import tornado.web
from jwt_util import jwt_required

class GetItems(tornado.web.RequestHandler):
    def initialize(self, items):  
        self.items = items
    @jwt_required
    async def get(self):
        self.write({"Items": self.items})