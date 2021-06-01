from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="this field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True,
                        help="every item needs a store id.")

    @jwt_required()
    def get(self, name):
        user = {'hello': current_identity.username}
        print(user)
        item = ItemModel.find_by_name(name)
        if item:
            return item.jsonInt()
        return {"message": "Item not found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured interting the item."}, 500
        return item.jsonInt(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
        item.save_to_db()
        return item.jsonInt()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.jsonInt(), ItemModel.query.all()))}

