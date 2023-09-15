import tornado.web
import json
from jwt_util import jwt_required

class TodoItems(tornado.web.RequestHandler):
    def initialize(self, items):
        self.items = items
    
    @jwt_required
    async def post(self, _):
        try:
            item = json.loads(self.request.body.decode("utf-8"))
            self.items.append(item)
            self.write({'message': item})
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': 'Invalid JSON format'})
    
    @jwt_required
    async def put(self, item_id):
        try:
            item_data = json.loads(self.request.body.decode("utf-8"))
            for i in range(len(self.items)):
                if self.items[i]["id"] == item_id:
                    self.items[i] = {
                        "id": item_id,
                        "name": item_data["name"]
                    }
                    self.write({"message": "Item updated"})
                    break
            else:
                self.set_status(404)
                self.write({"error": "Item not found"})

        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': 'Invalid JSON format'})

    @jwt_required
    async def delete(self, item_id):
        found_item = None
        for item in self.items:
            if item.get("id") == item_id:
                found_item = item
                break
        
        if found_item:
            self.items.remove(found_item)
            self.write({"message": "Item deleted"})
        else:
            self.set_status(404)
            self.write({"error": "Item not found"})
