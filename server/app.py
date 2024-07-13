from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)


api = Api(app)

db.init_app(app)


class Messages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]
        headers = {
            "Content-Type": "application/json"
        }

        response = make_response(messages, 200, headers)
        return response
    def post(self):
        params = request.json
        new_message = Message(username=params['username'], body=params['body'])
        db.session.add(new_message)
        db.session.commit()
        response = make_response(new_message.to_dict(), 201)
        return response


api.add_resource(Messages, "/messages")

class MessagesById(Resource):
    def patch(self, id):
        params = request.json
        message = Message.query.get(id)
        for attr in params:
            setattr(message, attr, params[attr])
        db.session.commit()
        response = make_response(jsonify(message.to_dict()), 200)
        return response
    def delete(self, id):
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        response = make_response("sucessfully deleted",204)
        return response



api.add_resource(MessagesById, "/messages/<int:id>")

if __name__ == '__main__':
    app.run(port=4000)